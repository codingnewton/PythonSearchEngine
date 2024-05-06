from scraper import HTML_list

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
    #print((scores.keys()))
    result, HTML_list_object = spider.fileretrieve(filename, page_ids=scores.keys())
    #print(HTML_list_object)
    HTML_list_object.export("print")

    web_graph = spider.create_web_graph()
    #print((calculate_pagerank(web_graph).keys()))
    print(type(HTML_list_object))

    # Export the search results to a text file
    spider.export('return')

if __name__ == "__main__":
    main()
