import sqlite3
import json
from pathlib import Path


class NanoMemory:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init()

    # =========================
    # INIT DB
    # =========================
    def _init(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_input TEXT,
            ai_response TEXT,
            intent TEXT,
            tool_used TEXT DEFAULT 'none',
            success INTEGER DEFAULT 1,
            metadata TEXT DEFAULT '{}',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    # =========================
    # ADD MEMORY (FIXED + FLEXIBLE)
    # =========================
    def add(self, session_id, user_input, ai_response,
            intent="chat", tool_used="none",
            success=True, metadata=None):

        if metadata is None:
            metadata = {}

        self.conn.execute("""
        INSERT INTO conversations
        (session_id, user_input, ai_response, intent, tool_used, success, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            user_input,
            ai_response,
            intent,
            tool_used,
            int(success),
            json.dumps(metadata)
        ))

        self.conn.commit()

    # =========================
    # SEARCH MEMORY
    # =========================
    def search(self, query, limit=5):
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.execute("""
        SELECT * FROM conversations
        WHERE user_input LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """, (f"%{query}%", limit))

        return [dict(r) for r in cur.fetchall()]

    # =========================
    # GET HISTORY (OPTIONAL)
    # =========================
    def history(self, session_id, limit=20):
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.execute("""
        SELECT * FROM conversations
        WHERE session_id=?
        ORDER BY id DESC
        LIMIT ?
        """, (session_id, limit))

        return [dict(r) for r in cur.fetchall()]


# GLOBAL INSTANCE
memory = NanoMemory()