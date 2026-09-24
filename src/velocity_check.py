from collections import deque, defaultdict


class VelocityChecker:
    """
    Tracks recent transaction timestamps per user using a sliding window (deque).
    Flags a user if they exceed a transaction limit within a time window.
    """

    def __init__(self, limit=3, window_seconds=300):
        self.limit = limit                    # max allowed transactions in the window
        self.window_seconds = window_seconds  # window size, default 5 minutes
        self.windows = defaultdict(deque)     # user_id -> deque of recent timestamps

    def check(self, user_id, timestamp):
        """
        Records this transaction's timestamp and returns True if the user
        has exceeded the velocity limit (i.e., this transaction is suspicious).
        """
        window = self.windows[user_id]

        # drop timestamps that have fallen outside the window
        while window and (timestamp - window[0]).total_seconds() > self.window_seconds:
            window.popleft()

        window.append(timestamp)

        return len(window) > self.limit

    def count_in_window(self, user_id):
        """How many transactions this user currently has inside the active window."""
        return len(self.windows[user_id])


if __name__ == "__main__":
    from datetime import datetime, timedelta

    checker = VelocityChecker(limit=3, window_seconds=300)  # max 3 per 5 min

    base_time = datetime(2025, 1, 15, 10, 0, 0)

    # simulate 5 rapid transactions from the same user, 1 minute apart
    for i in range(5):
        ts = base_time + timedelta(minutes=i)
        suspicious = checker.check("U001", ts)
        print(f"Txn {i+1} at {ts.time()} -> suspicious: {suspicious}, "
              f"count in window: {checker.count_in_window('U001')}")

    print()

    # a different, well-behaved user - transactions spaced far apart
    normal_times = [base_time, base_time + timedelta(minutes=10), base_time + timedelta(minutes=25)]
    for i, ts in enumerate(normal_times):
        suspicious = checker.check("U002", ts)
        print(f"U002 txn {i+1} at {ts.time()} -> suspicious: {suspicious}")