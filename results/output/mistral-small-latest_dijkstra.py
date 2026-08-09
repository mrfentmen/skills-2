def dijkstra_shortest_path(graph, source, target):
    """
    Compute the shortest path from source to target in a directed graph with non-negative edge weights.
    Uses Dijkstra's algorithm with a priority queue.
    """
    # requires:
    #   graph is a dict {u: {v: weight}} where u, v are nodes and weight >= 0
    #   source and target are nodes in graph
    # ensures:
    #   returns a tuple (distance, path) where distance is the shortest path length from source to target,
    #   and path is the list of nodes along that path; if no path exists, returns (float('inf'), [])
    # state-space note:
    #   dist: dict mapping node -> best known distance from source (initialized to infinity except source)
    #   prev: dict mapping node -> predecessor in shortest path tree (None for source)
    #   pq: priority queue of (distance, node) pairs, ordered by distance
    #   visited: set of nodes whose shortest distance has been finalized
    #   path: list of nodes from source to target (reconstructed at end)
    # transparency pass:
    #   No clever tricks: standard Dijkstra with priority queue. Uses standard heapq for priority queue.
    #   All variables are justified and necessary for correctness and reconstruction.

    import heapq

    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    prev = {node: None for node in graph}
    pq = [(0, source)]
    visited = set()

    # invariant: for every node v in visited, dist[v] is the shortest distance from source to v,
    #            and for every node v not in visited, dist[v] is the best known upper bound on the shortest distance.
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == target:
            break
        for v, weight in graph[u].items():
            if v in visited:
                continue
            new_dist = d + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    # Reconstruct path if target is reachable
    if dist[target] == float('inf'):
        return (float('inf'), [])
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return (dist[target], path)

# Example usage
if __name__ == "__main__":
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    distance, path = dijkstra_shortest_path(graph, 'A', 'D')
    print(f"Shortest distance: {distance}, Path: {path}")