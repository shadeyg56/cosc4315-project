import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import json

# List of documents (in a real-world use case, these would come from a database or search engine)
documents = [
    "Python is a popular programming language used in data science and web development.",
    "Machine learning involves training models to make predictions from data.",
    "Natural language processing is a field of AI focused on processing human language.",
    "Deep learning techniques utilize neural networks to solve complex problems."
]

def load_json():
    with open("data.json") as f:
        data = json.load(f)
    documents = []
    for entry in data:
        for key in entry:
            string = f"{entry["title"]}\n\n{entry["top_answer"]}"
            documents.append(string)
    return documents


# A simple retrieval function using TF-IDF and cosine similarity
def retrieve_documents(query, documents, top_n=2):
    # Convert documents and query to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents + [query])
    
    # Compute cosine similarity between the query and all documents
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Get the indices of the top_n most similar documents
    similar_doc_indices = cosine_sim.argsort()[0][-top_n:][::-1]
    
    return [documents[i] for i in similar_doc_indices]

# A simple function to generate a summary using a transformer model
def generate_summary(retrieved_docs):
    summarizer = pipeline("summarization")
    # Join the documents to provide context to the summarizer
    combined_text = " ".join(retrieved_docs)
    summary = summarizer(combined_text, max_length=100, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Example query
query = "How to install a package in Debian?"

documents = load_json()
# Step 1: Retrieve relevant documents based on cosine similarity
retrieved_docs = retrieve_documents(query, documents)

# Step 2: Generate a summary based on the retrieved documents
summary = generate_summary(retrieved_docs)

print("Retrieved Documents:")
for doc in retrieved_docs:
    print(f"- {doc}")

print("\nGenerated Summary:")
print(summary)

