from scraper import HTML_list

def main():
    # Initialize the HTML_list object
    spider = HTML_list()

    filename = "indexertest.db"

    # # Perform forward indexing
    # spider.dbforward(filename)

    # # Perform inverted indexing
    # spider.dbinverted(filename)≠

    print(spider.dbtemptest(filename, range(1,100)))
    # spider.dbtest(filename, 'inverted_index')

    postingslistbodies, postingslisttitles = spider.queryretrieve(filename, ['comput', 'part', 'document', 'final'])
    print(f"Postings List of page body: {postingslistbodies}\nPostings List of page title: {postingslisttitles}")
    
    # Export the search results to a text file
    spider.export('return')

if __name__ == "__main__":
    main()