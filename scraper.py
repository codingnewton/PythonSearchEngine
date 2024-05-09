import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import io
import sqlite3
import json
import datetime
import dateutil.parser
import copy
import numpy as np

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')

class page:
    crawled_url = set()
    def __init__(self, url=None):
        if url == None:
            self.title = ""
            self.body = ""
            self.url = ""
            self.last_mod_date = ""
            self.file_size = 0
            self.kw_freq = [] # This should be an array or set of tuples
            self.child_link = []
            self.parent_link = []
            self.link_queue = []
            self.stemmed = []
            self.keyword_counts = {} # wordfreq() has to be executed to store this
            self.page_title_kword = {}
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            self.body = soup.find('body').get_text()
            self.child_link = []
            self.parent_link = []
            self.stemmed = []
            self.keyword_counts = {}
            self.page_title_kword = {}
            
            # Extract title, url, last mod date and file size
            self.title = soup.find('title').text
            self.url = url
            if response.status_code == 200: #successful => 200
                self.file_size = len(response.content)
                self.last_mod_date = response.headers.get('last-modified')
            
            # handling <a> tags and extract parent and children link
            link_tags = soup.find_all("a")
            links = [link.get('href') for link in link_tags]
            #print(links[:10])
            full_links = [urljoin(response.url, link) for link in links]
            #print(f"full links: {full_links[:10]}")
            self.link_queue = [full_link for full_link in full_links]
            url_cleaned = response.url.split(".htm")[0].strip()

            for link in full_links:
                if response.url.startswith(link.split(".htm")[0].strip()) | self.hascrawled(link):
                    if link not in self.parent_link:
                        self.parent_link.append(link)
                        full_links.remove(link)
            for link in full_links:
                if len(self.child_link) < 10:
                    if link not in self.child_link:
                        self.child_link.append(link)

            self.crawled_url.add(url)

    def hascrawled(self, link) -> bool:
        if link in self.crawled_url:
            return True
        else:
            return False

    def __repr__(self) -> str:
        pagetitle = f"Page Title: {self.title}\n" 
        url = f"URL: {self.url}\n"
        modidate = f"Last modification date: {self.last_mod_date} | Size of Page: {self.file_size}Bytes\n"
        keyfreq = f"Keyword frequency: {self.returnwordfreq(10)}\n"
        childlink = f"Child Links: {self.child_link[:10]}\n"
        parentlink = f"Parent Links: {self.parent_link}\n"
        hypens = "-------------------------------------------------------------------\n"
        return pagetitle + url + modidate + keyfreq + childlink + parentlink + hypens

    def __lt__(self, other): #return if self < other, if self is older than other, then return true 
        sefdate = self.convertdate()
        otherdate = other.convertdate()
        return sefdate < otherdate

    def convertdate(self) -> datetime:
        str = self.last_mod_date
        month_dict = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }
        return datetime.datetime(int(str[12:16]), month_dict[str[8:11]], int(str[5:7]), int(str[17:19]), int(str[20:22]), int(str[23:25]))
    
    def stopstem(self, url, text): # stemming and stopword removal
        stemmer = PorterStemmer()
        words = word_tokenize(text)                                     # Tokenizing
        punct = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        stopwords = open('stopwords.txt').read().splitlines()
        for word in words:
            if word in punct:
                words.remove(word)
                continue
            elif word in stopwords:                                     # Stopword Removal
                words.remove(word)
                continue
        stemmed = [stemmer.stem(word) for word in words]
        self.stemmed = stemmed
        return stemmed
    
    def wordfreq(self, stemmed, mode):
        keyword_counts = {}
        # Increment count for this keyword
        for word in stemmed:
            keyword_counts[word] = keyword_counts.get(word, 0) + 1
        if mode == 'b':
            self.keyword_counts = keyword_counts
        if mode == 't':
            self.page_title_kword = keyword_counts
        return keyword_counts

    def returnwordfreq(self, n):
        """
        Args:
            n (int): number of keywords and values you would like to return
        Returns:
            string: in the format of key1 freq1; key2 freq2; key3 freq3; ...
        """
        keyword_counts = self.keyword_counts
        return '; '.join(f"{k} {v}" for k, v in list(keyword_counts.items())[:n])

    def returnwordfreqlist(self,n):
        # return a list of keywords and values with length n
        word_list = self.keyword_counts
        return list(word_list.items())[:n]

    def sortwordfreq(self):                                             # For later use
        keyword_counts = self.keyword_counts
        sorted_keyword_counts = sorted(keyword_counts.items, key = lambda x:x[1], reverse = True)
        self.keyword_counts = dict(sorted_keyword_counts)
        pass
    
    def deep_copy(self):
        return copy.deepcopy(self)

        

class HTML_list:
    crawled_list = set()

    def deep_copy(self):
        return copy.deepcopy(self)    

    def __init__(self):
       self.HTML_list = [] # list of page for later sorting
        # Web graph for PageRanking

    def get_object_at(self, idx):
        try: 
            return self.HTML_list[idx]
        except:
            print("Error: Invalid argument")
            return 0

    def create_web_graph(self):
        web_graph = {}
        for obj in self.HTML_list:
            if obj.url not in web_graph:
                web_graph[obj.url] = obj.child_link
        
        return web_graph

    def crawl(self, url, n):
        """Recursively crawl the pages

        Args:
            url (string): starting url
            n (int): max. number of pages to be crawled
        """
        if len(self.crawled_list) == n:
            return
        Info = page(url)
        if url in self.crawled_list:
            #If the page is updated, then replace the old with new
            #if modDate > self.get_by_url(url).last_mod_date:
            if self.get_by_url(url) < Info:
                Info.wordfreq(Info.stopstem(url, Info.title), 't')
                Info.wordfreq(Info.stopstem(url, Info.body), 'b')
                idx = self.get_idx_by_url(url)
                self.HTML_list[idx] = Info.deep_copy()
                for link in Info.link_queue:
                    self.crawl(link, n)
            else:
                pass
        else:
            Info.wordfreq(Info.stopstem(url, Info.title), 't')
            Info.wordfreq(Info.stopstem(url, Info.body), 'b')
            self.crawled_list.add(url)
            self.HTML_list.append(Info)
            for link in Info.link_queue:
                self.crawl(link, n)

    def get_by_url(self, url): # retrieve from html list by url
        try:
            for html in self.HTML_list:
                if html.url == url:
                    return html
        except:
            print("Error, not an actual URL")
            return page()
    
    def get_idx_by_url(self, url):
        idx = 0
        try:
            for i, html in enumerate(self.HTML_list):
                if html.url == url:
                    return i
        except:
            return -1
         
    # Export search results as "spider-result.txt"
    def export(self, mode):
        """ Export by print or by storing into "spider-result.txt"

        Args:
            mode (_string_): _"print"/"return": print is print, return is .txt file_
        """
        with open("spider_result.txt", "w", encoding="utf-8") as f:
            for i, page in enumerate(self.HTML_list):
                #f.write(f"Index: {i}\n")
                f.write(repr(page))
    
    # output the search result with page's display function, will be modified to output to a text file
    def test(self):
        for page in self.HTML_list:
            print(repr(page))
        print(f"Web crawling finished, {len(self.HTML_list)} results found.")


    def createdb(self, filename):
        """ Create the .db file for storing pages newly fetched pages OR Clean an existing .db file to store newly fetched pages.
            2 mapping tables and 2 indexing tables will be created. 
            filename (string): filename/filepath of the .db file. It will create one if the file did not exist.
        """
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        
        # Drop table if exist
        cursor.execute('DROP TABLE IF EXISTS forward_index')
        cursor.execute('DROP TABLE IF EXISTS inverted_index')
        cursor.execute('DROP TABLE IF EXISTS forward_title_index')
        cursor.execute('DROP TABLE IF EXISTS inverted_title_index')
        cursor.execute('DROP TABLE IF EXISTS content')
        cursor.execute('DROP TABLE IF EXISTS urls')
        cursor.execute('DROP TABLE IF EXISTS words')

        # 1st table: forward_index(page_id, word_freq)
        cursor.execute("""CREATE TABLE forward_index(
                       page_id INTEGER PRIMARY KEY,
                       word_freq TEXT
        )""")

        # 2nd table: inverted_index(page_id, page_freq)
        cursor.execute("""CREATE TABLE inverted_index(
                       word_id INTEGER PRIMARY KEY,
                       page_freq TEXT
        )""")

        # 3rd table: forward_title_index(page_id, word_freq)
        cursor.execute("""CREATE TABLE forward_title_index(
                       page_id INTEGER PRIMARY KEY,
                       word_freq TEXT
        )""")

        # 4th table: inverted_title_index(page_id, page_freq)
        cursor.execute("""CREATE TABLE inverted_title_index(
                       word_id INTEGER PRIMARY KEY,
                       page_freq TEXT
        )""")

        # 5th table: content(page_id, url, pagetitle, last_mod_date, file_size, child_link, parent_link)
        cursor.execute("""CREATE TABLE content(
                       page_id INTEGER,
                       url TEXT,
                       pagetitle TEXT,
                       last_mod_date DATETIME,
                       file_size INTEGER,
                       child_link TEXT,
                       parent_link TEXT
        )""")

        # 1st mapping table: urls(url, page_id, last_mod_date)
        cursor.execute("""CREATE TABLE urls(
                       url TEXT PRIMARY KEY,
                       page_id INTEGER
        )""")

        # 2nd mapping table: words(word, word_id)
        cursor.execute("""CREATE TABLE words(
                       word TEXT PRIMARY KEY,
                       word_id INTEGER
        )""")

    def dbforward(self, filename):
        """ Insert to a db file by new data crawled in the class (HTML_list)
        This function also supports data update for whenever there is a newer mod_date
            Database tables involved:
            - urls
            - content
            - forward_index
            - forward_title_index
        """
        connection = sqlite3.connect(filename)
        c1 = connection.cursor()
        c2 = connection.cursor()
        for page in self.HTML_list:

            # Check if URL already exists
            c1.execute("SELECT page_id FROM urls WHERE url=?", (page.url,))
            if c1.fetchone():
                c2.execute("SELECT last_mod_date FROM content WHERE page_id=?", (page.url))
                new_last_mod_date = page.last_mod_date
                old_last_mod_date = c2.fetchone()[0]
                if new_last_mod_date > old_last_mod_date:               # Update new value if (new_last_mod_date > old_last_mod_date)
                    page_id = c1.fetchone()[0]
                    last_mod_date = dateutil.parser.parse(page.last_mod_date).strftime('%Y-%m-%d %H:%M:%S')
                    c2.execute("UPDATE forward_index SET word_freq = (?) WHERE page_id = (?)", (json.dumps(page.keyword_counts), page_id))      # NOT SURE WHETHER THIS CODE IS CORRECT
                    c2.execute("UPDATE forward_title_index SET word_freq = (?) WHERE page_id = (?)", (json.dumps(page.page_title_kword), page_id))      # NOT SURE WHETHER THIS CODE IS CORRECT
                    c1.execute("UPDATE content SET pagetitle = (?), last_mod_date = (?), file_size = (?), child_link = (?), parent_link = (?) WHERE page_id = (?)",
                               (page.title, last_mod_date, page.file_size, json.dumps(page.child_link), json.dumps(page.parent_link), page_id))
                else:
                    continue
            # url does not exists, assign a new page_id and insert data into database file
            c2.execute("SELECT COUNT(*) FROM urls")
            new_page_id = c2.fetchone()[0] + 1
            last_mod_date = dateutil.parser.parse(page.last_mod_date).strftime('%Y-%m-%d %H:%M:%S')
            c1.execute("INSERT INTO urls VALUES (?,?)",(page.url, new_page_id))
            c2.execute("INSERT INTO forward_index VALUES (?,?)", (new_page_id, json.dumps(page.keyword_counts)))
            c2.execute("INSERT INTO forward_title_index VALUES (?,?)", (new_page_id, json.dumps(page.page_title_kword)))
            c1.execute("INSERT INTO content VALUES (?,?,?,?,?,?,?)",
                       (new_page_id, page.url, page.title, last_mod_date, page.file_size, json.dumps(page.child_link), json.dumps(page.parent_link)))
        connection.commit()
        connection.close()
        
    def dbinverted(self, filename):
        """Calculate the inverted index and put it into database. dbforward() must be runned before dbinverted()
           THIS FUNCTION DOES NOT SUPPORT UPDATING INVERTED INDEX YET
           Database tables involved:
            - forward_index (data extraction only)
            - forward_title_index (data extraction only)
            - words
            - inverted_index
             -inverted_title_index
        """

        # Getting data for inverting indexes and assigning/matching word_id
        connection = sqlite3.connect(filename)
        c1 = connection.cursor()                                # c1 is handling page bodies keywords
        c2 = connection.cursor()                                # c2 is handling page titles keywords
        c3 = connection.cursor()                                # c3 is handling table 'words'
        c1.execute("SELECT * FROM forward_index")
        c2.execute("SELECT * FROM forward_title_index")
        c3.execute("SELECT * FROM words")
        results_bodies = c1.fetchall()
        results_titles = c2.fetchall()
        Word_Freq_Bodies = {}
        Word_Freq_Titles = {}
        words = c3.fetchall()
        Word_Id = {}
        New_Word_Id = {}
        for word in words:
            Word_Id[word[0]] = word[1]                          # word[0] is the word itself; word[1] is the word id
        
        # For page body
        for page in results_bodies:
            page_id = page[0]
            word_freq = json.loads(page[1])
            for word, freq in word_freq.items():
                if word in Word_Id.keys():  # If word already exists in the database table "words"
                    word_id = Word_Id[word]  # Getting word id of a word
                    if word_id in Word_Freq_Bodies:
                        Word_Freq_Bodies[word_id][page_id] = freq  # Update the existing value
                    else:
                        Word_Freq_Bodies[word_id] = {page_id: freq}  # Create a new item for dictionary (Word_Freq_Bodies) to store the word frequency of a new page
                else:  # If word does not exist in the database table "words"
                    new_word_id = len(Word_Id) + 1  # Assign new_word_id to the new word introduced
                    New_Word_Id[word] = Word_Id[word] = new_word_id  # Create a new item for table "words"
                    Word_Freq_Bodies[new_word_id] = {page_id: freq}  # Create a new item for dictionary (Word_Freq_Bodies) to store the word frequency of a page

        # For page title
        for page in results_titles:
            page_id = page[0]
            word_freq = json.loads(page[1])
            for word, freq in word_freq.items():
                if word in Word_Id.keys():  # If word already exists in the database table "words"
                    word_id = Word_Id[word]  # Getting word id of a word
                    if word_id in Word_Freq_Titles:
                        Word_Freq_Titles[word_id][page_id] = freq  # Update the existing value
                    else:
                        Word_Freq_Titles[word_id] = {page_id: freq}  # Create a new item for dictionary (Word_Freq_Bodies) to store the word frequency of a new page
                else:  # If word does not exist in the database table "words"
                    new_word_id = len(Word_Id) + 1  # Assign new_word_id to the new word introduced
                    New_Word_Id[word] = Word_Id[word] = new_word_id  # Create a new item for table "words"
                    Word_Freq_Titles[new_word_id] = {page_id: freq}  # Create a new item for dictionary (Word_Freq_Bodies) to store the word frequency of a page        

        # Inserting the dictionaries into tables
        for word, word_id in New_Word_Id.items():
            c1.execute("INSERT INTO words VALUES (?,?)", (word, word_id))
        for word_id, page_freq in Word_Freq_Bodies.items():
            c1.execute("INSERT INTO inverted_index VALUES (?,?) ON CONFLICT (word_id) DO UPDATE SET word_id = excluded.word_id", 
                       (word_id, json.dumps(page_freq)))
        for word_id, page_freq in Word_Freq_Titles.items():
            c1.execute("INSERT INTO inverted_title_index VALUES (?,?) ON CONFLICT (word_id) DO UPDATE SET word_id = excluded.word_id", 
                       (word_id, json.dumps(page_freq)))            
        connection.commit()
        connection.close()

    def fileretrieve(self, filename, url = None, page_ids = None):
        """ Get the information of an url from the database from generating the pages

        Args:
            filename (string): filename/filepath
            url (string): the url of the page you want to fetch 
            page_ids (list): list of string of page_id of pages we want to display in the search result

        Returns:
            page_title ():
        """
        connection = sqlite3.connect(filename)
        c1 = connection.cursor()
        if (page_ids == None and url == None) or (page_ids == True and url == True):
            TypeError(r"Either only 'url' or only 'page_id' is inputted into function parameter")
            pass
        if url == True:
            qs = "(" + ",".join("?" * len(url)) + ")"
            c1.execute(f"SELECT page_id FROM urls WHERE url={qs}", (url,))
            page_ids = c1.fetchone()
        
        result = {}
        HTML_list_object = HTML_list()

        for page_id in page_ids:
            c1.execute("SELECT * FROM content WHERE page_id=?", (page_id,))
            content = c1.fetchone()
            if content:
                url = content[1]
                page_title = content[2]
                last_mod_date = content[3]
                file_size = content[4]
                child_link = json.loads(content[5])
                parent_link = json.loads(content[6])

                c1.execute("SELECT word_freq FROM forward_index WHERE page_id=?", (page_id,))
                word_freq = json.loads(c1.fetchone()[0])
                result[page_id] = (page_title, last_mod_date, file_size, word_freq, child_link, parent_link)
                temppage = page()
                temppage.title = page_title
                temppage.last_mod_date = last_mod_date
                temppage.file_size = file_size
                temppage.keyword_counts = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
                temppage.url = url
                temppage.child_link = child_link
                temppage.parent_link = parent_link
                HTML_list_object.HTML_list.append(temppage)
        connection.close()

        return result, HTML_list_object
        

    def queryretrieve(self, filename, query):
        f"""Retrieve the inverted index of query terms from {filename} and output a 2D array ready for cosine similarity processing

        Args:
            filename (string): filename/filepath
            query (list): list of strings (query terms)

        Returns:
            _2Darray_: Posting list for cosine similarity processing
        """
        # Format preparation before sending the query into .db file
        connection = sqlite3.connect(filename)
        c1 = connection.cursor()
        qs = "(" + ",".join("?" * len(query)) + ")"
        query = tuple(query)

        # Search up the word_id of the words
        c1.execute(f'''SELECT word_id FROM words WHERE word IN {qs} AND NOT '' ''', (query))
        word_ids = c1.fetchall()
        qs = "(" + ",".join("?" * len(word_ids)) + ")"          # Refresh another (?,?,...) as there might be words that is not in the database. The count has to be changed.

        # Process the output word_id as it is in the format of tuple
        word_ids = tuple(word_id for inner_tuple in word_ids for word_id in inner_tuple)

        # Fetch posting lists for page bodies
        c1.execute(f'''SELECT * FROM inverted_index WHERE word_id IN {qs}''', (word_ids))
        postingslistbodies = c1.fetchall() 

        # Fetch posting lists for page bodies
        c1.execute(f'''SELECT * FROM inverted_title_index WHERE word_id IN {qs}''', (word_ids))
        postingslisttitles = c1.fetchall()                                                          # Non-processed output

        connection.close()
        return postingslistbodies, postingslisttitles, word_ids


    def vector_space(self, filename, postingslistbodies, postingslisttitles, query_word_ids):
        """Generate Vector Space for both pages' bodies and titles

        Args:
            filename (string): filename/filepath
            postingslistbodies (_tuple_): posting list of page bodies extracted from queryretrieve()
            postingslisttitles (_tuple_): posting list of page titles extracted from queryretrieve()
            query_word_ids (_list_): the list of query terms

        Returns:
            _dictionary_: Vector Space Model: dict_key is page_id, dict_values is a weighted_vector (list of weighted_terms) of each page 
        """
        # Term Weighting of terms in bodies
        connection = sqlite3.connect(filename)
        c1 = connection.cursor()
        c1.execute('''SELECT COUNT(*) FROM urls''')
        N = c1.fetchone()                                                       # N is the number of documents/pages in collectioin
        N = N[0]

        vector_dim = len(query_word_ids)

        # Weigted Vectors in page bodies
        weighted_vector_bodies = {}                                             # A dictionary containing keys of page id, and query term weighting
        for word_id, tf_dict in postingslistbodies:                             # For each word (word_id) of the query
            tf_dict = json.loads(tf_dict)
            df = len(tf_dict)
            idf = np.log2(N/df)
            tf_max = max(tf_dict.values())
            for page_id, tf in tf_dict.items():                                         # For each page (page_id) of the word
                term_weighting = tf * idf / tf_max
                if page_id not in weighted_vector_bodies.keys():
                    weighted_vector_bodies[page_id] = [0] * vector_dim
                weighted_vector_bodies[page_id][query_word_ids.index(word_id)] = term_weighting

        # Weigted Vectors in page titles
        weighted_vector_titles = {}                                             # A dictionary containing keys of page id, and query term weighting
        for word_id, tf_dict in postingslisttitles:                             # For each word (word_id) of the query
            tf_dict = json.loads(tf_dict)
            df = len(tf_dict)
            idf = np.log2(N/df)
            tf_max = max(tf_dict.values())
            for page_id, tf in tf_dict.items():                                         # For each page (page_id) of the word
                term_weighting = tf * idf / tf_max
                if page_id not in weighted_vector_titles.keys():
                    weighted_vector_titles[page_id] = [0] * vector_dim
                weighted_vector_titles[page_id][query_word_ids.index(word_id)] = term_weighting

        connection.close()
        return weighted_vector_bodies, weighted_vector_titles
    
    def cossim(self, weighted_vector_bodies, weighted_vector_titles, query, query_weights=None):
        """Calculating the cosine similarity between each page and the query. 

        Args:
            weight_vector_bodies (_dict_): key is page_id, value is weighted_vector (list of terms weighting)
            weighted_vector_titles (_type_):  key is page_id, value is weighted_vector (list of terms weighting)
            query (list): list of query term (words, not word_id)
            query_weights (list, optional): Weighting of each individual term. Defaults to None.

        Returns:
            dictionary: Similarity scores between the query and each document. dict_key is page_id (STRING), dict_values is a similarity score
        """    
        vector_dim = len(next(iter(weighted_vector_bodies.values())))
        
        if query_weights == None:
            query_weights = np.ones(vector_dim)
        query_vector = query_weights
    
        # Bodies
        bodies_scores = {}
        for page_id, vector in weighted_vector_bodies.items():
            dot_product = np.dot(vector, query_vector)
            norm_vector = np.linalg.norm(vector)
            norm_query_vector = np.linalg.norm(query_vector)
            similarity = dot_product / (norm_vector * norm_query_vector)
            if page_id not in bodies_scores.keys():
                bodies_scores[page_id] = 0
            bodies_scores[page_id] += similarity
        # For returning sorted dictionary
        bodies_scores = {k: v for k, v in sorted(bodies_scores.items(), key = lambda x: x[1], reverse = True)}
        
        # Titles
        titles_scores = {}
        
        for page_id, vector in weighted_vector_titles.items():
            dot_product = np.dot(vector, query_vector)
            norm_vector = np.linalg.norm(vector)
            norm_query_vector = np.linalg.norm(query_vector)
            similarity = dot_product / (norm_vector * norm_query_vector)
            if page_id not in titles_scores.keys():
                titles_scores[page_id] = 0
            titles_scores[page_id] += similarity
        # For returning sorted dictionary
        titles_scores = {k: v for k, v in sorted(titles_scores.items(), key = lambda x: x[1], reverse = True)}
        all_page_ids = set(bodies_scores.keys()) | set(titles_scores.keys())
        combined_scores = {}
        for page_id in all_page_ids:
            body_score = bodies_scores.get(page_id, 0)
            title_score = titles_scores.get(page_id, 0)
            combined_score = (body_score * 1 + title_score * 24) / 25
            combined_scores[int(page_id)] = combined_score
        combined_scores = dict(sorted(combined_scores.items(), key=lambda x: x[1], reverse=True))
        return combined_scores

    def retrieve(self, filename, query, query_weights = None):
        """Calculating the similarity score of related pages and query based on cosine similarity and tf/idf

        Args:
            filename (string): filename/filepath
            query (list): the list of query terms 
            query_weights (list, optional): Weighting of each individual term. Defaults to None.

        Returns:
            dictionary: a dictionary of similarity scores. keys are 'page_id', values are scores. (Sorted in descending order of values.)
        """
        postingslistbodies, postingslisttitles, query_word_ids = self.queryretrieve(filename, query)
        weighted_vector_bodies, weighted_vector_titles = self.vector_space(filename, postingslistbodies, postingslisttitles, query_word_ids)
        scores = self.cossim(weighted_vector_bodies, weighted_vector_titles, query, query_weights)
        return scores
