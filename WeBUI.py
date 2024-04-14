from flask import Flask, render_template, request

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Search page
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    with open("spider_result.txt", 'r') as file:
        content = file.read()
    # Perform search operations here
    
    # Render search results
    return render_template('results.html', content=content, query=query)

if __name__ == '__main__':
    app.run(debug=True)