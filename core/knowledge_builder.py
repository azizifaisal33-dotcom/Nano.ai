#!/usr/bin/env python3
import subprocess
import re
import sqlite3
import pickle
from pathlib import Path
from typing import List, Optional

class AutonomousKnowledge:
    def __init__(self):
        self.kb_dir = Path("data/knowledge")
        self.kb_dir.mkdir(exist_ok=True)
        self.vector_db = self.kb_dir / "vector_db.sqlite"
        self._init_db()

    def _init_db(self):
        """Self-creating vector database"""
        conn = sqlite3.connect(self.vector_db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY,
                query TEXT,
                response TEXT,
                vector BLOB,
                source TEXT,
                timestamp REAL
            )
        """)
        conn.commit()
        conn.close()

    def local_search(self, query: str) -> List[str]:
        """Fast local lookup"""
        conn = sqlite3.connect(self.vector_db)
        cursor = conn.execute(
            "SELECT response FROM vectors WHERE query LIKE ? ORDER BY timestamp DESC LIMIT 3",
            (f"%{query}%",)
        )
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results

    def web_scrape(self, query: str) -> List[str]:
        """Autonomous Google scrape"""
        try:
            # Raw curl google
            cmd = f"curl -s -A 'NanoAI' 'https://www.google.com/search?q={query.replace(' ', '+')}'"
            html = subprocess.getoutput(cmd)
            
            # Extract snippets
            snippets = re.findall(r'<div class="[^"]*snippet[^"]*">(.*?)</div>', html, re.DOTALL)
            urls = re.findall(r'<a href="/url\?q=([^&"]+)', html)
            
            knowledge = []
            for i, (snippet, url) in enumerate(zip(snippets[:5], urls[:5])):
                clean_snippet = re.sub(r'<[^>]+>', '', snippet)[:200]
                knowledge.append(f"{clean_snippet} | {url}")
            
            # Auto-save to vector DB
            self._save_knowledge(query, knowledge)
            return knowledge[:3]
            
        except:
            return ["Web search unavailable"]

    def _save_knowledge(self, query: str, knowledge: List[str]):
        """Tokenize & vectorize"""
        conn = sqlite3.connect(self.vector_db)
        vector = pickle.dumps([hash(w) for w in query.split()])  # Simple hash vector
        
        for item in knowledge[:3]:
            conn.execute(
                "INSERT INTO vectors (query, response, vector, source, timestamp) VALUES (?, ?, ?, 'web', ?)",
                (query, item, vector, time.time())
            )
        conn.commit()
        conn.close()

    def search(self, query: str) -> str:
        """Master search: local → web"""
        local = self.local_search(query)
        if local:
            return f"💾 {local[0]}"
        
        web = self.web_scrape(query)
        return f"🌐 {web[0] if web else 'No data'}"

# Global brain
knowledge = AutonomousKnowledge()