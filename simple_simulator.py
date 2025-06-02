import os
import json
import datetime
import random
import hashlib
from pathlib import Path

# Ensure data directory exists
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

users_file = data_dir / "users.json"
transactions_file = data_dir / "transactions.json"
cards_file = data_dir / "cards.json"
bitcoin_file = data_dir / "bitcoin.json"

# Initialize empty data structures if files don't exist
if not users_file.exists():
    with open(users_file, "w") as f:
        json.dump([], f)

if not transactions_file.exists():
    with open(transactions_file, "w") as f:
        json.dump([], f)

if not cards_file.exists():
    with open(cards_file, "w") as f:
        json.dump([], f)

if not bitcoin_file.exists():
    with open(bitcoin_file, "w") as f:
        json.dump([], f)

# Helper functions
def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def generate_id():
    return str(random.randint(10000, 99999))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# User operations
def create_user(username, email, cashtag, password):
    users = load_data(users_file)
    
    # Check if username, email or cashtag already exist
    for user in users:
        if user["username"] == username:
            return False, "Username already exists"
        if user["email"] == email:
            return False, "Email already registered"
        if user["cashtag"] == cashtag:
            return False, "Cashtag already taken"
    
    new_user = {
        "id": generate_id(),
        "username": username,
        "email": email,
        "cashtag": cashtag,
        "password_hash": hash_password(password),
        "balance": 0.0,
        "created_at": timestamp()
    }
    
    users.append(new_user)
    save_data(users_file, users)
    
    # Create a Bitcoin wallet for the user
    create_bitcoin_wallet(new_user["id"])
    
    return True, new_user

def get_user_by_id(user_id):
    users = load_data(users_file)
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def get_user_by_email(email):
    users = load_data(users_file)
    for user in users:
        if user["email"] == email:
            return user
    return None

def verify_password(user, password):
    return user["password_hash"] == hash_password(password)

def update_balance(user_id, amount):
    users = load_data(users_file)
    for user in users:
        if user["id"] == user_id:
            user["balance"] += amount
            save_data(users_file, users)
            return True
    return False

# Transaction operations
def create_transaction(sender_id, receiver_id, amount, note="", transaction_type="payment"):
    transactions = load_data(transactions_file)
    sender = get_user_by_id(sender_id)
    receiver = get_user_by_id(receiver_id)
    
    if not sender or not receiver:
        return False, "User not found"
    
    if sender["balance"] < amount and transaction_type in ["payment", "withdrawal"]:
        return False, "Insufficient funds"
    
    # Update balances
    if transaction_type in ["payment", "withdrawal"]:
        update_balance(sender_id, -amount)
    
    if transaction_type in ["payment", "deposit"]:
        update_balance(receiver_id, amount)
    
    new_transaction = {
        "id": generate_id(),
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "amount": amount,
        "note": note,
        "transaction_type": transaction_type,
        "timestamp": timestamp()
    }
    
    transactions.append(new_transaction)
    save_data(transactions_file, transactions)
    
    return True, new_transaction

def get_user_transactions(user_id):
    transactions = load_data(transactions_file)
    user_transactions = []
    
    for transaction in transactions:
        if transaction["sender_id"] == user_id or transaction["receiver_id"] == user_id:
            user_transactions.append(transaction)
    
    return user_transactions

# Card operations
def add_card(user_id, card_number, card_name, expiry_date, cvv, card_type="debit"):
    cards = load_data(cards_file)
    
    # Check if this is the first card for the user
    is_default = True
    for card in cards:
        if card["user_id"] == user_id:
            is_default = False
            break
    
    new_card = {
        "id": generate_id(),
        "user_id": user_id,
        "card_number": card_number,
        "card_name": card_name,
        "expiry_date": expiry_date,
        "cvv": cvv,
        "card_type": card_type,
        "is_default": is_default,
        "created_at": timestamp()
    }
    
    cards.append(new_card)
    save_data(cards_file, cards)
    
    return True, new_card

def get_user_cards(user_id):
    cards = load_data(cards_file)
    user_cards = []
    
    for card in cards:
        if card["user_id"] == user_id:
            # Mask card number for display
            card["masked_number"] = "*" * 12 + card["card_number"][-4:]
            user_cards.append(card)
    
    return user_cards

def remove_card(card_id, user_id):
    cards = load_data(cards_file)
    was_default = False
    
    for i, card in enumerate(cards):
        if card["id"] == card_id and card["user_id"] == user_id:
            was_default = card["is_default"]
            del cards[i]
            break
    
    # If it was the default card, set another card as default
    if was_default:
        for card in cards:
            if card["user_id"] == user_id:
                card["is_default"] = True
                break
    
    save_data(cards_file, cards)
    return True

# Bitcoin operations
def create_bitcoin_wallet(user_id):
    bitcoin_wallets = load_data(bitcoin_file)
    
    # Check if user already has a wallet
    for wallet in bitcoin_wallets:
        if wallet["user_id"] == user_id:
            return False, "User already has a Bitcoin wallet"
    
    # Generate a fake Bitcoin address for simulation
    address = "bc1q" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=38))
    
    new_wallet = {
        "id": generate_id(),
        "user_id": user_id,
        "btc_balance": 0.0,
        "address": address,
        "created_at": timestamp(),
        "transactions": []
    }
    
    bitcoin_wallets.append(new_wallet)
    save_data(bitcoin_file, bitcoin_wallets)
    
    return True, new_wallet

def get_bitcoin_wallet(user_id):
    bitcoin_wallets = load_data(bitcoin_file)
    
    for wallet in bitcoin_wallets:
        if wallet["user_id"] == user_id:
            return wallet
    
    return None

def get_bitcoin_price():
    # Simulated Bitcoin price (around $30,000)
    base_price = 30000
    return round(base_price + random.uniform(-1000, 1000), 2)

def buy_bitcoin(user_id, usd_amount):
    bitcoin_wallets = load_data(bitcoin_file)
    user = get_user_by_id(user_id)
    
    if not user:
        return False, "User not found"
    
    if user["balance"] < usd_amount:
        return False, "Insufficient funds"
    
    wallet = None
    for w in bitcoin_wallets:
        if w["user_id"] == user_id:
            wallet = w
            break
    
    if not wallet:
        return False, "Bitcoin wallet not found"
    
    # Update user balance
    update_balance(user_id, -usd_amount)
    
    # Calculate Bitcoin amount based on current price
    btc_price = get_bitcoin_price()
    btc_amount = usd_amount / btc_price
    
    # Update Bitcoin wallet
    wallet["btc_balance"] += btc_amount
    
    # Record transaction
    transaction = {
        "id": generate_id(),
        "amount": btc_amount,
        "usd_value": usd_amount,
        "transaction_type": "buy",
        "timestamp": timestamp()
    }
    
    wallet["transactions"].append(transaction)
    save_data(bitcoin_file, bitcoin_wallets)
    
    return True, {"btc_amount": btc_amount, "usd_amount": usd_amount, "btc_price": btc_price}

def sell_bitcoin(user_id, btc_amount):
    bitcoin_wallets = load_data(bitcoin_file)
    
    wallet = None
    for w in bitcoin_wallets:
        if w["user_id"] == user_id:
            wallet = w
            break
    
    if not wallet:
        return False, "Bitcoin wallet not found"
    
    if wallet["btc_balance"] < btc_amount:
        return False, "Insufficient Bitcoin balance"
    
    # Calculate USD amount based on current price
    btc_price = get_bitcoin_price()
    usd_amount = btc_amount * btc_price
    
    # Update Bitcoin wallet
    wallet["btc_balance"] -= btc_amount
    
    # Update user balance
    update_balance(user_id, usd_amount)
    
    # Record transaction
    transaction = {
        "id": generate_id(),
        "amount": btc_amount,
        "usd_value": usd_amount,
        "transaction_type": "sell",
        "timestamp": timestamp()
    }
    
    wallet["transactions"].append(transaction)
    save_data(bitcoin_file, bitcoin_wallets)
    
    return True, {"btc_amount": btc_amount, "usd_amount": usd_amount, "btc_price": btc_price}

# functions
def demo_run():
    print("")
    print("=======================================")
    
    while True:
        print("\nMain Menu:")
        print("1. Create a new user")
        print("2. Log in")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            username = input("Enter your full name: ")
            email = input("Enter your email: ")
            cashtag = input("Enter your cashtag (without the $): ")
            password = input("Enter your password: ")
            
            success, result = create_user(username, email, cashtag, password)
            
            if success:
                print(f"\nAccount created successfully! Welcome {username}!")
                user_menu(result)
            else:
                print(f"\nError: {result}")
        
        elif choice == "2":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            
            user = get_user_by_email(email)
            
            if user and verify_password(user, password):
                print(f"\nWelcome back, {user['username']}!")
                user_menu(user)
            else:
                print("\nInvalid email or password.")
        
        elif choice == "3":
            print("")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

def user_menu(user):
    while True:
        print("\nUser Menu:")
        print(f"Balance: ${user['balance']:.2f}")
        print("\n1. Send money")
        print("2. Add cash")
        print("3. Cash out")
        print("4. Add card")
        print("5. View cards")
        print("6. Bitcoin")
        print("7. View transaction history")
        print("8. Log out")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            # Refresh user data
            user = get_user_by_id(user["id"])
            
            recipient = input("Enter recipient's cashtag or email: ")
            amount = float(input("Enter amount: $"))
            note = input("What's it for? ")
            
            # Find recipient
            recipient_user = None
            users = load_data(users_file)
            
            for u in users:
                if u["cashtag"] == recipient or u["email"] == recipient:
                    recipient_user = u
                    break
            
            if not recipient_user:
                print("\nRecipient not found.")
                continue
            
            if amount <= 0:
                print("\nAmount must be positive.")
                continue
            
            if user["balance"] < amount:
                print("\nInsufficient funds.")
                continue
            
            success, result = create_transaction(user["id"], recipient_user["id"], amount, note)
            
            if success:
                print(f"\nPayment of ${amount:.2f} sent to {recipient_user['username']}!")
            else:
                print(f"\nError: {result}")
        
        elif choice == "2":
            amount = float(input("Enter amount to add: $"))
            
            if amount <= 0:
                print("\nAmount must be positive.")
                continue
            
            success, _ = create_transaction(user["id"], user["id"], amount, "Added cash", "deposit")
            
            if success:
                print(f"\n${amount:.2f} added to your balance!")
                user = get_user_by_id(user["id"])  # Refresh user data
            else:
                print("\nTransaction failed.")
        
        elif choice == "3":
            # Refresh user data
            user = get_user_by_id(user["id"])
            
            amount = float(input("Enter amount to cash out: $"))
            
            if amount <= 0:
                print("\nAmount must be positive.")
                continue
            
            if user["balance"] < amount:
                print("\nInsufficient funds.")
                continue
            
            # Check if user has a card
            cards = get_user_cards(user["id"])
            if not cards:
                print("\nYou need to add a card first.")
                continue
            
            success, _ = create_transaction(user["id"], user["id"], amount, "Cash out", "withdrawal")
            
            if success:
                print(f"\n${amount:.2f} has been cashed out to your default card!")
                user = get_user_by_id(user["id"])  # Refresh user data
            else:
                print("\nTransaction failed.")
        
        elif choice == "4":
            card_number = input("Enter card number (16 digits): ")
            card_name = input("Enter name on card: ")
            expiry_date = input("Enter expiry date (MM/YY): ")
            cvv = input("Enter CVV: ")
            card_type = input("Enter card type (debit/credit): ")
            
            if len(card_number) != 16 or not card_number.isdigit():
                print("\nInvalid card number. Must be 16 digits.")
                continue
            
            if len(cvv) != 3 or not cvv.isdigit():
                print("\nInvalid CVV. Must be 3 digits.")
                continue
            
            success, _ = add_card(user["id"], card_number, card_name, expiry_date, cvv, card_type)
            
            if success:
                print("\nCard added successfully!")
            else:
                print("\nFailed to add card.")
        
        elif choice == "5":
            cards = get_user_cards(user["id"])
            
            if not cards:
                print("\nYou don't have any cards yet.")
                continue
            
            print("\nYour Cards:")
            for i, card in enumerate(cards):
                print(f"{i+1}. {card['card_type'].capitalize()} Card: {card['masked_number']}")
                print(f"   Name: {card['card_name']}")
                print(f"   Expiry: {card['expiry_date']}")
                if card["is_default"]:
                    print("   (Default)")
                print()
        
        elif choice == "6":
            bitcoin_menu(user)
        
        elif choice == "7":
            transactions = get_user_transactions(user["id"])
            
            if not transactions:
                print("\nYou don't have any transactions yet.")
                continue
            
            print("\nTransaction History:")
            for i, transaction in enumerate(transactions):
                sender = get_user_by_id(transaction["sender_id"])
                receiver = get_user_by_id(transaction["receiver_id"])
                
                if transaction["transaction_type"] == "deposit":
                    print(f"{i+1}. Added Cash: +${transaction['amount']:.2f}")
                elif transaction["transaction_type"] == "withdrawal":
                    print(f"{i+1}. Cash Out: -${transaction['amount']:.2f}")
                elif transaction["sender_id"] == user["id"]:
                    print(f"{i+1}. To {receiver['username']}: -${transaction['amount']:.2f}")
                else:
                    print(f"{i+1}. From {sender['username']}: +${transaction['amount']:.2f}")
                
                if transaction["note"]:
                    print(f"   Note: {transaction['note']}")
                
                print(f"   Date: {transaction['timestamp']}")
                print()
        
        elif choice == "8":
            print("\nLogged out successfully.")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

def bitcoin_menu(user):
    wallet = get_bitcoin_wallet(user["id"])
    
    if not wallet:
        print("\nCreating Bitcoin wallet...")
        success, wallet = create_bitcoin_wallet(user["id"])
        
        if not success:
            print(f"\nError: {wallet}")
            return
    
    while True:
        # Refresh wallet data
        wallet = get_bitcoin_wallet(user["id"])
        btc_price = get_bitcoin_price()
        wallet_value_usd = wallet["btc_balance"] * btc_price
        
        print("\nBitcoin Menu:")
        print(f"Bitcoin Balance: ₿{wallet['btc_balance']:.8f}")
        print(f"Current Value: ${wallet_value_usd:.2f}")
        print(f"Current Price: 1 BTC ≈ ${btc_price:.2f}")
        print("\n1. Buy Bitcoin")
        print("2. Sell Bitcoin")
        print("3. View transactions")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            # Refresh user data
            user = get_user_by_id(user["id"])
            
            usd_amount = float(input("Enter amount in USD: $"))
            
            if usd_amount <= 0:
                print("\nAmount must be positive.")
                continue
            
            if user["balance"] < usd_amount:
                print("\nInsufficient funds.")
                continue
            
            success, result = buy_bitcoin(user["id"], usd_amount)
            
            if success:
                print(f"\nSuccessfully purchased ₿{result['btc_amount']:.8f} for ${usd_amount:.2f}!")
                user = get_user_by_id(user["id"])  # Refresh user data
            else:
                print(f"\nError: {result}")
        
        elif choice == "2":
            btc_amount = float(input("Enter amount in BTC: ₿"))
            
            if btc_amount <= 0:
                print("\nAmount must be positive.")
                continue
            
            if wallet["btc_balance"] < btc_amount:
                print("\nInsufficient Bitcoin balance.")
                continue
            
            success, result = sell_bitcoin(user["id"], btc_amount)
            
            if success:
                print(f"\nSuccessfully sold ₿{btc_amount:.8f} for ${result['usd_amount']:.2f}!")
                user = get_user_by_id(user["id"])  # Refresh user data
            else:
                print(f"\nError: {result}")
        
        elif choice == "3":
            if not wallet["transactions"]:
                print("\nYou don't have any Bitcoin transactions yet.")
                continue
            
            print("\nBitcoin Transactions:")
            for i, transaction in enumerate(wallet["transactions"]):
                if transaction["transaction_type"] == "buy":
                    print(f"{i+1}. Bought: +₿{transaction['amount']:.8f}")
                else:
                    print(f"{i+1}. Sold: -₿{transaction['amount']:.8f}")
                
                print(f"   USD Value: ${transaction['usd_value']:.2f}")
                print(f"   Date: {transaction['timestamp']}")
                print()
        
        elif choice == "4":
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    # Start the demo
    demo_run()