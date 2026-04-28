import sqlite3
from pathlib import Path


class NanoMemory:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init()

    def _init(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_input TEXT,
            ai_response TEXT,
            intent TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    # =========================
    # ADD MEMORY
    # =========================
    def add(self, session_id, user_input, ai_response, intent="chat"):
        self.conn.execute("""
        INSERT INTO conversations
        (session_id, user_input, ai_response, intent)
        VALUES (?, ?, ?, ?)
        """, (session_id, user_input, ai_response, intent))

        self.conn.commit()

    # =========================
    # SEARCH MEMORY
    # =========================
    def search(self, query):
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.execute("""
        SELECT * FROM conversations
        WHERE user_input LIKE ?
        ORDER BY id DESC
        LIMIT 5
        """, (f"%{query}%",))

        return [dict(r) for r in cur.fetchall()]


memory = NanoMemory()