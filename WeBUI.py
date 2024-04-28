from flask import Flask, render_template, request
import re
from scraper import page, HTML_list

app = Flask(__name__)
spider = HTML_list()

def calculate_pagerank(web_graph, damping_factor=0.85, max_iterations=100, epsilon=1e-8):
    num_pages = len(web_graph)
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

# Home page
@app.route('/')
def home():
    spider.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 300)
    filename = "indexertest.db"
    spider.createdb(filename)
    spider.dbforward(filename)
    spider.dbinverted(filename)

    return render_template('index.html')

# Search page
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    log_query(query) # query is logged

    # Page Rank the Spider.HTML
    web_graph = spider.create_web_graph()
    pr = calculate_pagerank(web_graph)
    sorted_list = spider.HTML_list
    sorted_links = sorted(spider.HTML_list, key=lambda obj: pr[obj.url], reverse=True)
    
    #sorting/ranking operation
    spider.export('return')
    #with open("spider_result.txt", 'r', encoding="utf-8") as file:
    #    content = file.read()
    #with open(r"spider_result.txt", "r", encoding="utf-8") as file:
    count = 297 #int(len(file.readlines())/7)
    #content_with_links = re.sub(r'(https?://\S+)', r'<a href="\1">\1</a>', content)
    # Render search results
    return render_template('results.html', content=sorted_list, query=query, numOfPage=count)

if __name__ == '__main__':
    app.run(debug=True)