"""
Embedding Manager for MCP Conversation Intelligence System

This module provides semantic embedding capabilities for enhanced context matching
and prompt generation in the MCP conversation tracking system.
"""

import os
import json
import hashlib
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import sqlite3
import threading
import logging

# Try to import sentence-transformers, fallback to basic if not available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Using basic embeddings.")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: FAISS not available. Using basic similarity search.")


@dataclass
class EmbeddingEntry:
    """Represents a single embedding entry with metadata."""
    id: str
    text: str
    embedding: np.ndarray
    context_type: str
    session_id: Optional[str]
    user_id: Optional[str]
    created_at: datetime
    metadata: Dict[str, Any]
    similarity_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data['embedding'] = self.embedding.tolist() if self.embedding is not None else None
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmbeddingEntry':
        """Create from dictionary."""
        data['embedding'] = np.array(data['embedding']) if data['embedding'] else None
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


class EmbeddingManager:
    """
    Manages semantic embeddings for the MCP conversation intelligence system.
    
    Features:
    - Local embedding generation using sentence-transformers
    - FAISS-based vector similarity search
    - SQLite storage for persistence
    - Integration with existing context systems
    - Automatic embedding updates and cleanup
    """
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 db_path: str = "data/embeddings.db",
                 max_embeddings: int = 10000,
                 similarity_threshold: float = 0.7):
        """
        Initialize the embedding manager.
        
        Args:
            model_name: Name of the sentence transformer model
            db_path: Path to SQLite database for embeddings
            max_embeddings: Maximum number of embeddings to store
            similarity_threshold: Minimum similarity score for matches
        """
        self.model_name = model_name
        self.db_path = db_path
        self.max_embeddings = max_embeddings
        self.similarity_threshold = similarity_threshold
        
        # Initialize components
        self._init_embedding_model()
        self._init_database()
        self._init_vector_store()
        
        # Threading
        self.lock = threading.RLock()
        self.logger = self._setup_logging()
        
        # Statistics
        self.stats = {
            'embeddings_generated': 0,
            'similarity_searches': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def _init_embedding_model(self):
        """Initialize the embedding model."""
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(self.model_name)
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                self.logger.info(f"Initialized sentence transformer: {self.model_name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize sentence transformer: {e}")
                self._fallback_embedding_model()
        else:
            self._fallback_embedding_model()
    
    def _fallback_embedding_model(self):
        """Fallback to basic embedding model."""
        self.model = None
        self.embedding_dim = 384  # Standard dimension for fallback
        self.logger.warning("Using fallback embedding model")
    
    def _init_database(self):
        """Initialize the SQLite database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    embedding BLOB NOT NULL,
                    context_type TEXT NOT NULL,
                    session_id TEXT,
                    user_id TEXT,
                    created_at TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_context_type 
                ON embeddings(context_type)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_id 
                ON embeddings(session_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON embeddings(created_at)
            """)
    
    def _init_vector_store(self):
        """Initialize the FAISS vector store."""
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatIP(self.embedding_dim)
            self.vector_ids = []
            self.logger.info("Initialized FAISS vector store")
        else:
            self.index = None
            self.vector_ids = []
            self.logger.warning("FAISS not available, using basic similarity search")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the embedding manager."""
        logger = logging.getLogger('EmbeddingManager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for given text.
        
        Args:
            text: Text to embed
            
        Returns:
            numpy array of the embedding
        """
        if self.model is not None:
            try:
                embedding = self.model.encode(text, convert_to_numpy=True)
                return embedding
            except Exception as e:
                self.logger.error(f"Failed to generate embedding: {e}")
                return self._generate_fallback_embedding(text)
        else:
            return self._generate_fallback_embedding(text)
    
    def _generate_fallback_embedding(self, text: str) -> np.ndarray:
        """Generate a basic fallback embedding."""
        # Simple hash-based embedding for fallback
        text_hash = hashlib.md5(text.encode()).hexdigest()
        # Convert hash to fixed-size array
        embedding = np.zeros(self.embedding_dim)
        for i, char in enumerate(text_hash[:self.embedding_dim]):
            embedding[i] = ord(char) / 255.0
        return embedding
    
    def add_embedding(self, 
                     text: str, 
                     context_type: str,
                     session_id: Optional[str] = None,
                     user_id: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a new embedding to the system.
        
        Args:
            text: Text to embed
            context_type: Type of context (e.g., 'conversation', 'technical', 'user_preference')
            session_id: Optional session ID
            user_id: Optional user ID
            metadata: Additional metadata
            
        Returns:
            ID of the created embedding
        """
        with self.lock:
            # Generate embedding
            embedding = self.generate_embedding(text)
            
            # Create entry
            entry_id = hashlib.md5(f"{text}{context_type}{session_id}{user_id}".encode()).hexdigest()
            entry = EmbeddingEntry(
                id=entry_id,
                text=text,
                embedding=embedding,
                context_type=context_type,
                session_id=session_id,
                user_id=user_id,
                created_at=datetime.now(),
                metadata=metadata or {}
            )
            
            # Store in database
            self._store_embedding(entry)
            
            # Add to vector store if available
            if self.index is not None:
                self._add_to_vector_store(entry)
            
            # Update statistics
            self.stats['embeddings_generated'] += 1
            
            # Cleanup if needed
            self._cleanup_old_embeddings()
            
            self.logger.info(f"Added embedding: {entry_id[:8]}... for {context_type}")
            return entry_id
    
    def _store_embedding(self, entry: EmbeddingEntry):
        """Store embedding in SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO embeddings 
                (id, text, embedding, context_type, session_id, user_id, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id,
                entry.text,
                entry.embedding.tobytes(),
                entry.context_type,
                entry.session_id,
                entry.user_id,
                entry.created_at.isoformat(),
                json.dumps(entry.metadata)
            ))
    
    def _add_to_vector_store(self, entry: EmbeddingEntry):
        """Add embedding to FAISS vector store."""
        if self.index is not None:
            # Reshape embedding for FAISS
            embedding_reshaped = entry.embedding.reshape(1, -1).astype('float32')
            self.index.add(embedding_reshaped)
            self.vector_ids.append(entry.id)
    
    def find_similar_contexts(self, 
                             query: str, 
                             context_type: Optional[str] = None,
                             limit: int = 5,
                             min_similarity: Optional[float] = None) -> List[EmbeddingEntry]:
        """
        Find semantically similar contexts.
        
        Args:
            query: Query text to find similar contexts for
            context_type: Optional filter by context type
            limit: Maximum number of results
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar embedding entries
        """
        with self.lock:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            # Use FAISS if available
            if self.index is not None and len(self.vector_ids) > 0:
                return self._search_with_faiss(query_embedding, context_type, limit, min_similarity)
            else:
                return self._search_with_database(query_embedding, context_type, limit, min_similarity)
    
    def _search_with_faiss(self, 
                          query_embedding: np.ndarray,
                          context_type: Optional[str],
                          limit: int,
                          min_similarity: Optional[float]) -> List[EmbeddingEntry]:
        """Search using FAISS vector store."""
        # Reshape query embedding
        query_reshaped = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        scores, indices = self.index.search(query_reshaped, min(limit * 2, len(self.vector_ids)))
        
        # Get results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.vector_ids):
                entry_id = self.vector_ids[idx]
                entry = self._get_embedding_by_id(entry_id)
                if entry and (context_type is None or entry.context_type == context_type):
                    entry.similarity_score = float(score)
                    if min_similarity is None or score >= min_similarity:
                        results.append(entry)
                        if len(results) >= limit:
                            break
        
        # Sort by similarity score
        results.sort(key=lambda x: x.similarity_score or 0, reverse=True)
        return results[:limit]
    
    def _search_with_database(self, 
                             query_embedding: np.ndarray,
                             context_type: Optional[str],
                             limit: int,
                             min_similarity: Optional[float]) -> List[EmbeddingEntry]:
        """Search using database with basic similarity calculation."""
        with sqlite3.connect(self.db_path) as conn:
            # Build query
            query = "SELECT * FROM embeddings"
            params = []
            
            if context_type:
                query += " WHERE context_type = ?"
                params.append(context_type)
            
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit * 3)  # Get more for filtering
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        # Calculate similarities
        results = []
        for row in rows:
            entry = self._row_to_embedding_entry(row)
            if entry:
                similarity = self._calculate_cosine_similarity(query_embedding, entry.embedding)
                entry.similarity_score = similarity
                
                if min_similarity is None or similarity >= min_similarity:
                    results.append(entry)
        
        # Sort by similarity and return top results
        results.sort(key=lambda x: x.similarity_score or 0, reverse=True)
        return results[:limit]
    
    def _calculate_cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception:
            return 0.0
    
    def _get_embedding_by_id(self, entry_id: str) -> Optional[EmbeddingEntry]:
        """Get embedding entry by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM embeddings WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_embedding_entry(row)
            return None
    
    def _row_to_embedding_entry(self, row) -> Optional[EmbeddingEntry]:
        """Convert database row to EmbeddingEntry."""
        try:
            embedding_bytes = row[2]
            embedding = np.frombuffer(embedding_bytes, dtype=np.float64)
            
            return EmbeddingEntry(
                id=row[0],
                text=row[1],
                embedding=embedding,
                context_type=row[3],
                session_id=row[4],
                user_id=row[5],
                created_at=datetime.fromisoformat(row[6]),
                metadata=json.loads(row[7])
            )
        except Exception as e:
            self.logger.error(f"Failed to convert row to EmbeddingEntry: {e}")
            return None
    
    def _cleanup_old_embeddings(self):
        """Remove old embeddings if we exceed the limit."""
        with sqlite3.connect(self.db_path) as conn:
            # Count total embeddings
            cursor = conn.execute("SELECT COUNT(*) FROM embeddings")
            count = cursor.fetchone()[0]
            
            if count > self.max_embeddings:
                # Remove oldest embeddings
                to_remove = count - self.max_embeddings
                cursor = conn.execute("""
                    DELETE FROM embeddings 
                    WHERE id IN (
                        SELECT id FROM embeddings 
                        ORDER BY created_at ASC 
                        LIMIT ?
                    )
                """, (to_remove,))
                
                self.logger.info(f"Cleaned up {to_remove} old embeddings")
    
    def get_embedding_stats(self) -> Dict[str, Any]:
        """Get statistics about the embedding system."""
        with sqlite3.connect(self.db_path) as conn:
            # Get counts by context type
            cursor = conn.execute("""
                SELECT context_type, COUNT(*) 
                FROM embeddings 
                GROUP BY context_type
            """)
            context_counts = dict(cursor.fetchall())
            
            # Get total count
            cursor = conn.execute("SELECT COUNT(*) FROM embeddings")
            total_count = cursor.fetchone()[0]
            
            # Get oldest and newest
            cursor = conn.execute("""
                SELECT MIN(created_at), MAX(created_at) 
                FROM embeddings
            """)
            oldest, newest = cursor.fetchone()
            
            return {
                'total_embeddings': total_count,
                'context_type_counts': context_counts,
                'oldest_embedding': oldest,
                'newest_embedding': newest,
                'vector_store_size': len(self.vector_ids) if self.index else 0,
                'system_stats': self.stats.copy()
            }
    
    def clear_embeddings(self, context_type: Optional[str] = None):
        """Clear all embeddings or by context type."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                if context_type:
                    conn.execute("DELETE FROM embeddings WHERE context_type = ?", (context_type,))
                    self.logger.info(f"Cleared embeddings for context type: {context_type}")
                else:
                    conn.execute("DELETE FROM embeddings")
                    self.logger.info("Cleared all embeddings")
            
            # Reset vector store
            if self.index:
                self.index.reset()
                self.vector_ids.clear()
    
    def export_embeddings(self, 
                         context_type: Optional[str] = None,
                         limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Export embeddings for analysis."""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT * FROM embeddings"
            params = []
            
            if context_type:
                query += " WHERE context_type = ?"
                params.append(context_type)
            
            query += " ORDER BY created_at DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_embedding_entry(row).to_dict() for row in rows if self._row_to_embedding_entry(row)]


# Convenience functions for easy integration
def create_embedding_manager(**kwargs) -> EmbeddingManager:
    """Create a new embedding manager instance."""
    return EmbeddingManager(**kwargs)


def get_embedding_manager_singleton() -> EmbeddingManager:
    """Get or create a singleton embedding manager instance."""
    if not hasattr(get_embedding_manager_singleton, '_instance'):
        get_embedding_manager_singleton._instance = create_embedding_manager()
    return get_embedding_manager_singleton._instance


if __name__ == "__main__":
    # Test the embedding manager
    manager = create_embedding_manager()
    
    # Add some test embeddings
    test_texts = [
        "How to implement embeddings in Python?",
        "What are the best practices for context management?",
        "How to optimize prompt generation?",
        "What is the MCP protocol?",
        "How to implement conversation tracking?"
    ]
    
    for text in test_texts:
        manager.add_embedding(text, "test", metadata={"source": "test"})
    
    # Test similarity search
    results = manager.find_similar_contexts("Python embeddings implementation", limit=3)
    
    print("Similar contexts found:")
    for result in results:
        print(f"- {result.text} (similarity: {result.similarity_score:.3f})")
    
    # Print stats
    print("\nEmbedding stats:")
    stats = manager.get_embedding_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
