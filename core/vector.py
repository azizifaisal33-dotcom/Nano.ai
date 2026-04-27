"""
📊 NanoVectorStore v2 - FAISS Semantic Memory
Advanced vector database with cosine similarity
"""
import numpy as np
import faiss
import sqlite3
import pickle
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import hashlib
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

class NanoVectorStore:
    def __init__(self, dimension: int = 384, index_file: str = "data/vectors.index"):
        self.console = Console()
        self.dimension = dimension
        self.index_file = Path(index_file)
        self.db_file = Path("data/vector_db.sqlite")
        
        # FAISS Index
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product = Cosine
        self.metadata = []
        self.id_to_idx = {}
        
        # SQLite metadata store
        self._init_db()
        self._load_index()
        
    def _init_db(self):
        """Initialize SQLite metadata store"""
        self.db_file.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(self.db_file)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY,
                hash TEXT UNIQUE,
                text TEXT,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _load_index(self):
        """Load FAISS index from disk"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'rb') as f:
                    self.index = faiss.read_index(str(self.index_file))
                self.console.print("[green]✓ FAISS index loaded[/]")
                
                # Load metadata
                conn = sqlite3.connect(self.db_file)
                cursor = conn.execute("SELECT id, hash, text FROM vectors ORDER BY id")
                self.metadata = [{"id": row[0], "hash": row[1], "text": row[2]} 
                               for row in cursor.fetchall()]
                conn.close()
                self.console.print(f"[green]✓ Metadata: {len(self.metadata)} vectors[/]")
            except Exception as e:
                self.console.print(f"[yellow]⚠️  Index load failed: {e}[/]")

    def add(self, text: str, embedding: np.ndarray, metadata: Dict = None):
        """Add vector + metadata"""
        if metadata is None:
            metadata = {}
            
        # Normalize embedding for cosine similarity
        embedding = embedding / np.linalg.norm(embedding)
        
        # Add to FAISS
        vector_id = self.index.ntotal
        self.index.add(embedding.reshape(1, -1))
        
        # Store metadata
        doc_hash = hashlib.md5(text.encode()).hexdigest()
        self.metadata.append({
            "id": vector_id, "hash": doc_hash, "text": text, **metadata
        })
        
        # Save to SQLite
        conn = sqlite3.connect(self.db_file)
        conn.execute("""
            INSERT OR REPLACE INTO vectors (hash, text, metadata, id)
            VALUES (?, ?, ?, ?)
        """, (doc_hash, text, json.dumps(metadata), vector_id))
        conn.commit()
        conn.close()
        
        self.console.print(f"[green]✓ Vector added #{vector_id}[/]")

    def search(self, query_embedding: np.ndarray, k: int = 5, threshold: float = 0.75) -> List[Dict]:
        """Semantic search with similarity threshold"""
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # FAISS search (cosine similarity)
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1 or dist < threshold:
                break
                
            result = self.metadata[idx]
            result['similarity'] = float(dist)
            results.append(result)
            
        return results

    def batch_add(self, texts: List[str], embeddings: np.ndarray):
        """Batch insertion"""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Indexing batch...", total=len(texts))
            
            batch_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            self.index.add(batch_embeddings)
            
            for i, text in enumerate(texts):
                self.add(text, batch_embeddings[i], {"batch": i})
                progress.advance(task)

    def save_index(self):
        """Persist FAISS index"""
        self.index_file.parent.mkdir(exist_ok=True)
        faiss.write_index(self.index, str(self.index_file))
        self.console.print("[green]✓ Index saved to disk[/]")

    def get_stats(self) -> Dict:
        """Vector store statistics"""
        return {
            'total_vectors': self.index.ntotal,
            'dimension': self.dimension,
            'index_type': 'FlatIP (Cosine)'
        }

    def delete_old(self, max_age_days: int = 30):
        """Cleanup old vectors"""
        conn = sqlite3.connect(self.db_file)
        cutoff = (datetime.now() - timedelta(days=max_age_days)).strftime('%Y-%m-%d')
        deleted = conn.execute("DELETE FROM vectors WHERE timestamp < ?", (cutoff,)).rowcount
        conn.commit()
        conn.close()
        self.console.print(f"[yellow]🧹 Deleted {deleted} old vectors[/]")

# Global instance
vectorstore = NanoVectorStore()