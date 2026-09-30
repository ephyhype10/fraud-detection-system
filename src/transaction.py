from datetime import datetime


class Transaction:
    """
    Represents a single bank transfer: money moving from sender to receiver.
    This is the 'edge' in the transaction graph.
    """

    def __init__(self, txn_id, sender, receiver, amount, timestamp):
        self.txn_id = txn_id
        self.sender = sender
        self.receiver = receiver
        self.amount = float(amount)
        self.timestamp = timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(timestamp)

        self.risk_score = 0
        self.flags = []

    def is_flagged(self):
        return self.risk_score >= 50

    def to_dict(self):
        return {
            "txn_id": self.txn_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "risk_score": self.risk_score,
            "flags": self.flags,
        }

    def __repr__(self):
        return (f"Transaction(id={self.txn_id}, {self.sender}->{self.receiver}, "
                f"amount={self.amount}, risk={self.risk_score}, flags={self.flags})")


if __name__ == "__main__":
    t = Transaction("T001", "U001", "U002", 15000, "2025-01-15T10:30:00")
    print(t)
    print(t.to_dict())