class Graph:
    """
    Graph of users connected by money transfers.
    Users are nodes; transactions are directed edges (sender -> receiver).
    Supports both adjacency list and adjacency matrix representations.
    """

    def __init__(self):
        self.adj_list = {}      # user_id -> set of users they sent money to
        self.nodes = []         # ordered list of all user_ids (for matrix indexing)
        self.node_index = {}    # user_id -> index, for matrix lookups

    def add_node(self, user_id):
        if user_id not in self.adj_list:
            self.adj_list[user_id] = set()
            self.node_index[user_id] = len(self.nodes)
            self.nodes.append(user_id)

    def add_edge(self, sender, receiver, weight=None):
        """
        Adds a directed edge sender -> receiver (money sent from sender to receiver).
        weight is optional, used later by shortest_path.py (e.g. transaction amount).
        """
        self.add_node(sender)
        self.add_node(receiver)
        self.adj_list[sender].add(receiver)

        if weight is not None:
            if not hasattr(self, "weights"):
                self.weights = {}
            self.weights[(sender, receiver)] = weight

    def get_weight(self, sender, receiver):
        if hasattr(self, "weights"):
            return self.weights.get((sender, receiver))
        return None

    def get_adjacency_matrix(self):
        """Builds and returns the adjacency matrix (2D list) on demand."""
        n = len(self.nodes)
        matrix = [[0] * n for _ in range(n)]

        for user, neighbors in self.adj_list.items():
            i = self.node_index[user]
            for neighbor in neighbors:
                j = self.node_index[neighbor]
                matrix[i][j] = 1

        return matrix

    def neighbors(self, user_id):
        return self.adj_list.get(user_id, set())

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={sum(len(v) for v in self.adj_list.values())})"


if __name__ == "__main__":
    g = Graph()
    g.add_edge("U001", "U002", weight=5000)
    g.add_edge("U002", "U003", weight=4800)
    g.add_edge("U003", "U001", weight=7800)   # closes a loop

    print(g)
    print("Neighbors of U001:", g.neighbors("U001"))
    print("Weight U001->U002:", g.get_weight("U001", "U002"))

    print("\nAdjacency matrix:")
    for row in g.get_adjacency_matrix():
        print(" ", row)