# This is a scraper method that scrape most neccessary information from each html
#!apt-get install -y gdbm
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#import dbm.gnu as gdbm
import io
import sqlite3
nltk.download('stopwords')


class HTMLobj:
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

    def __init__(self, url): # The scraping process
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        self.body = soup.find('body').get_text()
        self.child_link = []
        self.parent_link = []
        self.stemmed = []
        self.keyword_counts = {}
        
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
                self.child_link.append(link)
            if response.url.startswith(link.split(".htm")[0].strip()):
                self.parent_link.append(link)


    def stopstem(self, url):
        stemmer = PorterStemmer()
        text = self.body
        words = word_tokenize(text)                                     # Tokenizing
        punct = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        for word in words:
            if word in punct:
                words.remove(word)
                continue
            elif word in stopwords.words():                             # Stopword Removal
                words.remove(word)
                continue
        stemmed = [stemmer.stem(word) for word in words]
        '''if mode == 'body':
          self.stemmed = stemmed
        else:
          self.page_title_kword = stemmed'''
        
        return stemmed

    def wordfreq(self, stemmed):
        keyword_counts = {}
        # Increment count for this keyword
        for word in stemmed:
            keyword_counts[word] = keyword_counts.get(word, 0) + 1
        self.keyword_counts = keyword_counts
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

    def display(self):
        print(f"Page Title: {self.title}")
        print(f"URL: {self.url}")
        print(f"Last modification date: {self.last_mod_date} | Size of Page: {self.file_size}B")
        print(f"Keyword frequency: {self.returnwordfreq(10)}")
        print(f"Child Links: {self.child_link[:10]}")
        print(f"Parent Links: {self.parent_link[:10]}")
        print("-------------------------------------------------------------------")
    

class HTML_list:
    crawled_list = set()
    MAX = 30

    def __init__(self):
       self.HTML_list = [] # list of HTMLobj for later sorting

    def get_object_at(self, idx):
        try: 
            return self.HTML_list[idx]
        except:
            print("Error: Invalid argument")
            return 0
    
    def crawl(self, url, pages):
        """ Recursively Crawl all the information of a webpage

        Args:
            url (string): the starting url
            pages (int): number of pages to be crawl
        """
        if len(self.crawled_list) == pages:
            return
        if url in self.crawled_list:
            pass
        else:
            Info = HTMLobj(url)
            Info.wordfreq(Info.stopstem(url))
            self.crawled_list.add(url)
            self.HTML_list.append(Info)
            for link in Info.link_queue:
                self.crawl(link, pages)
    
    # sort the HTML list by index
    def sort_by_index():
        print("Placeholder: Sort by index")
    
    # output the search result with HTMLobj's display function, will be modified to output to a text file
    def export(self):
        for page in self.HTML_list:
            page.display()
        print(f"Web crawling finished, {len(self.HTML_list)} results found.")

def dbfile(input):
    # Step 1: Create a new database file
    connection = sqlite3.connect('mydatabase.db')

    # Step 2: Create a cursor object
    cursor = connection.cursor()

    # Step 3: Define a table structure (optional)
    create_table_query = '''
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
    )
    '''

    cursor.execute(create_table_query)

    # Step 4: Insert data into the table
    insert_data_query = '''
    INSERT INTO users (id, name, email, password) VALUES
        (1, 'John Doe', 'johndoe@example.com'),
        (2, 'Jane Smith', 'janesmith@example.com'),
        (3, 'Alice Johnson', 'alicejohnson@example.com')
    '''
    cursor.execute(insert_data_query)

    # Step 5: Commit the changes
    connection.commit()

    # Step 6: Query the data
    select_data_query = 'SELECT * FROM users'
    cursor.execute(select_data_query)
    rows = cursor.fetchall()

    # Step 7: Print the queried data
    for row in rows:
        print(row)

    # Step 8: Close the connection
    connection.close()

# Testing the crawler
A = HTML_list()
A.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)
A.export()