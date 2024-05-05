from scraper import HTML_list

def main():
    # Initialize the HTML_list object
    spider = HTML_list()

    filename = "indexertest.db"

    # # Perform forward indexing
    # spider.dbforward(filename)

    # # Perform inverted indexing
    # spider.dbinverted(filename)

    # print(spider.dbtemptest(filename, range(1,100)))
    # spider.dbtest(filename, 'inverted_index')

    query = ['comput', 'part', 'document', 'final']

    postingslistbodies, postingslisttitles = spider.queryretrieve(filename, query)
    print(f"Po  `stings List of page body: {postingslistbodies}\nPostings List of page title: {postingslisttitles}")

    weighted_vector_bodies, weighted_vector_titles = spider.vector_space(filename, postingslistbodies, postingslisttitles)
    print(f"Weigthed Vectors Bodies are: {weighted_vector_bodies}\nWeighted Vectors Titles are: {weighted_vector_titles}")

    similarity_scores = spider.cossim(weighted_vector_bodies, query)
    print(f"Similarity scores: {similarity_scores}")
    
    # Export the search results to a text file
    spider.export('return')

if __name__ == "__main__":
    main()