import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import io
import sqlite3
import json
nltk.download('punkt')
import copy

class page:
    crawled_url = set()
    def __init__(self):
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
    

    def __init__(self, url): # The scraping process
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
        full_links = [urljoin(response.url, link) for link in links]
        self.link_queue = [full_link for full_link in full_links]
        url_cleaned = response.url.split(".htm")[0].strip()

        for link in full_links:
            if link.startswith(url_cleaned):
                if len(self.child_link) <=10:
                    self.child_link.append(link)
                else:
                    pass
            if response.url.startswith(link.split(".htm")[0].strip()):
                self.parent_link.append(link)


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

    def sortwordfreq(self):                                             # For later use
        keyword_counts = self.keyword_counts
        sorted_keyword_counts = sorted(keyword_counts.items, key = lambda x:x[1], reverse = True)
        self.keyword_counts = dict(sorted_keyword_counts)
        pass
    
    def deep_copy(self):
        return copy.deepcopy(self)

    def display(self, mode):
        """ Output crawl result by printing or returning

        Args:
            mode (String): "print"/"return". Print will print the function 

        Returns:
            String: return crawl result if the mode is "return"
        """
        if mode == 'print':
            print(f"Page Title: {self.title}")
            print(f"URL: {self.url}")
            print(f"Last modification date: {self.last_mod_date} | Size of Page: {self.file_size}Bytes")
            print(f"Keyword frequency: {self.returnwordfreq(10)}")
            print(f"Child Links: {self.child_link[:10]}")
            print(f"Parent Links: {self.parent_link}")
            print("-------------------------------------------------------------------")
            pass
        elif mode == 'return':
            pagetitle = f"Page Title: {self.title}\n" 
            url = f"URL: {self.url}\n"
            modidate = f"Last modification date: {self.last_mod_date} | Size of Page: {self.file_size}Bytes\n"
            keyfreq = f"Keyword frequency: {self.returnwordfreq(10)}\n"
            childlink = f"Child Links: {self.child_link[:10]}\n"
            parentlink = f"Parent Links: {self.parent_link}\n"
            hypens = "-------------------------------------------------------------------\n"
            return pagetitle + url + modidate + keyfreq + childlink + parentlink + hypens
    

class HTML_list:
    crawled_list = set()

    def __init__(self):
       self.HTML_list = [] # list of page for later sorting

    def get_object_at(self, idx):
        try: 
            return self.HTML_list[idx]
        except:
            print("Error: Invalid argument")
            return 0
    
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
            modDate = requests.get(url).headers.get('last-modified')
            if modDate > self.get_by_url(url).last_mod_date:
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
            for html in self.HTML_list:
                if html.url == url:
                    return idx
                else:
                    idx = idx+1
        except:
            return -1


    # sort the HTML list by index
    def HTMLlist_sort(self):
        pass            
    
    # Export search results as "spider-result.txt"
    def export(self, mode):
        """ Export by print or by storing into "spider-result.txt"

        Args:
            mode (_string_): _"print"/"return": print is print, return is .txt file_
        """
        with open("spider-result.txt", "w") as f:
            for page in self.HTML_list:
                f.write(page.display('return'))
    
    # output the search result with page's display function, will be modified to output to a text file
    def test(self):
        for page in self.HTML_list:
            page.display('print')
        print(f"Web crawling finished, {len(self.HTML_list)} results found.")


    def createdb(self):
        connection = sqlite3.connect('indexer.db')
        cursor = connection.cursor()
        
        # Drop table if exist
        cursor.execute('DROP TABLE IF EXISTS pages')
        cursor.execute('DROP TABLE IF EXISTS forward_index')
        cursor.execute('DROP TABLE IF EXISTS inverted_index')
        cursor.execute('DROP TABLE IF EXISTS urls')
        cursor.execute('DROP TABLE IF EXISTS words')


        # self.title = ""
        # self.body = ""
        # self.url = ""
        # self.last_mod_date = ""
        # self.file_size = 0
        # self.kw_freq = [] # This should be an array or set of tuples
        # self.child_link = []
        # self.parent_link = []
        # self.link_queue = []
        # self.stemmed = []
        # self.keyword_counts = {} # wordfreq() has to be executed to store this
        # self.page_title_kword = {}

        # # 1st table: pages(page_id, url, content)
        # cursor.execute("""CREATE TABLE pages (
        #                page_id INTEGER PRIMARY KEY,
        #                url TEXT,
        #                content TEXT
        # )""")

        # 1st table: forward_index(page_id, word_freq)
        cursor.execute("""CREATE TABLE forward_index(
                       page_id INTEGER,
                       word_freq TEXT
        )""")

        # 2nd table: inverted_index(page_id, page_freq) WRONG ATTRIBUTE ASSIGNMENT, PLEASE AMMEND
        cursor.execute("""CREATE TABLE inverted_index(
                       word_id INTEGER,
                       page_freq TEXT
        )""")

        # 1st mapping table: urls(url, page_id)
        cursor.execute("""CREATE TABLE urls(
                       url TEXT PRIMARY KEY,
                       page_id INTEGER
        )""")

        # 2nd mapping table: words(word, word_id)
        cursor.execute("""CREATE TABLE words(
                       word TEXT PRIMARY KEY,
                       word_id INTEGER
        )""")

    def dbforward(self):
        """ Insert to a db file by data crawled in the class (HTML_list)
        """
        connection = sqlite3.connect('indexer.db')
        c1 = connection.cursor()
        c2 = connection.cursor()

        for page in self.HTML_list:
            # Check if URL already exists
            c1.execute("SELECT page_id FROM urls WHERE url=?", (page.url,))
            if not(c1.fetchone()):
                # url does not exists, assign a new page_id
                c2.execute("SELECT COUNT(*) FROM urls")
                new_page_id = c2.fetchone()[0] + 1
                c1.execute("INSERT INTO urls VALUES (?,?)",(page.url, new_page_id))
                c2.execute("INSERT INTO forward_index VALUES (?,?)", (new_page_id, json.dumps(page.keyword_counts)))
        connection.commit()
        connection.close()
        
    def dbinverted(self):
        """Calculate the inverted index and put it into database. dbforward() must be runned before dbinverted()
        """
        connection = sqlite3.connect('indexer.db')
        c1 = connection.cursor()
        c1.execute("SELECT * FROM forward_index")
        results = c1.fetchall()
        Word_Freq = {}
        Word_Id = {}
        for page in results:
            page_id = page[0]
            word_freq = json.loads(page[1])
            for word, freq in word_freq.items():
                if word in Word_Id.keys():
                    word_id = Word_Id[word]                     # Getting word id of a word
                    Word_Freq[word_id][page_id] = freq          # Create a new item for dictionary (page_freq) to store the word frequency of a new page
                else:
                    pages_freq = {}                             # Create a dictionary to store the word frequency of pages (page_freq)
                    Word_Id[word] = len(Word_Id) + 1            # Create a new item for table words 
                    pages_freq[page_id] = freq                  # Create a new item for dictionary (page_freq) to store the word frequency of a page
                    Word_Freq[Word_Id[word]] = pages_freq  
     
        # Inserting the dictionaries into tables
        for word, word_id in Word_Id.items():
            c1.execute("INSERT INTO words VALUES (?,?)", (word, word_id))
        for word_id, page_freq in Word_Freq.items():
            c1.execute("INSERT INTO inverted_index VALUES (?,?)", (word_id, json.dumps(page_freq)))
        connection.commit()
        connection.close()

    def dbtest(self):
        connection = sqlite3.connect('indexer.db')
        c1 = connection.cursor()
        c1.execute("SELECT * FROM inverted_index")
        words = c1.fetchall()
        for word in words:
            print(word[1])
            #print(type(word[1]))
            #print(json.loads(word[1]))
            #print(type(json.loads(word[1])))


# Testing the crawler
A = HTML_list()
A.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)

# Testing db file creation
A.createdb()
A.dbforward()       # Forward indexing
A.dbinverted()      # Creating Inverted Index. dbforward() must be runned before this.
A.dbtest()          # Retrieve contents of db file.

A.export('return')
# A.test()


# When you would like to store a dictionary to a db table
# You have to make it a string first by json.dumps(_dict_)
# When you would like to get a dictionary from a db table
# You have to make it a dictionary first by json.loads(_string_)
