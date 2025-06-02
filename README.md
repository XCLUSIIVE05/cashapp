# Cash App Simulator

A faithful replica of Cash App with simulated functionality for sending payments, managing debit cards, and trading Bitcoin.

## Features

- **User Authentication**: Create an account with email, password, and your unique $Cashtag
- **Payment Simulation**: Send and request money from other users
- **Banking Features**: Add virtual debit/credit cards and manage your balance
- **Bitcoin Trading**: Buy and sell Bitcoin with simulated market prices
- **Accurate Design**: Replicates Cash App's distinctive user interface, colors, and typography

## Technology Stack

- **Backend**: Flask web framework with Python
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Design**: Custom CSS designed to match Cash App's visual style

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```cd cash_app_simulator
   
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python run.py
   ```
5. Access the application at `http://localhost:5000`

## Security Notice

This is a **simulation only**. It does not process real financial transactions or connect to actual payment systems. The app stores card details in plain text for demonstration purposes. In a real application, proper encryption and security measures would be implemented.

## Disclaimer

This project is not affiliated with Cash App or Block, Inc. It's created for educational and demonstration purposes only.