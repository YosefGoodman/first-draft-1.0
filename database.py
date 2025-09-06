"""
database.py
-----------
Handles all database operations for storing chat history.

Instructions:
- Initialize SQLite database and tables.
- Provide helper functions to save interactions and retrieve context.
- Expand schema later if you want multiple tables (users, metadata, etc.).
"""

import sqlite3
import time

DB_FILE = "database.db"
conn = None

def init_db():
    """Initialize the database and create tables if they don't exist."""
    global conn
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            user_id TEXT,
            timestamp TEXT,
            user_input TEXT,
            bot_response TEXT
        )
    """)
    conn.commit()

def save_interaction(user_id, user_input, bot_response):
    """Save a single user-bot interaction."""
    timestamp = str(time.time())
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations VALUES (?, ?, ?, ?)",
        (user_id, timestamp, user_input, bot_response)
    )
    conn.commit()

def get_recent_context(user_id, limit=5):
    """Fetch the last 'limit' messages for a user as context."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_input, bot_response FROM conversations WHERE user_id=? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    # Reverse order to chronological
    rows.reverse()
    context = [f"User: {r[0]} | Bot: {r[1]}" for r in rows]
    return context

