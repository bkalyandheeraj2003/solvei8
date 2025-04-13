# app/analytics.py
import sqlite3
from app.data_loader import load_and_clean_data
from app.db import DB_PATH

def revenue_trends(df):
    df['month'] = df['reservation_status_date'].dt.to_period('M').astype(str)
    return df.groupby('month')['adr'].sum().reset_index()

def compute_and_store_analytics(csv_path: str):
    df = load_and_clean_data(csv_path)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Revenue trends
    revenue = revenue_trends(df)  # Call the new separate function
    cur.executemany("INSERT OR REPLACE INTO revenue_trends (month, revenue) VALUES (?, ?)",
                     revenue.values.tolist())

    # Cancellation rate
    cancel_rate = round((df['is_canceled'].sum() / len(df)) * 100, 2)
    cur.execute("INSERT OR REPLACE INTO cancellation_stats (metric, value) VALUES (?, ?)",
                ("cancellation_rate", cancel_rate))

    # Country distribution
    country_data = df['country'].value_counts().reset_index()
    cur.executemany("INSERT OR REPLACE INTO geo_distribution (country, bookings) VALUES (?, ?)",
                     country_data.values.tolist())

    # Lead time stats
    lead_time_stats = df['lead_time'].describe().to_dict()
    for k, v in lead_time_stats.items():
        cur.execute("INSERT OR REPLACE INTO lead_time_distribution (metric, value) VALUES (?, ?)",
                     (k, v))

    conn.commit()
    conn.close()
