import sqlite3
import datetime
from flask import g

DATABASE = 'extractions.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name TEXT,
            description TEXT,
            features TEXT,
            pricing TEXT,
            raw_html TEXT,
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'success'
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_extraction(url, extracted_data, raw_html="", status="success"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO extractions (url, name, description, features, pricing, raw_html, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        url,
        extracted_data.get('name', ''),
        extracted_data.get('description', ''),
        extracted_data.get('features', ''),
        extracted_data.get('pricing', ''),
        raw_html,
        status
    ))
    
    conn.commit()
    extraction_id = cursor.lastrowid
    conn.close()
    return extraction_id

def get_recent_extractions(limit=50):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, url, name, description, features, pricing, extracted_at, status
        FROM extractions
        ORDER BY extracted_at DESC
        LIMIT ?
    ''', (limit,))
    
    extractions = cursor.fetchall()
    conn.close()
    
    return [{
        'id': row[0],
        'url': row[1],
        'name': row[2],
        'description': row[3],
        'features': row[4],
        'pricing': row[5],
        'extracted_at': row[6],
        'status': row[7]
    } for row in extractions]

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()