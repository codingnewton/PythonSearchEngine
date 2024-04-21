from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def search_documents(query, documents, titles):
    # Initialize the TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    document_tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Transform the query
    query_tfidf = tfidf_vectorizer.transform([query])

    # Calculate the cosine similarities between the query and all documents
    cosine_similarities = cosine_similarity(query_tfidf, document_tfidf_matrix).flatten()

    # Boost the cosine similarities for documents where the query matches the title
    for i in range(len(documents)):
        if query.lower() in titles[i].lower():
            cosine_similarities[i] *= 1.5  # Increase the weight by 50%

    # Get the indices of the top 50 documents
    top_50_indices = cosine_similarities.argsort()[:-51:-1]

    # Return the top 50 documents
    return [documents[i] for i in top_50_indices]