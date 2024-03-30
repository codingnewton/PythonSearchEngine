import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# import nltk
from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import io
import sqlite3
# nltk.download('stopwords')

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
       self.HTML_list = [] # list of HTMLobj for later sorting

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
        if url in self.crawled_list:
            pass
        else:
            Info = HTMLobj(url)
            Info.wordfreq(Info.stopstem(url, Info.title), 't')
            Info.wordfreq(Info.stopstem(url, Info.body), 'b')
            self.crawled_list.add(url)
            self.HTML_list.append(Info)
            for link in Info.link_queue:
                self.crawl(link, n)
    
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
    
    # output the search result with HTMLobj's display function, will be modified to output to a text file
    def test(self):
        for page in self.HTML_list:
            page.display('print')
        print(f"Web crawling finished, {len(self.HTML_list)} results found.")


# Testing the crawler
A = HTML_list()
A.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 30)
A.export('return')
# A.test()