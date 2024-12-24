import json
import os
from tinydb import TinyDB, Query

def create_db(file_path):
    """Create a new database file or load an existing one"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def insert_analysis(db, analysis):
    """Insert analysis into the database"""
    symbol = analysis.get("symbol")
    if symbol:
        db[symbol] = analysis
        with open("analysis_results.json", 'w') as file:
            json.dump(db, file, indent=2)

def track_holdings(db, order):
    """Track current holdings and profit/loss"""
    symbol = order['symbol']
    amount_to_buy = order['amount_to_buy']
    price = order['price']
    
    holdings = db.table('holdings')
    holding = holdings.get(Query().symbol == symbol)
    
    if holding:
        # Update existing holding
        new_amount = holding['amount'] + amount_to_buy
        new_total_cost = holding['total_cost'] + (amount_to_buy * price)
        holdings.update({'amount': new_amount, 'total_cost': new_total_cost}, Query().symbol == symbol)
    else:
        # Insert new holding
        holdings.insert({'symbol': symbol, 'amount': amount_to_buy, 'total_cost': amount_to_buy * price})

def get_holdings(db):
    """Get current holdings"""
    holdings = db.table('holdings')
    return holdings.all()

def get_profit_loss(db):
    """Calculate profit/loss for each holding"""
    holdings = db.table('holdings')
    profit_loss = {}
    
    for holding in holdings:
        symbol = holding['symbol']
        amount = holding['amount']
        total_cost = holding['total_cost']
        
        # Get current price
        analysis = db.table('analysis').get(Query().symbol == symbol)
        current_price = analysis['market_context']['price_action']['current_price']
        
        # Calculate profit/loss
        current_value = amount * current_price
        profit_loss[symbol] = current_value - total_cost
    
    return profit_loss
