# app/db.py

import sqlite3
import pandas as pd

DB_PATH = "analytics.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS revenue_trends (
        month TEXT PRIMARY KEY,
        revenue REAL
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cancellation_stats (
        metric TEXT PRIMARY KEY,
        value REAL
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS geo_distribution (
        country TEXT PRIMARY KEY,
        bookings INTEGER
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lead_time_distribution (
        metric TEXT PRIMARY KEY,
        value REAL
    )""")

    conn.commit()
    conn.close()
