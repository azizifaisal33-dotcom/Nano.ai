import sqlite3
import json
from pathlib import Path
from datetime import datetime

class NanoMemory:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init()

    def _init(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_input TEXT,
                ai_response TEXT,
                intent TEXT,
                tool_used TEXT,
                success INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_input ON memory(user_input);
            CREATE INDEX IF NOT EXISTS idx_session ON memory(session_id);
        """)
        self.conn.commit()

    def add(self, session_id, user_input, ai_response, intent="chat", tool_used="unknown", success=True):
        self.conn.execute("""
            INSERT INTO memory (session_id, user_input, ai_response, intent, tool_used, success)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, user_input, ai_response, intent, tool_used, int(success)))
        self.conn.commit()
        return True

    def search(self, query, session_id=None, limit=5):
        if session_id:
            sql = """
                SELECT user_input, ai_response, intent, tool_used, success 
                FROM memory 
                WHERE session_id = ? AND (user_input LIKE ? OR ai_response LIKE ?)
                ORDER BY timestamp DESC LIMIT ?
            """
            results = self.conn.execute(sql, (session_id, f"%{query}%", f"%{query}%", limit)).fetchall()
        else:
            sql = """
                SELECT user_input, ai_response, intent, tool_used, success 
                FROM memory 
                WHERE user_input LIKE ? OR ai_response LIKE ?
                ORDER BY timestamp DESC LIMIT ?
            """
            results = self.conn.execute(sql, (f"%{query}%", f"%{query}%", limit)).fetchall()
        
        return [{"user_input": r[0], "ai_response": r[1], "intent": r[2], 
                "tool_used": r[3], "success": bool(r[4])} for r in results]

    def clear(self):
        self.conn.execute("DELETE FROM memory")
        self.conn.commit()
        return "Memory cleared"

    def stats(self):
        total = self.conn.execute("SELECT COUNT(*) FROM memory").fetchone()[0]
        sessions = self.conn.execute("SELECT COUNT(DISTINCT session_id) FROM memory").fetchone()[0]
        return {"total_records": total, "active_sessions": sessions}

# Global instance
memory = NanoMemory()