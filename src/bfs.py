def bfs(graph, start):
    """
    Breadth-first traversal from start. Returns the list of users reachable
    from start, in the order they were visited.
    """
    if start not in graph.adj_list:
        return []

    visited = set([start])
    queue = [start]
    order = []

    while queue:
        current = queue.pop(0)
        order.append(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def find_all_connected_groups(graph):
    """
    Finds every connected group of users in the graph using BFS,
    treating the graph as undirected for grouping purposes.
    Useful for spotting clusters of users who transact among themselves.
    """
    visited = set()
    groups = []

    for node in graph.nodes:
        if node not in visited:
            group = bfs(graph, node)
            visited.update(group)
            if len(group) > 1:
                groups.append(group)

    return groups


if __name__ == "__main__":
    from graph import Graph

    g = Graph()
    g.add_edge("U001", "U002")
    g.add_edge("U002", "U003")
    g.add_edge("U005", "U006")
    g.add_node("U010")

    print("BFS from U001:", bfs(g, "U001"))
    print("All connected groups:", find_all_connected_groups(g))