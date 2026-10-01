import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import csv
from transaction import Transaction
from fraud_detection import FraudDetector


def load_transactions_from_csv(filepath):
    transactions = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            txn = Transaction(
                txn_id=row["txn_id"],
                sender=row["sender"],
                receiver=row["receiver"],
                amount=row["amount"],
                timestamp=row["timestamp"],
            )
            transactions.append(txn)
    return transactions


def main():
    detector = FraudDetector()
    detector.add_to_blacklist("U999")

    print("Loading transactions...")
    transactions = load_transactions_from_csv("data/transactions.csv")

    print(f"Processing {len(transactions)} transactions...")
    for txn in transactions:
        detector.process(txn)

    print(f"Done. {len(detector.get_flagged())} transaction(s) flagged.\n")

    print("--- Flagged transactions ---")
    for t in detector.get_flagged():
        print(" ", t)

    print("\n--- Connected user groups ---")
    for group in detector.get_connected_groups():
        print(" ", group)

    print("\n--- Money loop check ---")
    if detector.has_money_loop():
        print("ALERT: circular transfer detected:", detector.get_money_loop())
    else:
        print("No circular transfers found.")

    print("\n--- Shortest chain example: U001 -> U005 ---")
    path, total = detector.find_chain("U001", "U005")
    if path:
        print("Path:", path, "| Total amount:", total)
    else:
        print("No path found between U001 and U005.")


if __name__ == "__main__":
    main()