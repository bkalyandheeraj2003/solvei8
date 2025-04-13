# main.py

from app.db import init_db
from app.analytics import compute_and_store_analytics
from app.embedding_utils import store_embeddings_in_chroma

if __name__ == "__main__":
    init_db()
    compute_and_store_analytics("data/hotel_bookings.csv")
    store_embeddings_in_chroma()
