import bcrypt
from typing import Optional, Tuple
from utils.database import Database

class User:
    def __init__(self, db: Database):
        self.db = db
        self.id: Optional[int] = None
        self.username: Optional[str] = None
        self.email: Optional[str] = None

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def register(self, username: str, password: str, email: str) -> bool:
        """Register a new user"""
        # Check if username or email already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return False

        # Hash password and create user
        password_hash = self.hash_password(password)
        if self.db.create_user(username, password_hash, email):
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """Login a user"""
        user_data = self.db.get_user_by_username(username)
        if not user_data:
            return False

        # Verify password
        if not self.verify_password(password, user_data[2]):  # password_hash is at index 2
            return False

        # Set user attributes
        self.id = user_data[0]
        self.username = user_data[1]
        self.email = user_data[3]
        return True

    def get_accounts(self) -> list:
        """Get all accounts for the current user"""
        if not self.id:
            return []
        return self.db.get_accounts_by_user_id(self.id)

    def create_account(self, account_type: str, interest_rate: float = 0.0) -> bool:
        """Create a new account for the current user"""
        if not self.id:
            return False
        return self.db.create_account(self.id, account_type, interest_rate)

    def get_user_info(self) -> Optional[Tuple]:
        """Get user information"""
        if not self.username:
            return None
        return self.db.get_user_by_username(self.username) 