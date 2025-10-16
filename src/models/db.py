import sqlite3
import os
from contextlib import contextmanager

# Database file path - stores SQLite database in the qms folder
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'qms.db')

def get_db_connection():
    """Get SQLite database connection"""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
        # Enable foreign keys in SQLite
        conn.execute("PRAGMA foreign_keys = ON")
        print("✅ Database connected successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None

@contextmanager
def get_cursor():
    """Context manager for database cursor"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            cursor.close()
            conn.close()

def dict_factory(cursor, row):
    """Convert row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
