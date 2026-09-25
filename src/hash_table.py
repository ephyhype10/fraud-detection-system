class HashTable:
    """
    Custom hash table using separate chaining for collision resolution.
    Used to map user_id -> list of that user's transactions.
    """

    def __init__(self, size=101):
        self.size = size
        self.buckets = [[] for _ in range(size)]  # each bucket is a list (chain)
        self.collision_count = 0
        self.item_count = 0

    def _hash(self, key):
        """Polynomial rolling hash - spreads similar keys (like 'U1', 'U10', 'U100')
        across the table much better than a simple character sum."""
        hash_value = 0
        prime = 31
        for ch in str(key):
            hash_value = (hash_value * prime + ord(ch)) % self.size
        return hash_value

    def insert(self, key, value):
        """
        Insert (key, value). If key already exists, append value to its list
        (since one user has MANY transactions, not just one).
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for pair in bucket:
            if pair[0] == key:
                pair[1].append(value)   # key exists, add to its transaction list
                return

        # key not found in this bucket -> new entry
        if len(bucket) > 0:
            self.collision_count += 1   # bucket wasn't empty, so this is a collision

        bucket.append([key, [value]])
        self.item_count += 1

    def get(self, key):
        """Return the list of values stored under this key, or empty list if not found."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return []

    def contains(self, key):
        return len(self.get(key)) > 0

    def delete(self, key):
        """Remove a key and all its values entirely."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self.item_count -= 1
                return True
        return False

    def load_factor(self):
        """How full the table is — useful for your performance report."""
        return self.item_count / self.size

    def __repr__(self):
        return f"HashTable(size={self.size}, items={self.item_count}, collisions={self.collision_count})"


if __name__ == "__main__":
    ht = HashTable(size=10)

    ht.insert("U001", "T001")
    ht.insert("U001", "T002")   # same user, second transaction
    ht.insert("U002", "T003")
    ht.insert("U003", "T004")

    print(ht)
    print("U001 transactions:", ht.get("U001"))
    print("U002 transactions:", ht.get("U002"))
    print("U999 transactions (not found):", ht.get("U999"))
    print("Contains U003?", ht.contains("U003"))
    print("Load factor:", ht.load_factor())