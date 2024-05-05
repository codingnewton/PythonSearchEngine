from scraper import HTML_list

def main():
    # Initialize the HTML_list object
    spider = HTML_list()

    # Start the web crawling process
    spider.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm", 300)

    filename = "indexertest.db"

    # Create the SQLite database
    spider.createdb(filename)

    # Perform forward indexing
    spider.dbforward(filename)

    # Perform inverted indexing
    spider.dbinverted(filename)

    query = ['comput', 'part', 'document', 'final']
    scores = spider.retrieve(filename, query)
    result, HTML_list_object = spider.fileretrieve(filename, page_ids=scores.keys())
    print(result)
    HTML_list_object.export("print")


    # Export the search results to a text file
    spider.export('return')

if __name__ == "__main__":
    main()
