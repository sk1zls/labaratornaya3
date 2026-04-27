import sqlite3
import os

DB_NAME = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget_limits (
                category TEXT NOT NULL,
                limit_amount REAL NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                PRIMARY KEY (category, month, year)
            )
        """)
        conn.commit()