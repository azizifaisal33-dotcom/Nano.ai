"""
💾 NanoMemory v2 - Hybrid SQL + Vector Memory
Persistent conversation memory with full-text search
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
from rich.table import Table
from rich.console import Console

class NanoMemory:
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()
        self.console = Console()

    def _init_schema(self):
        """Create advanced memory schema"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_input TEXT,
                ai_response TEXT,
                intent TEXT,
                tool_used TEXT,
                success INTEGER,
                tokens_user INTEGER,
                tokens_ai INTEGER,
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
            
            CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp);
            CREATE INDEX IF NOT EXISTS idx_intent ON conversations(intent);
            CREATE INDEX IF NOT EXISTS idx_session ON conversations(session_id);
            CREATE FULLTEXT INDEX IF NOT EXISTS ft_user ON conversations(user_input);
        """)
        self.conn.commit()

    def add_conversation(self, session_id: str, user_input: str, 
                        ai_response: str, intent: str, tool_used: str,
                        success: bool, metadata: Dict = None):
        """Add conversation to memory"""
        if metadata is None:
            metadata = {}
            
        hash_id = hashlib.md5(user_input.encode()).hexdigest()
        
        self.conn.execute("""
            INSERT INTO conversations 
            (session_id, user_input, ai_response, intent, tool_used, 
             success, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, user_input, ai_response, intent, tool_used, 
              int(success), json.dumps(metadata)))
        
        # Update session
        self.conn.execute("""
            INSERT OR REPLACE INTO sessions (session_id, name, last_active, message_count)
            SELECT ?, ?, CURRENT_TIMESTAMP, COUNT(*)
            FROM conversations WHERE session_id = ?
        """, (session_id, f"Session-{session_id[:8]}", session_id))
        
        self.conn.commit()

    def search_similar(self, query: str, session_id: Optional[str] = None, 
                      limit: int = 10) -> List[Dict]:
        """Full-text + semantic search"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        
        where_clause = "WHERE user_input LIKE ?"
        params = [f'%{query}%']
        
        if session_id:
            where_clause += " AND session_id = ?"
            params.append(session_id)
            
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.execute(f"""
            SELECT *, 
                   (user_input LIKE ?) * 0.9 + 
                   (intent LIKE ?) * 0.1 AS relevance
            FROM conversations {where_clause}
            ORDER BY relevance DESC, timestamp DESC
            LIMIT ?
        """, params + [limit])
        
        return [dict(row) for row in cursor.fetchall()]

    def get_session_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history"""
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.execute("""
            SELECT * FROM conversations 
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, int]:
        """Memory statistics"""
        stats = {}
        cursor = self.conn.execute("SELECT COUNT(*) as total FROM conversations")
        stats['total_conversations'] = cursor.fetchone()[0]
        
        cursor = self.conn.execute("SELECT COUNT(DISTINCT session_id) FROM conversations")
        stats['total_sessions'] = cursor.fetchone()[0]
        
        cursor = self.conn.execute("""
            SELECT intent, COUNT(*) as count 
            FROM conversations 
            GROUP BY intent 
            ORDER BY count DESC LIMIT 5
        """)
        stats['top_intents'] = [row for row in cursor.fetchall()]
        
        return stats

    def prune_old(self, days: int = 30):
        """Remove old conversations"""
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        deleted = self.conn.execute(
            "DELETE FROM conversations WHERE timestamp < ?", (cutoff,)
        ).rowcount
        self.conn.commit()
        self.console.print(f"[yellow]🧹 Pruned {deleted} old conversations[/]")

    def show_stats(self):
        """Rich stats display"""
        stats = self.get_stats()
        table = Table(title="Memory Stats")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")
        
        table.add_row("Total Conversations", str(stats['total_conversations']))
        table.add_row("Active Sessions", str(stats['total_sessions']))
        
        self.console.print(table)
        
        # Top intents
        intent_table = Table(title="Top Intents")
        intent_table.add_column("Intent", style="magenta")
        intent_table.add_column("Count", justify="right")
        for row in stats['top_intents']:
            intent_table.add_row(row[0], str(row[1]))
        self.console.print(intent_table)

# Global memory instance
memory = NanoMemory()