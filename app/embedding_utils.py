# app/embedding_utils.py

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import sqlite3

DB_PATH = "analytics.db"

def generate_analytics_summaries():
    summaries = []

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Revenue trends
    for row in cur.execute("SELECT * FROM revenue_trends"):
        summaries.append(f"Total revenue in {row[0]} was {row[1]:.2f} euros.")

    # Cancellation rate
    cur.execute("SELECT value FROM cancellation_stats WHERE metric='cancellation_rate'")
    cancel_rate = cur.fetchone()[0]
    summaries.append(f"The overall cancellation rate is {cancel_rate:.2f}%.")

    # Geo distribution
    for row in cur.execute("SELECT * FROM geo_distribution LIMIT 30"):  # limit for brevity
        summaries.append(f"{row[0]} had {row[1]} bookings.")

    # Lead time
    for row in cur.execute("SELECT * FROM lead_time_distribution"):
        summaries.append(f"The {row[0]} lead time is {row[1]:.2f} days.")

    conn.close()
    return summaries

def store_embeddings_in_chroma():
    summaries = generate_analytics_summaries()

    embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="analytics", embedding_function=embedding_fn)

    collection.add(
        documents=summaries,
        ids=[f"summary_{i}" for i in range(len(summaries))]
    )

    print("✅ Embedded and stored analytics in ChromaDB.")
