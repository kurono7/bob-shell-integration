"""
Database Manager - Secure database operations with prepared statements
"""

import sqlite3
from typing import List, Tuple, Any, Optional
from contextlib import contextmanager


class DatabaseManager:
    """
    Manages database connections and executes queries securely.
    
    Uses prepared statements to prevent SQL injection.
    Implements connection pooling and proper resource management.
    """
    
    def __init__(self, db_path: str = "banking_app.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database schema if not exists"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Login attempts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    username TEXT PRIMARY KEY,
                    failed_attempts INTEGER DEFAULT 0,
                    last_failed_attempt TIMESTAMP
                )
            """)
            
            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Ensures connections are properly closed.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(
        self, 
        query: str, 
        params: Tuple[Any, ...] = ()
    ) -> List[Tuple[Any, ...]]:
        """
        Execute a parameterized query safely.
        
        Args:
            query: SQL query with ? placeholders
            params: Tuple of parameters to bind
            
        Returns:
            List of result tuples
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    
    def execute_many(
        self, 
        query: str, 
        params_list: List[Tuple[Any, ...]]
    ) -> None:
        """
        Execute multiple queries with different parameters.
        
        Args:
            query: SQL query with ? placeholders
            params_list: List of parameter tuples
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()

# Made with Bob
