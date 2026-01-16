import sqlite3
import os

DB_PATH = 'mapping.db'

def init_db():
    """Initialize the SQLite database with tables and sample data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create mapping table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mapping (
            id TEXT PRIMARY KEY,
            website TEXT NOT NULL
        )
    ''')
    
    # Create imageslog table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imageslog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            filename TEXT NOT NULL,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data (avoid duplicates)
    cursor.execute("DELETE FROM mapping")  # Clear existing data
    cursor.execute("INSERT INTO mapping (id, website) VALUES (?, ?)", ('605004', 'pondicherry.com'))
    cursor.execute("INSERT INTO mapping (id, website) VALUES (?, ?)", ('605106', 'cuddlore.com'))
    cursor.execute("INSERT INTO mapping (id, website) VALUES (?, ?)", ('627003', 'tirunelveli.com'))

    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
    print("Tables created: mapping, imageslog")
    print("Sample data inserted: 605004 -> pondicherry.com, 605106 -> cuddlore.com, 627003 -> tirunelveli.com")

if __name__ == '__main__':
    init_db()
