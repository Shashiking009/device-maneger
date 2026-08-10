import time
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from database import get_connection, init_db
from memory.models import Memory, MemoryCategory, MemorySource
from memory.secrets import is_secret

class MemoryStorage:
    """
    SQLite-backed Local Storage Manager for Spidy AI Memories.
    Handles duplicate prevention, conflict resolution, secret rejection, and thread-safe CRUD.
    """
    def __init__(self):
        init_db()

    def save_memory(self, memory: Memory) -> Tuple[bool, str, Optional[Memory]]:
        if is_secret(memory.value) or is_secret(memory.key):
            return False, "Secret or sensitive credential detected; storage rejected.", None

        conn = get_connection()
        cursor = conn.cursor()
        now = time.time()

        try:
            # Check for existing memory with same key
            cursor.execute("SELECT id FROM memories WHERE key = ?", (memory.key,))
            row = cursor.fetchone()
            
            if row:
                # Update existing memory record
                existing_id = row["id"]
                cursor.execute("""
                UPDATE memories
                SET value = ?, category = ?, source = ?, confidence = ?, importance = ?, scope = ?, updated_at = ?, last_used_at = ?
                WHERE id = ?
                """, (memory.value, memory.category.value, memory.source.value, memory.confidence, memory.importance, memory.scope, now, now, existing_id))
                conn.commit()
                memory.id = existing_id
                memory.updated_at = now
                memory.last_used_at = now
                return True, f"Updated preference '{memory.key}' -> '{memory.value}'", memory
            else:
                # Insert new memory record
                cursor.execute("""
                INSERT INTO memories (id, category, key, value, source, confidence, importance, scope, created_at, updated_at, last_used_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (memory.id, memory.category.value, memory.key, memory.value, memory.source.value, memory.confidence, memory.importance, memory.scope, memory.created_at, memory.updated_at, memory.last_used_at, memory.expires_at))
                conn.commit()
                return True, f"Saved preference '{memory.key}' -> '{memory.value}'", memory
        except Exception as e:
            return False, f"Memory save error: {str(e)}", None
        finally:
            conn.close()

    def get_memory(self, key: str) -> Optional[Memory]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM memories WHERE key = ? OR id = ?", (key, key))
            row = cursor.fetchone()
            if row:
                # Touch last_used_at
                now = time.time()
                cursor.execute("UPDATE memories SET last_used_at = ? WHERE id = ?", (now, row["id"]))
                conn.commit()
                return Memory(
                    id=row["id"],
                    category=MemoryCategory(row["category"]),
                    key=row["key"],
                    value=row["value"],
                    source=MemorySource(row["source"]),
                    confidence=row["confidence"],
                    importance=row["importance"],
                    scope=row["scope"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    last_used_at=now,
                    expires_at=row["expires_at"]
                )
            return None
        finally:
            conn.close()

    def delete_memory(self, key_or_id: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM memories WHERE key = ? OR id = ?", (key_or_id, key_or_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def list_memories(self, category: Optional[MemoryCategory] = None) -> List[Memory]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if category:
                cursor.execute("SELECT * FROM memories WHERE category = ? ORDER BY importance DESC, updated_at DESC", (category.value,))
            else:
                cursor.execute("SELECT * FROM memories ORDER BY importance DESC, updated_at DESC")
            rows = cursor.fetchall()
            return [
                Memory(
                    id=r["id"],
                    category=MemoryCategory(r["category"]),
                    key=r["key"],
                    value=r["value"],
                    source=MemorySource(r["source"]),
                    confidence=r["confidence"],
                    importance=r["importance"],
                    scope=r["scope"],
                    created_at=r["created_at"],
                    updated_at=r["updated_at"],
                    last_used_at=r["last_used_at"],
                    expires_at=r["expires_at"]
                ) for r in rows
            ]
        finally:
            conn.close()

    def clear_all_memories(self) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM memories")
            conn.commit()
            return True
        finally:
            conn.close()

memory_storage = MemoryStorage()
