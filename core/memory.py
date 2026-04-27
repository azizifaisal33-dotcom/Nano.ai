import sqlite3
import json
from pathlib import Path
import hashlib
from datetime import datetime, timedelta

class NanoMemory:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()


    # =========================
    # INIT DB
    # =========================
    def _init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_input TEXT,
            ai_response TEXT,
            intent TEXT,
            tool_used TEXT,
            success INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT
        );

        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_active DATETIME,
            message_count INTEGER DEFAULT 0
        );
        """)
        self.conn.commit()


    # =========================
    # ADD MEMORY
    # =========================
    def add(self, session_id, user_input, ai_response,
            intent="unknown", tool_used="none",
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

        # update session
        self.conn.execute("""
        INSERT INTO sessions (session_id, name, last_active, message_count)
        VALUES (?, ?, CURRENT_TIMESTAMP, 1)
        ON CONFLICT(session_id)
        DO UPDATE SET
            last_active=CURRENT_TIMESTAMP,
            message_count=message_count+1
        """, (session_id, f"Session-{session_id[:8]}"))

        self.conn.commit()


    # =========================
    # SEARCH MEMORY
    # =========================
    def search(self, query, session_id=None, limit=10):
        self.conn.row_factory = sqlite3.Row

        sql = """
        SELECT * FROM conversations
        WHERE user_input LIKE ?
        """

        params = [f"%{query}%"]

        if session_id:
            sql += " AND session_id=?"
            params.append(session_id)

        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cur = self.conn.execute(sql, params)

        return [dict(r) for r in cur.fetchall()]


    # =========================
    # SESSION HISTORY
    # =========================
    def history(self, session_id, limit=50):
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.execute("""
        SELECT * FROM conversations
        WHERE session_id=?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (session_id, limit))

        return [dict(r) for r in cur.fetchall()]


    # =========================
    # STATS
    # =========================
    def stats(self):
        cur = self.conn.execute("SELECT COUNT(*) FROM conversations")
        total = cur.fetchone()[0]

        cur = self.conn.execute("SELECT COUNT(DISTINCT session_id) FROM conversations")
        sessions = cur.fetchone()[0]

        return {
            "total_conversations": total,
            "total_sessions": sessions
        }


# GLOBAL INSTANCE
memory = NanoMemory()