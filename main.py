import os
from decimal import Decimal
from colorama import init, Fore, Style
from tabulate import tabulate
from utils.database import Database
from models.user import User
from models.account import Account

# Initialize colorama
init()

class BankingSystem:
    def __init__(self):
        self.db = Database()
        self.user = User(self.db)
        self.current_account = None

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str):
        """Print a formatted header"""
        self.clear_screen()
        print(f"{Fore.CYAN}{'=' * 50}")
        print(f"{title.center(50)}")
        print(f"{'=' * 50}{Style.RESET_ALL}\n")

    def get_input(self, prompt: str, password: bool = False) -> str:
        """Get user input with proper formatting"""
        if password:
            import getpass
            return getpass.getpass(prompt)
        return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")

    def register(self):
        """Handle user registration"""
        self.print_header("User Registration")
        
        username = self.get_input("Enter username: ")
        password = self.get_input("Enter password: ", password=True)
        email = self.get_input("Enter email: ")

        if self.user.register(username, password, email):
            print(f"\n{Fore.GREEN}Registration successful!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Registration failed. Username or email may already exist.{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")

    def login(self):
        """Handle user login"""
        self.print_header("User Login")
        
        username = self.get_input("Enter username: ")
        password = self.get_input("Enter password: ", password=True)

        if self.user.login(username, password):
            print(f"\n{Fore.GREEN}Login successful!{Style.RESET_ALL}")
            self.show_account_menu()
        else:
            print(f"\n{Fore.RED}Login failed. Invalid username or password.{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")

    def create_account(self):
        """Create a new account"""
        self.print_header("Create New Account")
        
        print("Account Types:")
        print("1. Savings (2.5% interest)")
        print("2. Checking (No interest)")
        
        choice = self.get_input("Select account type (1-2): ")
        
        if choice == "1":
            account_type = "Savings"
            interest_rate = 2.5
        elif choice == "2":
            account_type = "Checking"
            interest_rate = 0.0
        else:
            print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            return

        if self.user.create_account(account_type, interest_rate):
            print(f"\n{Fore.GREEN}Account created successfully!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Failed to create account.{Style.RESET_ALL}")

    def show_accounts(self):
        """Display user's accounts"""
        accounts = self.user.get_accounts()
        if not accounts:
            print(f"\n{Fore.YELLOW}No accounts found.{Style.RESET_ALL}")
            return

        headers = ["ID", "Type", "Balance", "Interest Rate"]
        table_data = [[acc[0], acc[2], f"${acc[3]:.2f}", f"{acc[4]}%"] for acc in accounts]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

    def select_account(self):
        """Select an account to operate on"""
        self.show_accounts()
        account_id = self.get_input("\nEnter account ID: ")
        
        try:
            account_id = int(account_id)
            self.current_account = Account(self.db)
            if not self.current_account.load_account(account_id):
                print(f"\n{Fore.RED}Invalid account ID.{Style.RESET_ALL}")
                self.current_account = None
        except ValueError:
            print(f"\n{Fore.RED}Invalid account ID.{Style.RESET_ALL}")
            self.current_account = None

    def deposit(self):
        """Handle deposit operation"""
        if not self.current_account:
            print(f"\n{Fore.RED}No account selected.{Style.RESET_ALL}")
            return

        try:
            amount = Decimal(self.get_input("Enter amount to deposit: $"))
            if self.current_account.deposit(amount):
                print(f"\n{Fore.GREEN}Deposit successful!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Deposit failed. Invalid amount.{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}Invalid amount.{Style.RESET_ALL}")

    def withdraw(self):
        """Handle withdrawal operation"""
        if not self.current_account:
            print(f"\n{Fore.RED}No account selected.{Style.RESET_ALL}")
            return

        try:
            amount = Decimal(self.get_input("Enter amount to withdraw: $"))
            if self.current_account.withdraw(amount):
                print(f"\n{Fore.GREEN}Withdrawal successful!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Withdrawal failed. Invalid amount or insufficient funds.{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}Invalid amount.{Style.RESET_ALL}")

    def transfer(self):
        """Handle transfer operation"""
        if not self.current_account:
            print(f"\n{Fore.RED}No account selected.{Style.RESET_ALL}")
            return

        try:
            target_id = int(self.get_input("Enter target account ID: "))
            amount = Decimal(self.get_input("Enter amount to transfer: $"))
            
            target_account = Account(self.db)
            if not target_account.load_account(target_id):
                print(f"\n{Fore.RED}Invalid target account.{Style.RESET_ALL}")
                return

            if self.current_account.transfer(target_account, amount):
                print(f"\n{Fore.GREEN}Transfer successful!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Transfer failed. Invalid amount or insufficient funds.{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}Invalid input.{Style.RESET_ALL}")

    def show_transactions(self):
        """Display account transactions"""
        if not self.current_account:
            print(f"\n{Fore.RED}No account selected.{Style.RESET_ALL}")
            return

        transactions = self.current_account.get_transactions()
        if not transactions:
            print(f"\n{Fore.YELLOW}No transactions found.{Style.RESET_ALL}")
            return

        headers = ["Date", "Type", "Amount", "Description"]
        table_data = [[t[5], t[2], f"${t[3]:.2f}", t[4]] for t in transactions]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

    def show_account_menu(self):
        """Display and handle account operations menu"""
        while True:
            self.print_header("Account Operations")
            print(f"Current Account: {self.current_account.id if self.current_account else 'None'}")
            print("\n1. Create New Account")
            print("2. Select Account")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Transfer")
            print("6. View Transactions")
            print("7. Show All Accounts")
            print("8. Logout")
            
            choice = self.get_input("\nSelect operation (1-8): ")
            
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.select_account()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.withdraw()
            elif choice == "5":
                self.transfer()
            elif choice == "6":
                self.show_transactions()
            elif choice == "7":
                self.show_accounts()
            elif choice == "8":
                break
            else:
                print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            
            input("\nPress Enter to continue...")

    def show_main_menu(self):
        """Display and handle main menu"""
        while True:
            self.print_header("Banking System")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = self.get_input("\nSelect option (1-3): ")
            
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print(f"\n{Fore.YELLOW}Thank you for using the Banking System!{Style.RESET_ALL}")
                break
            else:
                print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            
            input("\nPress Enter to continue...")

def main():
    banking_system = BankingSystem()
    banking_system.show_main_menu()

if __name__ == "__main__":
    main() 