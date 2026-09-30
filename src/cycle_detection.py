def has_cycle(graph):
    """
    Detects whether the transaction graph contains a cycle
    (money returning to its origin, e.g. A -> B -> C -> A).
    Uses DFS with a recursion-stack to detect back-edges.
    Returns True if any cycle exists, False otherwise.
    """
    visited = set()
    rec_stack = set()

    def dfs_visit(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                if dfs_visit(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True   # back-edge found -> cycle

        rec_stack.remove(node)
        return False

    for node in graph.nodes:
        if node not in visited:
            if dfs_visit(node):
                return True
    return False


def find_cycle_path(graph):
    """
    Returns one actual cycle as a list of users, e.g. ['A', 'B', 'C', 'A'],
    or None if no cycle exists. Useful for showing WHICH users form the loop,
    not just whether one exists.
    """
    visited = set()
    rec_stack = []   # ordered, so we can reconstruct the path

    def dfs_visit(node):
        visited.add(node)
        rec_stack.append(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                result = dfs_visit(neighbor)
                if result:
                    return result
            elif neighbor in rec_stack:
                cycle_start = rec_stack.index(neighbor)
                return rec_stack[cycle_start:] + [neighbor]

        rec_stack.pop()
        return None

    for node in graph.nodes:
        if node not in visited:
            result = dfs_visit(node)
            if result:
                return result
    return None


if __name__ == "__main__":
    from graph import Graph

    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")

    print("Has cycle?", has_cycle(g))
    print("Cycle path:", find_cycle_path(g))

    g2 = Graph()
    g2.add_edge("X", "Y")
    g2.add_edge("Y", "Z")
    print("\nHas cycle?", has_cycle(g2))
    print("Cycle path:", find_cycle_path(g2))