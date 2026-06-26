"""
Mock customer and transaction data for the Spending Insights demo.

This is synthetic data only — no real customer information is used anywhere
in this codebase. It exists so the chatbot has something realistic to
reason over during the engagement.
"""

from datetime import datetime, timedelta
import random

MOCK_CUSTOMERS = {
    "PEN-10234": {"name": "Aisha Bello", "account_opened": "2023-02-14"},
    "PEN-10891": {"name": "James Whitfield", "account_opened": "2022-11-03"},
    "PEN-11456": {"name": "Priya Shah", "account_opened": "2024-01-22"},
}

_CATEGORIES = [
    "Groceries", "Transport", "Rent", "Utilities", "Dining Out",
    "Subscriptions", "Healthcare", "Entertainment", "Savings Transfer",
]

_MERCHANTS = {
    "Groceries": ["Tesco", "Sainsbury's", "Aldi", "Waitrose"],
    "Transport": ["TfL", "Trainline", "Uber"],
    "Rent": ["Penhallow Properties Ltd"],
    "Utilities": ["British Gas", "Thames Water", "EE Mobile"],
    "Dining Out": ["Deliveroo", "Pret A Manger", "Wagamama"],
    "Subscriptions": ["Netflix", "Spotify", "Amazon Prime"],
    "Healthcare": ["Boots Pharmacy", "NHS Prescription"],
    "Entertainment": ["Cineworld", "Steam"],
    "Savings Transfer": ["Penhallow Savings Pot"],
}


def _generate_transactions(customer_id: str, count: int = 40) -> list[dict]:
    """Deterministically generate plausible transaction history for a customer."""
    random.seed(customer_id)  # deterministic per customer, varies across customers
    transactions = []
    today = datetime.now()

    for i in range(count):
        category = random.choice(_CATEGORIES)
        merchant = random.choice(_MERCHANTS[category])
        days_ago = random.randint(0, 90)
        amount = round(random.uniform(4.50, 180.00), 2)
        if category == "Rent":
            amount = 1250.00
        elif category == "Savings Transfer":
            amount = round(random.uniform(50, 300), 2)

        transactions.append({
            "transaction_id": f"TXN-{customer_id}-{i:04d}",
            "date": (today - timedelta(days=days_ago)).strftime("%Y-%m-%d"),
            "merchant": merchant,
            "category": category,
            "amount": amount,
            "currency": "GBP",
        })

    return sorted(transactions, key=lambda t: t["date"], reverse=True)


def get_customer_transactions(customer_id: str) -> list[dict]:
    """Return the transaction history for a given customer."""
    if customer_id not in MOCK_CUSTOMERS:
        return []
    return _generate_transactions(customer_id)
