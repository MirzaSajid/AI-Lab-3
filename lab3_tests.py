"""Lab 3 - comparison summary, edge-case tests (Section 3.8) and a failure demo.

Part 1  summary of all five algorithms on the A-G graph (goal processing is
        INCLUDED in every node count).
Part 2  start == goal, unreachable goal, a graph containing a cycle, a depth
        limit that is not proof of unreachability, and a negative-weight guard.
Part 3  failure demo: a GLOBAL visited set inside depth-limited search wrongly
        suppresses a valid shallower route (the flaw warned about in Section 3.6).
        The flawed function exists only for this demonstration.
Exit code 0 if every check passes, 1 otherwise.
Run: python lab3_tests.py   (needs the other lab3_*.py files in the same folder)
"""
import sys

import lab3_bfs_dfs as bd
from lab3_depth_search import dls, iddfs
from lab3_ucs import EDGES, NODES, build_graph, path_cost, ucs

results = []


def check(name, condition):
    results.append(bool(condition))
    print(f"{'PASS' if condition else 'FAIL'} | {name}")


def arrow(path):
    return " -> ".join(path) if path else "-"


def unweighted(wg):
    return {n: [v for v, _ in nbrs] for n, nbrs in wg.items()}


def dls_global_visited(g, start, goal, limit):
    """FLAWED on purpose: one visited set shared by all branches of one DLS."""
    visited = set()

    def recurse(node, path, remaining):
        if node == goal:
            return path
        if node in visited:
            return None
        visited.add(node)
        if remaining == 0:
            return None
        for n in g[node]:
            found = recurse(n, path + [n], remaining - 1)
            if found:
                return found
        return None
    return recurse(start, [start], limit)


def main():
    # ---------------------------------------------------------------- Part 1
    print("== Part 1: summary on the A-G graphs (goal processing included) ==")
    wg = build_graph(EDGES, NODES)
    print("algorithm | graph | path | nodes processed")
    p, o, _ = bd.bfs_trace(bd.graph, "A", "G")
    print("BFS", "original", arrow(p), len(o), sep=" | ")
    p, o, _ = bd.dfs_trace(bd.graph, "A", "G")
    print("DFS", "original", arrow(p), len(o), sep=" | ")
    s, p, v = dls(bd.graph, "A", "G", 3)
    print("DLS limit 3", "original", arrow(p), len(v), sep=" | ")
    s, p, per = iddfs(bd.graph, "A", "G", 4)
    print("IDDFS max depth 4", "original", arrow(p),
          f"{sum(n for _, _, n in per)} (final iteration {per[-1][2]})", sep=" | ")
    p, c, o, _ = ucs(wg, "A", "G")
    print("UCS", "weighted (C -> G added)", arrow(p), len(o), sep=" | ")
    print()

    # ---------------------------------------------------------------- Part 2
    print("== Part 2: edge cases ==")
    # 1. start == goal
    g = bd.graph
    check("start == goal: BFS returns [A]", bd.bfs_trace(g, "A", "A")[0] == ["A"])
    check("start == goal: DFS returns [A]", bd.dfs_trace(g, "A", "A")[0] == ["A"])
    check("start == goal: DLS limit 0 FOUND [A]", dls(g, "A", "A", 0)[:2] == ("FOUND", ["A"]))
    check("start == goal: IDDFS FOUND [A] after limit 0 only",
          iddfs(g, "A", "A", 4)[0:2] == ("FOUND", ["A"]) and len(iddfs(g, "A", "A", 4)[2]) == 1)
    r = ucs(wg, "A", "A")
    check("start == goal: UCS returns [A] with cost 0", r[0] == ["A"] and r[1] == 0)

    # 2. unreachable goal (H exists but no edge leads to it)
    gx = dict(bd.graph, H=[])
    wgx = dict(wg, H=[])
    check("unreachable H: BFS returns None", bd.bfs_trace(gx, "A", "H")[0] is None)
    check("unreachable H: DFS returns None", bd.dfs_trace(gx, "A", "H")[0] is None)
    check("unreachable H: DLS limit 2 is CUTOFF (not proof of unreachability)",
          dls(gx, "A", "H", 2)[0] == "CUTOFF")
    check("unreachable H: DLS limit 4 is FAILURE (space exhausted)",
          dls(gx, "A", "H", 4)[0] == "FAILURE")
    st, _, per = iddfs(gx, "A", "H", 4)
    print("info | IDDFS for unreachable H attempted limits", [l for l, _, _ in per], "->", st)
    check("unreachable H: IDDFS ends with FAILURE before max depth",
          st == "FAILURE" and len(per) < 5)
    check("unreachable H: UCS returns None", ucs(wgx, "A", "H")[0] is None)

    # 3. graph containing a cycle (weights: A-C-D-E is cheapest, A-B-D-E is not)
    cyc_edges = [("A", "B", 1), ("A", "C", 1), ("B", "A", 1), ("B", "D", 5),
                 ("C", "D", 1), ("D", "A", 1), ("D", "E", 1)]
    cyc_w = build_graph(cyc_edges, list("ABCDE"))
    cyc = unweighted(cyc_w)
    check("cycle: BFS terminates and finds E", bd.bfs_trace(cyc, "A", "E")[0] == ["A", "B", "D", "E"])
    check("cycle: DFS terminates and finds E", bd.dfs_trace(cyc, "A", "E")[0] == ["A", "B", "D", "E"])
    check("cycle: DLS limit 3 FOUND with path-local check",
          dls(cyc, "A", "E", 3)[:2] == ("FOUND", ["A", "B", "D", "E"]))
    check("cycle: IDDFS FOUND at limit 3", iddfs(cyc, "A", "E", 4)[0] == "FOUND")
    cp, cc, _, _ = ucs(cyc_w, "A", "E")
    bp = bd.bfs_trace(cyc, "A", "E")[0]
    print(f"info | cycle graph: BFS path {arrow(bp)} cost {path_cost(bp, cyc_edges)}; "
          f"UCS path {arrow(cp)} cost {cc}")
    check("cycle: UCS finds cheaper path (cost 3) than BFS (cost 7)",
          cc == 3 and path_cost(bp, cyc_edges) == 7 and path_cost(cp, cyc_edges) == cc)

    # 4. negative weights are rejected
    try:
        build_graph([("A", "B", -1)], ["A", "B"])
        rejected = False
    except ValueError:
        rejected = True
    check("negative edge weight is rejected (UCS assumes nonnegative costs)", rejected)

    # ---------------------------------------------------------------- Part 3
    print()
    print("== Part 3: failure demo - global visited set inside DLS ==")
    trap = {"A": ["B", "C"], "B": ["D"], "D": ["C"], "C": ["X"], "X": ["G"], "G": []}
    print("graph:", trap)
    print("shortest route A -> C -> X -> G has depth 3; limit = 3")
    flawed = dls_global_visited(trap, "A", "G", 3)
    status, correct, visited = dls(trap, "A", "G", 3)
    print("flawed (global visited) result :", arrow(flawed) if flawed else "not found")
    print("correct (path-local) result    :", status, arrow(correct))
    print("correct visit order            :", ", ".join(visited))
    check("flawed global-visited DLS misses the valid depth-3 route", flawed is None)
    check("path-local DLS finds A -> C -> X -> G", correct == ["A", "C", "X", "G"])

    passed = sum(results)
    print()
    print(f"{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
