from flask import Flask, render_template, request, redirect
import os
from scraper import page, HTML_list
import datetime
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

app = Flask(__name__)
spider = HTML_list()
FILENAME = "indexertest.db"

def calculate_pagerank(web_graph, damping_factor=0.85, max_iterations=100, epsilon=1e-8):
    num_pages = len(web_graph) + 1
    initial_score = 1.0 / num_pages
    pagerank = {page: initial_score for page in web_graph}
    outgoing_links = {page: len(links) for page, links in web_graph.items() if links}

    for _ in range(max_iterations):
        new_pagerank = {}

        for page in web_graph:
            new_score = (1 - damping_factor) / num_pages

            for incoming_page, links in web_graph.items():
                if page in links:
                    new_score += damping_factor * pagerank[incoming_page] / outgoing_links[incoming_page]

            new_pagerank[page] = new_score

        # Check convergence
        diff = sum(abs(pagerank[page] - new_pagerank[page]) for page in web_graph)
        if diff < epsilon:
            break

        pagerank = new_pagerank

    return pagerank

def log_query(query):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("query_log.txt", "a") as f:
        f.write(f"{timestamp}: {query}\n")

def stopstem(text): # stemming and stopword removal
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
    return stemmed
# Home page
@app.route('/')
def home():
    spider.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 300)

    spider.createdb(FILENAME)
    spider.dbforward(FILENAME)
    spider.dbinverted(FILENAME)

    return render_template('index.html')

# Search page
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    log_query(query) # query is logged
    query_refined = stopstem(query)

    #sort by similarity
    scores = spider.retrieve(FILENAME, query_refined)
    _, HTML_list_object = spider.fileretrieve(FILENAME, page_ids=scores.keys())

    # Page Rank the Spider.HTML
    #web_graph = spider.create_web_graph()
    #pr = calculate_pagerank(web_graph)
    #sorted_list = spider.HTML_list
    #sorted_links = sorted(spider.HTML_list, key=lambda obj: pr[obj.url], reverse=True)
    
    #sorting/ranking operation

    count = len(HTML_list_object.HTML_list) 

    # Render search results
    return render_template('test1.html', search_results=HTML_list_object.HTML_list, count=count, query=query)

# Previous Query
@app.route('/previous_queries')
def get_previous_queries():
    with open('query_log.txt', 'r') as file:
        queries = file.readlines()
        dates = []

        for i, query in enumerate(queries):
            queries[i] = query[21:]
            dates.append(query[0:20])
        return render_template('previous_queries.html', array=zip(dates, queries))

@app.route('/clear_queries', methods=['POST'])
def clear_queries():
    # Specify the path to the text file
    file_path = "query_log.txt"

    # decide which mode (clear all or specific item)
    try:
        print(request.form['query_index'])
        query_index = int(request.form['query_index'])
    except:
        query_index = -1 #Clear all mode

    # Check if the file exists
    if os.path.exists(file_path):

        # Clear the content of the file by opening it in write mode
        with open(file_path, 'w') as f:
            f.truncate(0)  # This truncates the file to 0 bytes

    # Redirect to the previous queries page or any other desired page
    return redirect('/previous_queries')

@app.route('/clear_query', methods=['POST'])
def clear_query():    
    # Specify the path to the text file
    file_path = "query_log.txt"
    # decide which mode (clear all or specific item)
    query_index = int(request.form['query_index'])

    print(query_index)
    # Check if the file exists
    if os.path.exists(file_path):

            with open(file_path, 'r') as f:
                lines = f.readlines()

        # Remove the line at the specified index
            if 0 <= query_index < len(lines):
                del lines[query_index]

        # Write the updated lines back to the file
            with open(file_path, 'w') as f:
                f.writelines(lines)

    # Redirect to the previous queries page or any other desired page
    return redirect('/previous_queries')
    
if __name__ == '__main__':
    app.run(debug=True)