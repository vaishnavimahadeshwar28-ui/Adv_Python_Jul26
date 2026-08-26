# Integration Testing

import pytest
import sqlite3
from datetime import datetime
# ===== Integration Test Example =====

class UserRepository:
    """Repository for user data."""
   
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()
   
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()
   
    def create_user(self, name, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
       
        try:
            cursor.execute(
                "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
                (name, email, datetime.now().isoformat())
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Email {email} already exists")
        finally:
            conn.close()
   
    def get_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
       
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "created_at": result[3]
            }
        return None

# ===== Integration Tests =====
@pytest.fixture
def test_db():
    """Create a test database."""
    import tempfile
    import os
   
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    os.unlink(path)  # Clean up
def test_user_repository_create(test_db):
    """Test creating a user."""
    repo = UserRepository(test_db)
    user_id = repo.create_user("Alice", "alice@example.com")
   
    assert user_id is not None
    user = repo.get_user(user_id)
    assert user['name'] == "Alice"
    assert user['email'] == "alice@example.com"
def test_user_repository_unique_email(test_db):
    """Test duplicate email raises error."""
    repo = UserRepository(test_db)
    repo.create_user("Alice", "alice@example.com")
   
    with pytest.raises(ValueError, match="Email alice@example.com already exists"):
        repo.create_user("Bob", "alice@example.com")
def test_user_repository_get_not_found(test_db):
    """Test getting non-existent user."""
    repo = UserRepository(test_db)
    user = repo.get_user(999)
    assert user is None
# ===== Running Tests =====
# python -m pytest P3.py -v