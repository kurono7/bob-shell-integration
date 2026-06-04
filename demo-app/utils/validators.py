"""
Input Validation Module - Secure input validation
"""

import re
from typing import Optional


class InputValidator:
    """
    Validates user inputs to prevent injection attacks and ensure data quality.
    
    Implements whitelist-based validation following OWASP guidelines.
    """
    
    # Regex patterns for validation
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    
    def validate_username(self, username: str) -> bool:
        """
        Validate username format.
        
        Rules:
        - 3-20 characters
        - Only alphanumeric and underscore
        - No special characters
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not username:
            return False
        
        return bool(self.USERNAME_PATTERN.match(username))
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email:
            return False
        
        return bool(self.EMAIL_PATTERN.match(email))
    
    def validate_password_strength(self, password: str) -> bool:
        """
        Validate password strength.
        
        Requirements:
        - 8-128 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
            
        Returns:
            True if strong enough, False otherwise
        """
        if not password:
            return False
        
        # Check length
        if len(password) < self.MIN_PASSWORD_LENGTH or len(password) > self.MAX_PASSWORD_LENGTH:
            return False
        
        # Check for required character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    def sanitize_string(self, input_str: str, max_length: int = 255) -> str:
        """
        Sanitize string input by removing potentially dangerous characters.
        
        Args:
            input_str: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_str:
            return ""
        
        # Remove null bytes
        sanitized = input_str.replace('\x00', '')
        
        # Trim to max length
        sanitized = sanitized[:max_length]
        
        # Remove leading/trailing whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    def validate_numeric(
        self, 
        value: str, 
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> bool:
        """
        Validate numeric input.
        
        Args:
            value: String value to validate
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            
        Returns:
            True if valid number within range, False otherwise
        """
        try:
            num = float(value)
            
            if min_value is not None and num < min_value:
                return False
            
            if max_value is not None and num > max_value:
                return False
            
            return True
        except (ValueError, TypeError):
            return False

# Made with Bob
