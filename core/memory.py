import sqlite3
import json
from pathlib import Path
import hashlib


# =========================
# SEMANTIC KEY
# =========================
def semantic_key(text):
    text = text.lower()
    for w in ["cara", "bagaimana", "tolong", "aku", "saya"]:
        text = text.replace(w, "")
    text = " ".join(text.split())
    return hashlib.md5(text.encode()).hexdigest()


# =========================
# MEMORY CORE
# =========================
class NanoMemory:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_input TEXT,
            ai_response TEXT,
            intent TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            semantic_key TEXT
        );
        """)
        self.conn.commit()

    # =========================
    # ADD MEMORY
    # =========================
    def add(self, session_id, user_input, ai_response, intent="chat"):
        key = semantic_key(user_input)

        self.conn.execute("""
        INSERT INTO conversations
        (session_id, user_input, ai_response, intent, semantic_key)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_input, ai_response, intent, key))

        self.conn.commit()

    # =========================
    # SEARCH
    # =========================
    def search(self, query):
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.execute("""
        SELECT * FROM conversations
        WHERE user_input LIKE ?
        ORDER BY timestamp DESC
        LIMIT 10
        """, (f"%{query}%",))

        return [dict(r) for r in cur.fetchall()]

    # =========================
    # SEMANTIC SEARCH
    # =========================
    def semantic_search(self, query):
        key = semantic_key(query)

        self.conn.row_factory = sqlite3.Row

        cur = self.conn.execute("""
        SELECT * FROM conversations
        WHERE semantic_key = ?
        ORDER BY timestamp DESC
        LIMIT 10
        """, (key,))

        return [dict(r) for r in cur.fetchall()]


# GLOBAL
memory = NanoMemory()