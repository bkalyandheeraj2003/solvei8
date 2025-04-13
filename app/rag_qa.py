# app/rag_qa.py

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from transformers import pipeline

# Use a faster distilled model for QA
QA_MODEL_NAME = "distilbert-base-uncased-distilled-squad"

# Set up ChromaDB client with persistent settings (optional but recommended)
CHROMA_SETTINGS = Settings(anonymized_telemetry=False)
client = chromadb.Client(CHROMA_SETTINGS)

# Preload embedding function for efficiency
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Initialize collection once to avoid repeated overhead
collection = client.get_or_create_collection(
    name="analytics",
    embedding_function=embedding_fn
)

# Initialize QA model pipeline once
qa_pipeline = pipeline("question-answering", model=QA_MODEL_NAME, tokenizer=QA_MODEL_NAME)

def get_relevant_context(question: str) -> str:
    """Query ChromaDB for top-k relevant documents."""
    results = collection.query(query_texts=[question], n_results=3)
    return " ".join(results['documents'][0]) if results['documents'] else "No relevant data found."

def answer_question(question: str) -> str:
    """Generate an answer using relevant context from ChromaDB and a fast QA model."""
    context = get_relevant_context(question)
    if context == "No relevant data found.":
        return "Sorry, I couldn't find relevant data to answer that question."
    
    result = qa_pipeline({
        "question": question,
        "context": context
    })
    return result['answer']
