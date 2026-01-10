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
            client_id TEXT NOT NULL,
            run_id TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            number_images INTEGER,
            ram TEXT,
            cpu TEXT,
            UNIQUE(client_id, run_id)
        )
    """)
    conn.commit()
    conn.close()

def get_node(client_id: uuid.UUID, run_id: str):
    """Retrieves a single node by its client_id and run_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT client_id, run_id, registered_at, number_images, ram, cpu FROM nodes WHERE client_id = ? AND run_id = ?",
        (str(client_id), run_id)
    )
    node = cursor.fetchone()
    conn.close()
    return node

def update_node_details(client_id: uuid.UUID, run_id: str, number_images: int = None, ram: str = None, cpu: str = None):
    """Updates the details of an existing node."""
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []

    if number_images is not None:
        updates.append("number_images = ?")
        params.append(number_images)
    if ram is not None:
        updates.append("ram = ?")
        params.append(ram)
    if cpu is not None:
        updates.append("cpu = ?")
        params.append(cpu)

    if not updates:
        conn.close()
        return False # No updates provided

    set_clause = ", ".join(updates)
    params.append(str(client_id))
    params.append(run_id)

    cursor.execute(f"UPDATE nodes SET {set_clause} WHERE client_id = ? AND run_id = ?", tuple(params))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def register_node(client_id: uuid.UUID, run_id: str, number_images: int = None):
    """Registers a new node in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO nodes (client_id, run_id, number_images, ram, cpu) VALUES (?, ?, ?, NULL, NULL)", (str(client_id), run_id, number_images))
        conn.commit()
    except sqlite3.IntegrityError:
        # Client ID and run_id combination already exists
        pass
    finally:
        conn.close()

def get_all_nodes():
    """Retrieves all registered nodes from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT client_id, run_id, registered_at, number_images, ram, cpu FROM nodes")
    nodes = cursor.fetchall()
    conn.close()
    return nodes

def delete_node(client_id: uuid.UUID, run_id: str):
    """Deletes a specific node from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nodes WHERE client_id = ? AND run_id = ?", (str(client_id), run_id))
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
