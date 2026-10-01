import heapq


def shortest_path(graph, start, end):
    """
    Finds the shortest (lowest total weight) path from start to end using
    Dijkstra's algorithm. Weight = transaction amount on each edge.

    Returns (path, total_weight) where path is a list of users from start
    to end, or (None, float('inf')) if no path exists.
    """
    if start not in graph.adj_list or end not in graph.adj_list:
        return None, float('inf')

    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous = {node: None for node in graph.nodes}

    visited = set()
    priority_queue = [(0, start)]   # (distance, node)

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue

            weight = graph.get_weight(current_node, neighbor)
            if weight is None:
                weight = 1   # fallback: treat as unweighted if no weight stored

            new_dist = current_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_dist, neighbor))

    if distances[end] == float('inf'):
        return None, float('inf')

    # reconstruct path by walking backwards through `previous`
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return path, distances[end]


if __name__ == "__main__":
    from graph import Graph

    g = Graph()
    g.add_edge("U001", "U002", weight=5000)
    g.add_edge("U002", "U003", weight=4800)
    g.add_edge("U003", "U004", weight=5200)
    g.add_edge("U001", "U004", weight=20000)   # direct but expensive route
    g.add_edge("U004", "U005", weight=3000)

    path, total = shortest_path(g, "U001", "U005")
    print(f"Shortest path U001 -> U005: {path}")
    print(f"Total weight (amount): {total}")

    path2, total2 = shortest_path(g, "U001", "U004")
    print(f"\nShortest path U001 -> U004: {path2}")
    print(f"Total weight (amount): {total2}")

    path3, total3 = shortest_path(g, "U001", "U999")
    print(f"\nShortest path U001 -> U999 (no connection): {path3}, weight: {total3}")