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

def get_all_nodes():
    """Retrieves all registered nodes from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT client_id, registered_at FROM nodes")
    nodes = cursor.fetchall()
    conn.close()
    return nodes

def delete_node(client_id: uuid.UUID):
    """Deletes a specific node from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nodes WHERE client_id = ?", (str(client_id),))
    conn.commit()
    conn.close()

def delete_all_nodes():
    """Deletes all nodes from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nodes")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Database and table created successfully.")
