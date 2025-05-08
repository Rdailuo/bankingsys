# Banking System

Hi there! This is a secure and feature-rich banking system implemented in Python. This project demonstrates core banking operations with a focus on security and best practices.

## Features

- User account management (create, update, delete)
- Secure login system with password hashing
- Multiple account types (Savings, Checking)
- Transaction management (deposit, withdraw, transfer)
- Transaction history
- Balance inquiry
- Interest calculation for savings accounts
- Data persistence using SQLite
- Input validation and error handling

## Requirements

- Python 3.8+
- Required packages (install using `pip install -r requirements.txt`):
  - bcrypt
  - tabulate
  - colorama

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-system.git
cd banking-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Project Structure

```
banking-system/
├── main.py                 # Main application entry point
├── models/
│   ├── __init__.py
│   ├── user.py            # User model and authentication
│   ├── account.py         # Account management
│   └── transaction.py     # Transaction handling
├── utils/
│   ├── __init__.py
│   ├── database.py        # Database operations
│   └── validators.py      # Input validation
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Security Features

- Password hashing using bcrypt
- Input sanitization
- Transaction validation
- Secure session management

## Usage

1. Create a new account
2. Login with your credentials
3. Perform banking operations:
   - Check balance
   - Deposit money
   - Withdraw money
   - Transfer funds
   - View transaction history

## Contributing

Feel free to submit issues and enhancement requests!

Author: Reyna Dai
