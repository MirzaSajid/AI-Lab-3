"""Lab 3 - Task 2: depth-limited search (DLS) and iterative deepening (IDDFS).

Same original A-G graph; the root has depth 0 and depth counts edges.
Status values:
  FOUND   - the goal was reached within the depth limit.
  CUTOFF  - the goal was not found, but at least one branch was stopped by the
            limit while it still had an unexplored (non-cyclic) continuation,
            so a deeper search might still succeed.
  FAILURE - the explored space is exhausted: no deeper continuation exists.
Cycle check: path-local (a successor already on the CURRENT path is skipped).
No global visited set is carried across branches or across depth limits.
Run: python lab3_depth_search.py
"""

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"],
         "D": [], "E": ["G"], "F": [], "G": []}


def dls(g, start, goal, limit):
    """Return (status, path, visit_order). Visit order lists processed nodes."""
    visited = []

    def recurse(node, path, remaining):
        visited.append(node)
        if node == goal:
            return "FOUND", path
        successors = [n for n in g[node] if n not in path]   # path-local check
        if remaining == 0:
            return ("CUTOFF", None) if successors else ("FAILURE", None)
        cutoff = False
        for n in successors:
            status, result = recurse(n, path + [n], remaining - 1)
            if status == "FOUND":
                return status, result
            if status == "CUTOFF":
                cutoff = True
        return ("CUTOFF", None) if cutoff else ("FAILURE", None)

    status, path = recurse(start, [start], limit)
    return status, path, visited


def iddfs(g, start, goal, max_depth):
    """Run DLS with limits 0..max_depth, each time from scratch.

    Returns (status, path, per_limit) where per_limit is a list of
    (limit, status, nodes_processed). Stops early on FOUND, or on FAILURE
    (nothing was cut off, so a larger limit cannot help).
    """
    per_limit = []
    for limit in range(max_depth + 1):
        status, path, visited = dls(g, start, goal, limit)
        per_limit.append((limit, status, len(visited)))
        if status == "FOUND":
            return "FOUND", path, per_limit
        if status == "FAILURE":
            return "FAILURE", None, per_limit
    return "CUTOFF", None, per_limit


def arrow(path):
    return " -> ".join(path) if path else "-"


def main():
    print("DLS on the original graph, start A, goal G (root depth 0)")
    print("limit | status | path | nodes processed (visit order)")
    for limit in (1, 2, 3, 4):
        status, path, visited = dls(graph, "A", "G", limit)
        print(limit, status, arrow(path), ", ".join(visited), sep=" | ")
    print()

    print("IDDFS on the original graph, start A, goal G")
    print("max depth | status | path | limits attempted | total nodes processed")
    for max_depth in (1, 2, 3, 4):
        status, path, per_limit = iddfs(graph, "A", "G", max_depth)
        limits = ", ".join(str(l) for l, _, _ in per_limit)
        total = sum(n for _, _, n in per_limit)
        print(max_depth, status, arrow(path), limits, total, sep=" | ")
    print()

    print("IDDFS per-iteration detail (max depth 4; stops when G is found)")
    print("limit | status | nodes processed")
    _, _, per_limit = iddfs(graph, "A", "G", 4)
    for limit, status, n in per_limit:
        print(limit, status, n, sep=" | ")
    single = len(dls(graph, "A", "G", 3)[2])
    total = sum(n for _, _, n in per_limit)
    print()
    print(f"Repeated work: one DLS at limit 3 processes {single} nodes; "
          f"IDDFS processes {total} in total across limits 0-3.")


if __name__ == "__main__":
    main()
