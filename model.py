import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, AutoTokenizer
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

# A simple function to generate a answer using a transformer model
def generate_answer(query, retrieved_docs):
    tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
    qa_pipeline = pipeline("text-generation", model="./sys-admin-gpt2", tokenizer=tokenizer)
    # Join the documents to provide context to the summarizer
    combined_text = " ".join(retrieved_docs)
    prompt = f"Question: {query}\nAnswer:"
    result = qa_pipeline(prompt)
    return result[0]["generated_text"]

# Example query
#query = "How to ping a port?"
query = input("Enter your question: ")

documents = load_json()
# Step 1: Retrieve relevant documents based on cosine similarity
retrieved_docs = retrieve_documents(query, documents)

# Step 2: Generate a answer based on the retrieved documents
answer = generate_answer(query, retrieved_docs)

print("Retrieved Documents:")
for doc in retrieved_docs:
    print(f"- {doc}")

print("\nGenerated answer:")
print(answer)

