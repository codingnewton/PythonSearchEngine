from scraper import HTML_list

def main():
    query = ['Comput']
    filename = 'indexer.db'
    spider = HTML_list()
    scores = spider.retrieve(filename=filename, query=query)
    result, HTML_list_object = spider.fileretrieve(filename=filename, combined_scores=scores)
    print(HTML_list_object)


if __name__ == '__main__':
    main()