class Graph:
    """
    Graph of users connected by shared devices or money transfers.
    Supports both adjacency list and adjacency matrix representations,
    plus BFS/DFS for connected clusters and DFS-based cycle detection.
    """

    def __init__(self):
        self.adj_list = {}      # user_id -> set of connected user_ids
        self.nodes = []         # ordered list of all user_ids (needed for matrix indexing)
        self.node_index = {}    # user_id -> index, for matrix lookups

    # ---------- building the graph ----------

    def add_node(self, user_id):
        if user_id not in self.adj_list:
            self.adj_list[user_id] = set()
            self.node_index[user_id] = len(self.nodes)
            self.nodes.append(user_id)

    def add_edge(self, user_a, user_b, directed=False):
        """
        directed=False  -> use for 'shared device' links (relationship is mutual)
        directed=True   -> use for 'money transfer' links (A paid B, direction matters)
        """
        self.add_node(user_a)
        self.add_node(user_b)

        self.adj_list[user_a].add(user_b)
        if not directed:
            self.adj_list[user_b].add(user_a)

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

    # ---------- BFS: find connected clusters ----------

    def bfs_cluster(self, start_user):
        """Returns all users reachable from start_user (their connected cluster)."""
        if start_user not in self.adj_list:
            return []

        visited = set([start_user])
        queue = [start_user]
        cluster = []

        while queue:
            current = queue.pop(0)
            cluster.append(current)

            for neighbor in self.adj_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return cluster

    def find_all_clusters(self):
        """Finds every connected cluster in the graph (e.g., every fraud ring group)."""
        visited = set()
        clusters = []

        for user in self.nodes:
            if user not in visited:
                cluster = self.bfs_cluster(user)
                visited.update(cluster)
                if len(cluster) > 1:          # a lone user isn't a "ring"
                    clusters.append(cluster)

        return clusters

    # ---------- DFS: cycle detection (money loops) ----------

    def has_cycle_directed(self):
        """
        Detects cycles in a DIRECTED graph (for money-transfer loops like A->B->C->A).
        Returns True if any cycle exists.
        """
        visited = set()
        rec_stack = set()   # tracks nodes in the CURRENT dfs path

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True   # back-edge found -> cycle!

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={sum(len(v) for v in self.adj_list.values())})"


if __name__ == "__main__":
    # --- example 1: shared-device fraud ring (undirected) ---
    device_graph = Graph()
    device_graph.add_edge("U001", "U002")   # share a device
    device_graph.add_edge("U002", "U003")
    device_graph.add_edge("U005", "U006")   # separate, unrelated pair
    device_graph.add_node("U010")           # lone user, no shared devices

    print(device_graph)
    print("Cluster containing U001:", device_graph.bfs_cluster("U001"))
    print("All suspicious clusters (size > 1):", device_graph.find_all_clusters())

    print("\nAdjacency matrix:")
    for row in device_graph.get_adjacency_matrix():
        print(" ", row)

    # --- example 2: money transfer loop (directed) ---
    money_graph = Graph()
    money_graph.add_edge("A", "B", directed=True)
    money_graph.add_edge("B", "C", directed=True)
    money_graph.add_edge("C", "A", directed=True)   # closes the loop!

    print("\nMoney graph:", money_graph)
    print("Has cycle (fraud loop)?", money_graph.has_cycle_directed())

    # --- example 3: normal transfers, no loop ---
    normal_graph = Graph()
    normal_graph.add_edge("X", "Y", directed=True)
    normal_graph.add_edge("Y", "Z", directed=True)

    print("\nNormal graph:", normal_graph)
    print("Has cycle?", normal_graph.has_cycle_directed())