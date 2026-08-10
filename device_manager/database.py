import sqlite3
import json
import time
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "device_manager.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL
    )
    """)
    
    # Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        sources TEXT,
        tokens_per_sec REAL,
        created_at REAL NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
    )
    """)
    
    # Documents table for RAG
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        chunks_count INTEGER NOT NULL,
        created_at REAL NOT NULL
    )
    """)
    
    # System settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

# Session functions
def create_session(session_id: str, title: str = "New Conversation") -> Dict[str, Any]:
    now = time.time()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (session_id, title, now, now)
    )
    conn.commit()
    conn.close()
    return {"id": session_id, "title": title, "created_at": now, "updated_at": now}

def get_sessions() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_session(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

# Message functions
def add_message(session_id: str, role: str, content: str, sources: Optional[List[Dict[str, Any]]] = None, tokens_per_sec: Optional[float] = None) -> int:
    now = time.time()
    sources_json = json.dumps(sources) if sources else None
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, sources, tokens_per_sec, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, role, content, sources_json, tokens_per_sec, now)
    )
    msg_id = cursor.lastrowid
    
    # Update session updated_at
    cursor.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))
    
    # Update session title if first user message
    cursor.execute("SELECT COUNT(*) as count FROM messages WHERE session_id = ?", (session_id,))
    msg_count = cursor.fetchone()["count"]
    if msg_count <= 2 and role == "user":
        short_title = content[:35] + "..." if len(content) > 35 else content
        cursor.execute("UPDATE sessions SET title = ? WHERE id = ?", (short_title, session_id))
        
    conn.commit()
    conn.close()
    return msg_id

def get_session_messages(session_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        item = dict(row)
        if item.get("sources"):
            try:
                item["sources"] = json.loads(item["sources"])
            except Exception:
                item["sources"] = []
        result.append(item)
    return result

# Document functions
def add_document(filename: str, filepath: str, file_type: str, file_size: int, chunks_count: int) -> int:
    now = time.time()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (filename, filepath, file_type, file_size, chunks_count, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (filename, filepath, file_type, file_size, chunks_count, now)
    )
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def get_documents() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_document(doc_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
