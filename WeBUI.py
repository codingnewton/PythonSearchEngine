from flask import Flask, render_template, request
import re
from scraper import page, HTML_list

app = Flask(__name__)
spider = HTML_list()
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
    #sorting/ranking operation
    spider.export('return')
    with open("spider_result.txt", 'r', encoding="utf-8") as file:
        content = file.read()
    with open(r"spider_result.txt", "r", encoding="utf-8") as file:
        count = int(len(file.readlines())/7)
    # Perform search operations here
    content_with_links = re.sub(r'(https?://\S+)', r'<a href="\1">\1</a>', content)
    # Render search results
    return render_template('results.html', content=content_with_links, query=query, numOfPage=count)

if __name__ == '__main__':
    app.run(debug=True)