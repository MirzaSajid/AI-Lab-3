"""Lab 3 - Task 1: BFS and DFS on the original A-G emergency-exit graph.

A is the initial location and G is the exit. Successor-list order is the
tie-breaking order. Depth counts edges (A has depth 0).

bfs() and dfs() are the supplied reference functions from the Lab 3 manual
(Section 3.2), kept unchanged apart from layout. bfs_trace() and dfs_trace()
follow exactly the same logic but also record every node that is removed from
the queue/stack and processed, plus the frontier after each step, so that a
manual trace can be checked against code.

Trace convention (manual Section 3.5): list each node removed from the
queue/stack and processed, including the goal; skip already-processed
duplicates; stop when the goal is processed.
Run: python lab3_bfs_dfs.py
"""
from collections import deque

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"],
         "D": [], "E": ["G"], "F": [], "G": []}


# ---- supplied reference code (manual Section 3.2) -------------------------
def bfs(start, goal):
    q = deque([(start, [start])])
    seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal:
            return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n)
                q.append((n, path + [n]))


def dfs(start, goal):
    stack = [(start, [start])]
    seen = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node in seen:
            continue
        seen.add(node)
        for n in reversed(graph[node]):
            stack.append((n, path + [n]))


# ---- traced versions (same logic, graph passed in) ------------------------
def bfs_trace(g, start, goal):
    """Return (path, visit_order, steps). Frontier = queue, front first."""
    queue = deque([(start, [start])])
    seen = {start}
    order, steps = [], []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            steps.append((len(order), node, path, [n for n, _ in queue]))
            return path, order, steps
        for n in g[node]:
            if n not in seen:
                seen.add(n)
                queue.append((n, path + [n]))
        steps.append((len(order), node, path, [n for n, _ in queue]))
    return None, order, steps


def dfs_trace(g, start, goal):
    """Return (path, visit_order, steps). Frontier = stack, top first."""
    stack = [(start, [start])]
    seen = set()
    order, steps = [], []
    while stack:
        node, path = stack.pop()
        if node in seen and node != goal:
            continue                      # already processed duplicate
        order.append(node)
        if node == goal:
            steps.append((len(order), node, path, [n for n, _ in reversed(stack)]))
            return path, order, steps
        seen.add(node)
        for n in reversed(g[node]):
            stack.append((n, path + [n]))
        steps.append((len(order), node, path, [n for n, _ in reversed(stack)]))
    return None, order, steps


def arrow(path):
    return " -> ".join(path) if path else "-"


def show(title, frontier_note, path, order, steps, supplied):
    print(f"{title} ({frontier_note})")
    print("step | processed | path | frontier after")
    for step, node, p, frontier in steps:
        print(step, node, arrow(p), "[" + ", ".join(frontier) + "]", sep=" | ")
    print("Final path :", arrow(path))
    print(f"Visit order: {', '.join(order)} "
          f"({len(order)} nodes processed, goal included)")
    print("Matches supplied code path:", path == supplied)
    print()


def main():
    print("Supplied code (manual Section 3.2), path only")
    print("bfs ->", bfs("A", "G"))
    print("dfs ->", dfs("A", "G"))
    print()
    p, o, s = bfs_trace(graph, "A", "G")
    show("BFS trace", "queue, front first", p, o, s, bfs("A", "G"))
    p, o, s = dfs_trace(graph, "A", "G")
    show("DFS trace", "stack, top first", p, o, s, dfs("A", "G"))


if __name__ == "__main__":
    main()
