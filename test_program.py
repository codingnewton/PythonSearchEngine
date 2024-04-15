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

    # Retrieve content of the database table
    # spider.dbtest(filename, tablename)

    # Export the search results to a text file
    spider.export('return')

if __name__ == "__main__":
    main()
