import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fraud_rules import FraudDetector
from menu import run_menu
import csv
from transaction import Transaction


def load_transactions_from_csv(filepath):
    transactions = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            txn = Transaction(
                txn_id=row["txn_id"],
                user_id=row["user_id"],
                amount=row["amount"],
                timestamp=row["timestamp"],
                location=row["location"],
                device_id=row["device_id"],
                merchant=row["merchant"],
            )
            transactions.append(txn)
    return transactions


def main():
    detector = FraudDetector()

    # manually planted blacklist entries
    detector.add_to_blacklist("U999")

    print("Loading transactions...")
    transactions = load_transactions_from_csv("data/transactions.csv")

    print(f"Processing {len(transactions)} transactions through fraud rules...")
    for txn in transactions:
        detector.process(txn)

    print(f"Done. {len(detector.get_flagged())} transaction(s) flagged.\n")

    run_menu(detector)


if __name__ == "__main__":
    main()