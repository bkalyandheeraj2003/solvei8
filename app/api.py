import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from app.data_loader import load_and_clean_data
from app.analytics import compute_and_store_analytics
from app.rag_qa import answer_question
from app.db import DB_PATH, init_db

# Initialize the database (run this on startup)
init_db()

# Load and clean data
df = load_and_clean_data("data/hotel_bookings.csv")
compute_and_store_analytics("data/hotel_bookings.csv")  # Compute and store analytics in DB

app = FastAPI()

@app.post("/analytics")
def get_analytics():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Revenue trends
    cur.execute("SELECT month, revenue FROM revenue_trends")
    revenue_trends_data = cur.fetchall()

    # Cancellation rate
    cur.execute("SELECT value FROM cancellation_stats WHERE metric = 'cancellation_rate'")
    cancellation_rate_data = cur.fetchone()[0]

    # Geo distribution
    cur.execute("SELECT country, bookings FROM geo_distribution")
    geo_distribution_data = cur.fetchall()

    # Lead time distribution
    cur.execute("SELECT metric, value FROM lead_time_distribution")
    lead_time_distribution_data = cur.fetchall()

    conn.close()

    return {
        "revenue_trends": revenue_trends_data,
        "cancellation_rate": f"{cancellation_rate_data}%",
        "geo_distribution": geo_distribution_data,
        "lead_time_distribution": lead_time_distribution_data
    }

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    answer = answer_question(query.question)
    return {"question": query.question, "answer": answer}
