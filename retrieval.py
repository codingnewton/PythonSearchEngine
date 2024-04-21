from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class YourClass:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def pagerank(self, M, num_iterations=100, d=0.85):
        N = M.shape[1]
        v = np.random.rand(N, 1)
        v = v / np.linalg.norm(v, 1)
        M_hat = (d * M + (1 - d) / N)
        for i in range(num_iterations):
            v = M_hat @ v
        return v

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
        pagerank_scores = self.pagerank(adjacency_matrix)

        # Combine cosine similarity with PageRank and favor matches in title
        final_scores = {i: (0.5 * similarities[0][i] + 0.5 * pagerank_scores[i]) * (1 + titles[i].lower().count(query.lower())) for i in range(len(documents))}

        # Get the indices of the documents sorted by their final score (in descending order)
        ranked_indices = sorted(final_scores, key=final_scores.get, reverse=True)

        # Return the documents in their ranked order
        return [documents[i] for i in ranked_indices]
