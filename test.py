from scraper import HTML_list

def main():
    # Initialize the HTML_list object
    spider = HTML_list()

    filename = "indexertest.db"

    query = ['comput', 'part', 'document', 'final']
    
    scores = spider.retrieve(filename, query)
    # print(f"Similarity scores between the query and the pages are {scores}")
    # print(scores.keys())

    result, HTML_list_object = spider.fileretrieve(filename, page_ids=scores.keys())
    # print(result)

    # HTML_list_object.export("print")

    # Export the search results to a text file
    # spider.export('HTML_list_object')

if __name__ == "__main__":
    main()