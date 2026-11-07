"""Lab 3 - Task 3: uniform-cost search (UCS) on a weighted version of the graph.

The original A-G vertices and corridors are kept. The weights below are a
CLEARLY STATED lab assumption (the manual's reference weights were not supplied
in my copy); they are chosen so the manual's Section 3.7 results hold:
BFS prefers A -> C -> G (2 edges, cost 12) and UCS finds
A -> B -> E -> G (3 edges, cost 3). The corridor C -> G is ADDED for this
experiment and is not part of the original manual trace graph.
All weights are nonnegative travel-cost units; UCS assumes nonnegative edges.
Ties in path cost are broken by insertion order (reproducible traces).
Run: python lab3_ucs.py
"""
import heapq
from collections import deque

NODES = ["A", "B", "C", "D", "E", "F", "G"]
# (from, to, weight, note) in successor order
EDGES = [
    ("A", "B", 1, "original"),
    ("A", "C", 5, "original"),
    ("B", "D", 2, "original"),
    ("B", "E", 1, "original"),
    ("C", "F", 3, "original"),
    ("C", "G", 7, "ADDED (Section 3.7)"),
    ("E", "G", 1, "original"),
]


def build_graph(edges, nodes):
    """Weighted adjacency list {node: [(neighbour, weight), ...]}."""
    g = {n: [] for n in nodes}
    for u, v, w, *_ in edges:
        if w < 0:
            raise ValueError(f"negative edge weight {w} on {u}->{v}")
        g[u].append((v, w))
    return g


def ucs(wg, start, goal):
    """Return (path, cost, processing_order, steps) or (None, None, order, steps).

    steps: (step, node, cost, path, frontier) where frontier is the priority
    queue after the step as [(node, cost), ...] in pop order.
    """
    counter = 0
    heap = [(0, counter, start, [start])]
    explored = set()
    order, steps = [], []
    while heap:
        cost, _, node, path = heapq.heappop(heap)
        if node in explored:
            continue                                  # stale duplicate entry
        explored.add(node)
        order.append(node)
        if node != goal:
            for nxt, w in wg[node]:
                if nxt not in explored:
                    counter += 1
                    heapq.heappush(heap, (cost + w, counter, nxt, path + [nxt]))
        frontier = [(n, c) for c, _, n, _ in sorted(heap)]
        steps.append((len(order), node, cost, path, frontier))
        if node == goal:
            return path, cost, order, steps
    return None, None, order, steps


def bfs_path(wg, start, goal):
    """Plain BFS (ignores weights) on the same topology: (path, order)."""
    queue = deque([(start, [start])])
    seen = {start}
    order = []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            return path, order
        for nxt, _ in wg[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None, order


def path_cost(path, edges):
    """Independent check: sum the edge weights along a path from the edge list."""
    weight = {(u, v): w for u, v, w, *_ in edges}
    return sum(weight[(a, b)] for a, b in zip(path, path[1:]))


def all_simple_paths(wg, start, goal):
    out = []

    def walk(node, path):
        if node == goal:
            out.append(path)
            return
        for nxt, _ in wg[node]:
            if nxt not in path:
                walk(nxt, path + [nxt])
    walk(start, [start])
    return out


def arrow(path):
    return " -> ".join(path) if path else "-"


def plus(path, edges):
    weight = {(u, v): w for u, v, w, *_ in edges}
    return " + ".join(str(weight[(a, b)]) for a, b in zip(path, path[1:]))


def main():
    wg = build_graph(EDGES, NODES)

    print("Weighted graph (edges in successor order)")
    print("edge | weight | note")
    for u, v, w, note in EDGES:
        print(f"{u} -> {v}", w, note, sep=" | ")
    print()

    path, cost, order, steps = ucs(wg, "A", "G")
    print("UCS trace (frontier = priority queue by path cost, ties by insertion order)")
    print("step | processed | cost | path | frontier after")
    for step, node, c, p, frontier in steps:
        fr = ", ".join(f"{n}({fc})" for n, fc in frontier)
        print(step, node, c, arrow(p), f"[{fr}]", sep=" | ")
    print("UCS final path      :", arrow(path))
    print(f"UCS processing order: {', '.join(order)} "
          f"({len(order)} nodes processed, goal included)")
    print("Cost reported by UCS:", cost)
    print(f"Independent edge-weight sum: {plus(path, EDGES)} = {path_cost(path, EDGES)}")
    print()

    bpath, border = bfs_path(wg, "A", "G")
    print("BFS on the same weighted topology")
    print(f"BFS processing order: {', '.join(border)} "
          f"({len(border)} nodes processed, goal included)")
    print("BFS path:", arrow(bpath))
    print(f"Hops: {len(bpath) - 1} | independent cost: "
          f"{plus(bpath, EDGES)} = {path_cost(bpath, EDGES)}")
    print()

    print("Comparison of hop count and total cost")
    print("algorithm | path | hops | cost | processing order")
    print("BFS", arrow(bpath), len(bpath) - 1, path_cost(bpath, EDGES),
          ", ".join(border), sep=" | ")
    print("UCS", arrow(path), len(path) - 1, path_cost(path, EDGES),
          ", ".join(order), sep=" | ")
    print()

    print("Exhaustive check: every simple path from A to G")
    print("path | hops | cost")
    allp = all_simple_paths(wg, "A", "G")
    for p in allp:
        print(arrow(p), len(p) - 1, path_cost(p, EDGES), sep=" | ")
    best = min(allp, key=lambda p: path_cost(p, EDGES))
    print(f"Minimum-cost path: {arrow(best)} (cost {path_cost(best, EDGES)}); "
          f"UCS agrees: {best == path}")


if __name__ == "__main__":
    main()
