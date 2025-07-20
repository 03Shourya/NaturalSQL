#!/usr/bin/env python3
"""
🏢 NaturalSQL Enterprise Features
================================
Enterprise-grade features for production deployment.
"""

import json
import logging
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
import sqlite3

class EnterpriseFeatures:
    """Enterprise features for NaturalSQL"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.setup_database()
        self.rate_limit_cache = {}
        self.api_keys = {}
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "logging": {
                "level": "INFO",
                "file": "naturalsql.log",
                "max_size": "10MB",
                "backup_count": 5
            },
            "authentication": {
                "enabled": True,
                "session_timeout": 3600,
                "max_failed_attempts": 5
            },
            "rate_limiting": {
                "enabled": True,
                "requests_per_minute": 60,
                "requests_per_hour": 1000
            },
            "api": {
                "enabled": True,
                "version": "1.0",
                "documentation": True
            }
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get("logging", {})
        
        logging.basicConfig(
            level=getattr(logging, log_config.get("level", "INFO")),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_config.get("file", "naturalsql.log")),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("NaturalSQL")
        self.logger.info("Enterprise features initialized")
    
    def setup_database(self):
        """Setup enterprise database tables"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # API keys table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    api_key TEXT UNIQUE NOT NULL,
                    name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Query history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    natural_query TEXT NOT NULL,
                    generated_sql TEXT NOT NULL,
                    execution_time REAL,
                    success BOOLEAN,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Rate limiting table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rate_limits (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    endpoint TEXT,
                    request_count INTEGER DEFAULT 0,
                    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("Enterprise database tables created")
            
        except Exception as e:
            self.logger.error(f"Failed to setup enterprise database: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, email: str = None, role: str = "user") -> bool:
        """Create a new user"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, role)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, email, role))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"User created: {username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create user {username}: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, email, role, is_active
                FROM users
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user[0],))
                
                conn.commit()
                
                user_data = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[3]
                }
                
                self.logger.info(f"User authenticated: {username}")
                return user_data
            
            conn.close()
            return None
            
        except Exception as e:
            self.logger.error(f"Authentication failed for {username}: {e}")
            return None
    
    def generate_api_key(self, user_id: int, name: str = "Default") -> Optional[str]:
        """Generate API key for user"""
        try:
            api_key = secrets.token_urlsafe(32)
            
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO api_keys (user_id, api_key, name)
                VALUES (?, ?, ?)
            ''', (user_id, api_key, name))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"API key generated for user {user_id}")
            return api_key
            
        except Exception as e:
            self.logger.error(f"Failed to generate API key: {e}")
            return None
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate API key"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT u.id, u.username, u.email, u.role, ak.name
                FROM api_keys ak
                JOIN users u ON ak.user_id = u.id
                WHERE ak.api_key = ? AND ak.is_active = 1 AND u.is_active = 1
            ''', (api_key,))
            
            user = cursor.fetchone()
            
            if user:
                # Update last used
                cursor.execute('''
                    UPDATE api_keys SET last_used = CURRENT_TIMESTAMP
                    WHERE api_key = ?
                ''', (api_key,))
                
                conn.commit()
                
                user_data = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[3],
                    "api_key_name": user[4]
                }
                
                return user_data
            
            conn.close()
            return None
            
        except Exception as e:
            self.logger.error(f"API key validation failed: {e}")
            return None
    
    def check_rate_limit(self, user_id: int, endpoint: str = "default") -> bool:
        """Check rate limit for user"""
        if not self.config.get("rate_limiting", {}).get("enabled", True):
            return True
        
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            # Get current window
            window_start = datetime.now().replace(second=0, microsecond=0)
            
            cursor.execute('''
                SELECT request_count, window_start
                FROM rate_limits
                WHERE user_id = ? AND endpoint = ?
                ORDER BY window_start DESC
                LIMIT 1
            ''', (user_id, endpoint))
            
            record = cursor.fetchone()
            
            if record:
                count, stored_window = record
                stored_window = datetime.fromisoformat(stored_window)
                
                # Check if in same window
                if stored_window == window_start:
                    if count >= self.config["rate_limiting"]["requests_per_minute"]:
                        conn.close()
                        return False
                    else:
                        # Increment count
                        cursor.execute('''
                            UPDATE rate_limits
                            SET request_count = request_count + 1
                            WHERE user_id = ? AND endpoint = ? AND window_start = ?
                        ''', (user_id, endpoint, stored_window))
                else:
                    # New window
                    cursor.execute('''
                        INSERT INTO rate_limits (user_id, endpoint, request_count, window_start)
                        VALUES (?, ?, 1, ?)
                    ''', (user_id, endpoint, window_start))
            else:
                # First request
                cursor.execute('''
                    INSERT INTO rate_limits (user_id, endpoint, request_count, window_start)
                    VALUES (?, ?, 1, ?)
                ''', (user_id, endpoint, window_start))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Rate limit check failed: {e}")
            return True  # Allow on error
    
    def log_query(self, user_id: int, natural_query: str, generated_sql: str, 
                  execution_time: float = None, success: bool = True):
        """Log query to history"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO query_history (user_id, natural_query, generated_sql, execution_time, success)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, natural_query, generated_sql, execution_time, success))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Query logged for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to log query: {e}")
    
    def get_query_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get query history for user"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT natural_query, generated_sql, execution_time, success, timestamp
                FROM query_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    "natural_query": row[0],
                    "generated_sql": row[1],
                    "execution_time": row[2],
                    "success": row[3],
                    "timestamp": row[4]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            self.logger.error(f"Failed to get query history: {e}")
            return []
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        try:
            conn = sqlite3.connect('enterprise.db')
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            total_users = cursor.fetchone()[0]
            
            # Total queries
            cursor.execute("SELECT COUNT(*) FROM query_history")
            total_queries = cursor.fetchone()[0]
            
            # Successful queries
            cursor.execute("SELECT COUNT(*) FROM query_history WHERE success = 1")
            successful_queries = cursor.fetchone()[0]
            
            # Active API keys
            cursor.execute("SELECT COUNT(*) FROM api_keys WHERE is_active = 1")
            active_api_keys = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_users": total_users,
                "total_queries": total_queries,
                "successful_queries": successful_queries,
                "success_rate": (successful_queries / total_queries * 100) if total_queries > 0 else 0,
                "active_api_keys": active_api_keys
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system stats: {e}")
            return {}

# Decorators for enterprise features
def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'current_user') or not self.current_user:
            raise Exception("Authentication required")
        return f(self, *args, **kwargs)
    return wrapper

def rate_limited(f):
    """Decorator to apply rate limiting"""
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'current_user') and self.current_user:
            if not self.enterprise.check_rate_limit(self.current_user['id']):
                raise Exception("Rate limit exceeded")
        return f(self, *args, **kwargs)
    return wrapper

def log_query(f):
    """Decorator to log queries"""
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        try:
            result = f(self, *args, **kwargs)
            execution_time = time.time() - start_time
            
            if hasattr(self, 'current_user') and self.current_user:
                self.enterprise.log_query(
                    self.current_user['id'],
                    args[0] if args else "",
                    result,
                    execution_time,
                    True
                )
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            
            if hasattr(self, 'current_user') and self.current_user:
                self.enterprise.log_query(
                    self.current_user['id'],
                    args[0] if args else "",
                    str(e),
                    execution_time,
                    False
                )
            
            raise e
    return wrapper 