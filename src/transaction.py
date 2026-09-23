from datetime import datetime


class Transaction:
    """
    Represents a single financial transaction.

    Attributes:
        txn_id (str): Unique transaction identifier
        user_id (str): ID of the user who made the transaction
        amount (float): Transaction amount
        timestamp (datetime): When the transaction occurred
        location (str): City/region where the transaction happened
        device_id (str): Device used to make the transaction
        merchant (str): Merchant/vendor name
    """

    def __init__(self, txn_id, user_id, amount, timestamp, location, device_id, merchant):
        self.txn_id = txn_id
        self.user_id = user_id
        self.amount = float(amount)
        self.timestamp = timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(timestamp)
        self.location = location
        self.device_id = device_id
        self.merchant = merchant

        # filled in later by fraud_rules.py
        self.risk_score = 0
        self.flags = []  # list of reasons this txn was flagged, e.g. ["blacklist", "velocity"]

    def is_flagged(self):
        return self.risk_score >= 50

    def to_dict(self):
        return {
            "txn_id": self.txn_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "device_id": self.device_id,
            "merchant": self.merchant,
            "risk_score": self.risk_score,
            "flags": self.flags,
        }

    def __repr__(self):
        return (f"Transaction(id={self.txn_id}, user={self.user_id}, "
                f"amount={self.amount}, risk={self.risk_score}, flags={self.flags})")


if __name__ == "__main__":
    # quick sanity check
    t = Transaction(
        txn_id="T001",
        user_id="U001",
        amount=15000,
        timestamp="2025-01-15T10:30:00",
        location="Coimbatore",
        device_id="D001",
        merchant="Amazon"
    )
    print(t)
    print(t.to_dict())