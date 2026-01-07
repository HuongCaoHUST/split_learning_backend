import sqlite3
import uuid
from pathlib import Path

DB_FILE = Path(__file__).parent / "split_learning.db"

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Creates the 'nodes' table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL UNIQUE,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def register_node(client_id: uuid.UUID):
    """Registers a new node in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO nodes (client_id) VALUES (?)", (str(client_id),))
        conn.commit()
    except sqlite3.IntegrityError:
        # Client ID already exists
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    create_table()
    print("Database and table created successfully.")
