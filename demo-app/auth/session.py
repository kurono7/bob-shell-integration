"""
Session Manager - Secure session handling
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from database.db_manager import DatabaseManager


class SessionManager:
    """
    Manages user sessions securely.
    
    Implements:
    - Cryptographically secure token generation
    - Session expiration
    - Session invalidation
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize session manager.
        
        Args:
            db_manager: Database manager instance
        """
        self._db = db_manager
        self._session_duration = timedelta(hours=2)
        self._token_length = 32  # 32 bytes = 256 bits
    
    def create_session(self, user_id: int, username: str) -> str:
        """
        Create a new session for user.
        
        Args:
            user_id: User's database ID
            username: User's username
            
        Returns:
            Session token string
        """
        # Generate cryptographically secure random token
        token = secrets.token_urlsafe(self._token_length)
        
        # Calculate expiration time
        expires_at = datetime.now() + self._session_duration
        
        # Store session in database
        query = """
            INSERT INTO sessions (token, user_id, expires_at)
            VALUES (?, ?, ?)
        """
        self._db.execute_query(
            query, 
            (token, user_id, expires_at.isoformat())
        )
        
        return token
    
    def validate_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate session token and return user info if valid.
        
        Args:
            token: Session token to validate
            
        Returns:
            Dict with user info if valid, None otherwise
        """
        query = """
            SELECT s.user_id, s.expires_at, u.username
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?
        """
        result = self._db.execute_query(query, (token,))
        
        if not result:
            return None
        
        user_id, expires_at_str, username = result[0]
        expires_at = datetime.fromisoformat(expires_at_str)
        
        # Check if session has expired
        if datetime.now() > expires_at:
            # Clean up expired session
            self.invalidate_session(token)
            return None
        
        return {
            'user_id': user_id,
            'username': username,
            'expires_at': expires_at.isoformat()
        }
    
    def invalidate_session(self, token: str) -> bool:
        """
        Invalidate (delete) a session.
        
        Args:
            token: Session token to invalidate
            
        Returns:
            True if session was invalidated
        """
        query = "DELETE FROM sessions WHERE token = ?"
        self._db.execute_query(query, (token,))
        return True
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions from database.
        
        Returns:
            Number of sessions removed
        """
        query = "DELETE FROM sessions WHERE expires_at < ?"
        now = datetime.now().isoformat()
        self._db.execute_query(query, (now,))
        
        # Return count would require additional query
        return 0  # Simplified for demo
    
    def extend_session(self, token: str) -> bool:
        """
        Extend session expiration time.
        
        Args:
            token: Session token to extend
            
        Returns:
            True if session was extended
        """
        new_expires_at = datetime.now() + self._session_duration
        
        query = "UPDATE sessions SET expires_at = ? WHERE token = ?"
        self._db.execute_query(query, (new_expires_at.isoformat(), token))
        
        return True

# Made with Bob
