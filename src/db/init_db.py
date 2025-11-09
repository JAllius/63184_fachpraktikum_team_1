# db/init_db.py
# Simple MySQL DB init script for our project

import mysql.connector
import logging

# TODO: get from config
DB_HOST = "localhost"
DB_USER = "root"
DB_PW = "safe123"
DB_NAME = "app"

logger = logging.getLogger(__name__)

def main():
    # connect to MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PW
    )
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    # connect to MySQL database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PW,
        database=DB_NAME
    )
    cur = conn.cursor()

    # table for uploads (datasets that are processed)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS 
    uploads (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        filename TEXT NOT NULL,
        uploaded_at TEXT NOT NULL
    );
    """)

    # table for predictions (results of models)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS 
    predictions (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        upload_id INTEGER NOT NULL,
        model_name TEXT NOT NULL,
        result_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(upload_id) REFERENCES uploads(id)
    );
    """)

    conn.commit()
    conn.close()
    logger.info(f"Database initialized")
