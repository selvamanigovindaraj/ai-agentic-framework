"""Episodic Memory using SQLite"""
from typing import List, Dict, Any
import sqlite3
import json
from datetime import datetime
from agentic_framework.core.memory import MemoryProvider

class EpisodicMemory(MemoryProvider):
    """Episodic memory using SQLite for time-series events"""
    
    def __init__(self, db_path: str = "episodic_memory.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    agent_id TEXT,
                    task TEXT,
                    content TEXT,
                    type TEXT
                )
            """)
            
    async def store(self, memory: Dict[str, Any]) -> None:
        """Log an episode"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO episodes (timestamp, agent_id, task, content, type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                memory.get("agent_id", "unknown"),
                memory.get("task", ""),
                json.dumps(memory.get("content", {})),
                memory.get("type", "experience")
            ))
            
    async def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve recent episodes (simple time-based)"""
        # Note: 'query' is ignored in this simple implementation, acts as 'get recent'
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT timestamp, agent_id, task, content, type 
                FROM episodes 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (k,))
            
            results = []
            for row in cursor:
                results.append({
                    "timestamp": row[0],
                    "agent_id": row[1],
                    "task": row[2],
                    "content": json.loads(row[3]),
                    "type": row[4]
                })
            return results
