class AVLNode:
    def __init__(self, transaction):
        self.transaction = transaction   # the actual Transaction object
        self.amount = transaction.amount # key used for ordering
        self.left = None
        self.right = None
        self.height = 1                  # height of this node's subtree


class AVLTree:
    """
    AVL tree keyed by transaction amount.
    Supports insert, delete, and range queries (find all transactions
    with amount between low and high).
    """

    def __init__(self):
        self.root = None

    # ---------- helpers ----------

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        self._update_height(y)
        self._update_height(x)
        return x  # x becomes the new subtree root

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        self._update_height(x)
        self._update_height(y)
        return y  # y becomes the new subtree root

    # ---------- insert ----------

    def insert(self, transaction):
        self.root = self._insert(self.root, transaction)

    def _insert(self, node, transaction):
        if not node:
            return AVLNode(transaction)

        if transaction.amount < node.amount:
            node.left = self._insert(node.left, transaction)
        else:
            node.right = self._insert(node.right, transaction)

        self._update_height(node)
        balance = self._balance_factor(node)

        # Left Left case
        if balance > 1 and transaction.amount < node.left.amount:
            return self._rotate_right(node)

        # Right Right case
        if balance < -1 and transaction.amount >= node.right.amount:
            return self._rotate_left(node)

        # Left Right case
        if balance > 1 and transaction.amount >= node.left.amount:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left case
        if balance < -1 and transaction.amount < node.right.amount:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node  # already balanced

    # ---------- range query ----------

    def range_query(self, low, high):
        """Return all transactions with amount in [low, high], inclusive."""
        result = []
        self._range_query(self.root, low, high, result)
        return result

    def _range_query(self, node, low, high, result):
        if not node:
            return

        if low < node.amount:
            self._range_query(node.left, low, high, result)

        if low <= node.amount <= high:
            result.append(node.transaction)

        if node.amount < high:
            self._range_query(node.right, low, high, result)

    # ---------- utility ----------

    def height(self):
        return self._height(self.root)

    def inorder(self):
        """Returns transactions sorted by amount (ascending) - free with a BST."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.transaction)
            self._inorder(node.right, result)


if __name__ == "__main__":
    from transaction import Transaction

    amounts = [5000, 15000, 200, 90000, 500, 120000, 3000, 75000]
    txns = [
        Transaction(f"T{i:03d}", f"U{i:03d}", amt, "2025-01-15T10:00:00", "City", f"D{i}", "Merchant")
        for i, amt in enumerate(amounts)
    ]

    tree = AVLTree()
    for t in txns:
        tree.insert(t)

    print("Tree height:", tree.height())  # should be small, e.g. 3-4, not 8

    print("\nAll transactions sorted by amount:")
    for t in tree.inorder():
        print(" ", t.amount)

    print("\nRange query [3000, 90000]:")
    for t in tree.range_query(3000, 90000):
        print(" ", t.amount)