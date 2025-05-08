import sqlite3
from typing import Optional, List, Tuple
import os

class Database:
    def __init__(self, db_name: str = "banking.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        """Create necessary tables if they don't exist"""
        self.connect()
        
        # Create users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create accounts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_type TEXT NOT NULL,
                balance DECIMAL(10,2) DEFAULT 0.00,
                interest_rate DECIMAL(5,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Create transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        ''')

        self.conn.commit()
        self.close()

    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[Tuple]]:
        """Execute a query and return results"""
        try:
            self.connect()
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            self.conn.commit()
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.close()

    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = ?"
        result = self.execute_query(query, (username,))
        return result[0] if result else None

    def create_user(self, username: str, password_hash: str, email: str) -> bool:
        """Create a new user"""
        query = "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)"
        try:
            self.execute_query(query, (username, password_hash, email))
            return True
        except sqlite3.Error:
            return False

    def create_account(self, user_id: int, account_type: str, interest_rate: float = 0.0) -> bool:
        """Create a new account for a user"""
        query = "INSERT INTO accounts (user_id, account_type, interest_rate) VALUES (?, ?, ?)"
        try:
            self.execute_query(query, (user_id, account_type, interest_rate))
            return True
        except sqlite3.Error:
            return False

    def get_accounts_by_user_id(self, user_id: int) -> List[Tuple]:
        """Get all accounts for a user"""
        query = "SELECT * FROM accounts WHERE user_id = ?"
        return self.execute_query(query, (user_id,)) or []

    def update_balance(self, account_id: int, amount: float) -> bool:
        """Update account balance"""
        query = "UPDATE accounts SET balance = balance + ? WHERE id = ?"
        try:
            self.execute_query(query, (amount, account_id))
            return True
        except sqlite3.Error:
            return False

    def add_transaction(self, account_id: int, transaction_type: str, amount: float, description: str = "") -> bool:
        """Add a new transaction"""
        query = "INSERT INTO transactions (account_id, transaction_type, amount, description) VALUES (?, ?, ?, ?)"
        try:
            self.execute_query(query, (account_id, transaction_type, amount, description))
            return True
        except sqlite3.Error:
            return False

    def get_transactions_by_account(self, account_id: int) -> List[Tuple]:
        """Get all transactions for an account"""
        query = "SELECT * FROM transactions WHERE account_id = ? ORDER BY created_at DESC"
        return self.execute_query(query, (account_id,)) or [] 