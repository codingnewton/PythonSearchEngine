from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class YourClass:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_page_rank(self, graph, damping_factor=0.85, epsilon=1e-8, max_iterations=100):
        num_pages = len(graph)
        initial_rank = 1/num_pages
        page_rank = {page: initial_rank for page in graph}
        out_links = {page: len(graph[page]) for page in graph}

        for _ in range(max_iterations):
            diff = 0
            for page in graph:
                rank = (1 - damping_factor)/num_pages
                for incoming_page in graph:
                    if page in graph[incoming_page]:
                        rank += damping_factor * paage_rank[incoming_page] / out_links[incoming_page]
                diff += abs(page_rank[page] - rank)
                page_rank[page] = rank
            if diff < epsilon:
                break
        return page_rank

    def ranking(self, documents, query, titles):
        # Fit the vectorizer and transform the documents into vectors
        document_vectors = self.vectorizer.fit_transform(documents)

        # Transform the query into a vector
        query_vector = self.vectorizer.transform([query])

        # Calculate the cosine similarity between the query vector and each document vector
        similarities = cosine_similarity(query_vector, document_vectors)

        # Create an adjacency matrix for PageRank
        adjacency_matrix = (similarities > 0).astype(int)

        # Calculate PageRank scores
        pagerank_scores = self.calculate_page_rank(adjacency_matrix)

        # Combine cosine similarity with PageRank and favor matches in title
        final_scores = {i: (0.5 * similarities[0][i] + 0.5 * pagerank_scores[i]) * (1 + titles[i].lower().count(query.lower())) for i in range(len(documents))}

        # Get the indices of the documents sorted by their final score (in descending order)
        ranked_indices = sorted(final_scores, key=final_scores.get, reverse=True)

        # Return the documents in their ranked order
        return [documents[i] for i in ranked_indices]
