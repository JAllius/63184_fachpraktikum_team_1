# db/init_db.py
# Simple SQLite DB init script for our project

import sqlite3
from pathlib import Path

# Make sure the db folder exists
DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "app.db"

def main():
    # connect to SQLite (file will be created if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # table for uploads (datasets that are processed)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        uploaded_at TEXT NOT NULL
    );
    """)

    # table for predictions (results of models)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id INTEGER NOT NULL,
        model_name TEXT NOT NULL,
        result_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(upload_id) REFERENCES uploads(id)
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database created at: {DB_PATH}")

if __name__ == "__main__":
    main()
