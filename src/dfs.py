def dfs(graph, start, visited=None):
    """
    Depth-first traversal from start. Returns the list of users visited,
    in DFS order.
    """
    if visited is None:
        visited = set()

    if start not in graph.adj_list or start in visited:
        return []

    visited.add(start)
    order = [start]

    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            order.extend(dfs(graph, neighbor, visited))

    return order


if __name__ == "__main__":
    from graph import Graph

    g = Graph()
    g.add_edge("U001", "U002")
    g.add_edge("U002", "U003")
    g.add_edge("U001", "U004")

    print("DFS from U001:", dfs(g, "U001"))