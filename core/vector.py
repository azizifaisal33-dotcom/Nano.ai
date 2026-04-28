import json
import sqlite3
import hashlib
import os
import math
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from datetime import datetime

class NanoVectorStore:
    def __init__(self, dimension: int = 384, index_file: str = "data/vectors.json"):
        # Menggunakan print biasa agar tidak NameError: Console
        self.dimension = dimension
        self.db_file = Path("data/vector_db.sqlite")
        self.memory_cache = [] # Untuk pencarian cepat di RAM

        self._init_db()
        self._load_from_db()

    def _init_db(self):
        """Fitur Database: Tetap simpan metadata secara permanen"""
        self.db_file.parent.mkdir(exist_ok=True, parents=True)
        conn = sqlite3.connect(self.db_file)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE,
                text TEXT,
                vector TEXT, 
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _load_from_db(self):
        """Memuat data dari SQLite ke RAM saat startup"""
        if self.db_file.exists():
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.execute("SELECT hash, text, vector FROM vectors")
                for row in cursor.fetchall():
                    self.memory_cache.append({
                        "hash": row, 
                        "text": row, 
                        "vector": json.loads(row)
                    })
                conn.close()
                print(f"✓ NanoAI Memory Loaded: {len(self.memory_cache)} vectors")
            except Exception as e:
                print(f"⚠️ Load failed: {e}")

    def _normalize(self, v: List[float]) -> List[float]:
        """Fungsi matematika manual pengganti np.linalg.norm"""
        norm = math.sqrt(sum(x*x for x in v))
        return [x/norm for x in v] if norm > 0 else v

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Fungsi Semantic Search manual pengganti FAISS"""
        # Perhitungan dot product
        return sum(a * b for a, b in zip(v1, v2))

    def add(self, text: str, embedding: List[float], metadata: Dict = None):
        """Fitur Tambah Memori: Tetap simpan vector + metadata"""
        metadata = metadata or {}
        embedding = self._normalize(embedding)
        doc_hash = hashlib.md5(text.encode()).hexdigest()

        # Update Cache RAM
        self.memory_cache.append({"hash": doc_hash, "text": text, "vector": embedding})

        # Simpan Permanen ke SQLite
        try:
            conn = sqlite3.connect(self.db_file)
            conn.execute("""
                INSERT OR REPLACE INTO vectors (hash, text, vector, metadata)
                VALUES (?, ?, ?, ?)
            """, (doc_hash, text, json.dumps(embedding), json.dumps(metadata)))
            conn.commit()
            conn.close()
            print(f"✓ Vector stored: {text[:30]}...")
        except Exception as e:
            print(f"❌ Database Error: {e}")

    def search(self, query_embedding: List[float], k: int = 5, threshold: float = 0.45) -> List[Dict]:
        """Fitur Semantic Search: Tetap mencari berdasarkan kemiripan makna"""
        query_embedding = self._normalize(query_embedding)
        
        results = []
        for item in self.memory_cache:
            sim = self._cosine_similarity(query_embedding, item['vector'])
            if sim >= threshold:
                res = item.copy()
                res['similarity'] = float(sim)
                results.append(res)

        # Sort berdasarkan yang paling mirip
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:k]

    def batch_add(self, texts: List[str], embeddings: List[List[float]]):
        """Fitur Batch: Tetap bisa memproses banyak data sekaligus"""
        print(f"⚙️  Processing batch: {len(texts)} items...")
        for i, text in enumerate(texts):
            self.add(text, embeddings[i], {"batch_mode": True})

    def get_stats(self) -> Dict:
        """Fitur Stats: Menampilkan kondisi memori NanoAI"""
        return {
            'total_vectors': len(self.memory_cache),
            'dimension': self.dimension,
            'status': 'Online (Pure Python)'
        }

# Global instance
vectorstore = NanoVectorStore()
