from typing import Optional, List, Tuple
from decimal import Decimal
from utils.database import Database

class Account:
    def __init__(self, db: Database):
        self.db = db
        self.id: Optional[int] = None
        self.user_id: Optional[int] = None
        self.account_type: Optional[str] = None
        self.balance: Decimal = Decimal('0.00')
        self.interest_rate: Decimal = Decimal('0.00')

    def load_account(self, account_id: int) -> bool:
        """Load account data from database"""
        accounts = self.db.get_accounts_by_user_id(account_id)
        if not accounts:
            return False
        
        account_data = accounts[0]
        self.id = account_data[0]
        self.user_id = account_data[1]
        self.account_type = account_data[2]
        self.balance = Decimal(str(account_data[3]))
        self.interest_rate = Decimal(str(account_data[4]))
        return True

    def deposit(self, amount: Decimal, description: str = "Deposit") -> bool:
        """Deposit money into the account"""
        if amount <= 0:
            return False

        if self.db.update_balance(self.id, float(amount)):
            self.balance += amount
            self.db.add_transaction(self.id, "DEPOSIT", float(amount), description)
            return True
        return False

    def withdraw(self, amount: Decimal, description: str = "Withdrawal") -> bool:
        """Withdraw money from the account"""
        if amount <= 0 or amount > self.balance:
            return False

        if self.db.update_balance(self.id, float(-amount)):
            self.balance -= amount
            self.db.add_transaction(self.id, "WITHDRAWAL", float(-amount), description)
            return True
        return False

    def transfer(self, target_account: 'Account', amount: Decimal, description: str = "Transfer") -> bool:
        """Transfer money to another account"""
        if amount <= 0 or amount > self.balance:
            return False

        # Start transaction
        if self.withdraw(amount, f"Transfer to {target_account.id}"):
            if target_account.deposit(amount, f"Transfer from {self.id}"):
                return True
            # If deposit fails, reverse the withdrawal
            self.deposit(amount, "Transfer reversal")
        return False

    def get_transactions(self) -> List[Tuple]:
        """Get transaction history for the account"""
        if not self.id:
            return []
        return self.db.get_transactions_by_account(self.id)

    def calculate_interest(self) -> Decimal:
        """Calculate interest for the account"""
        if self.account_type.lower() == "savings":
            return self.balance * (self.interest_rate / Decimal('100'))
        return Decimal('0.00')

    def apply_interest(self) -> bool:
        """Apply interest to the account"""
        interest = self.calculate_interest()
        if interest > 0:
            return self.deposit(interest, "Interest payment")
        return True 