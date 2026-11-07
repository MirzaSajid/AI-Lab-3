# Lab 3 - Uninformed Search: BFS, DFS, DLS, IDDFS & UCS

**Student:** Sajid Hussain (BSAIM-046) | **Course:** CAI601400 - Artificial Intelligence | **Lab:** 3 (CLO2)

Uninformed search on the A-G emergency-exit graph (A = start, G = exit): BFS and DFS
traces, depth-limited search (DLS) and iterative deepening (IDDFS) at limits 1-4, and
uniform-cost search (UCS) on a weighted version of the graph. Successor-list order is
the tie-breaking order, depth counts edges, and goal processing is included in every
node count.

The edge weights and the added corridor **C -> G** are a **documented lab assumption**
(the weighted experiment, manual Section 3.7), not part of the original trace graph.

## Setup
Python 3.8+ (tested on 3.12). Standard library only. No virtual environment needed.

```bash
python --version
```

## Run
```bash
python lab3_bfs_dfs.py        # Task 1: BFS and DFS traces (queue/stack after every step)
python lab3_depth_search.py   # Task 2: DLS and IDDFS at limits 1-4 (FOUND/CUTOFF/FAILURE)
python lab3_ucs.py            # Task 3: weighted graph, UCS vs BFS, independent cost check
python lab3_tests.py          # summary + edge cases + failure demo (exit code 0 = all pass)
```
Keep all `lab3_*.py` files in the same folder: `lab3_tests.py` imports the others.

## Files
| File | Purpose |
|---|---|
| `lab3_bfs_dfs.py` | Supplied BFS/DFS (manual 3.2) plus traced versions |
| `lab3_depth_search.py` | DLS and IDDFS with path-local cycle check |
| `lab3_ucs.py` | UCS (priority queue), weighted graph, BFS comparison, exhaustive check |
| `lab3_tests.py` | Summary table, start==goal / unreachable / cycle tests, global-visited failure demo |
| `outputs/*.txt` | Captured outputs of the four scripts |
| `Lab3_Report.docx` | Full report: traces, results, comparison, analysis, reflection |

## Reproducing the outputs
```bash
python lab3_bfs_dfs.py      > outputs/bfs_dfs_output.txt
python lab3_depth_search.py > outputs/depth_search_output.txt
python lab3_ucs.py          > outputs/ucs_output.txt
python lab3_tests.py        > outputs/tests_output.txt
```

## Sources
`bfs()` and `dfs()` in `lab3_bfs_dfs.py` are the supplied reference functions from the
Lab 3 manual (Section 3.2). Everything else is my own implementation. Textbook and
paper sources are listed in the References section of `Lab3_Report.docx`.
No credentials, private data or virtual environments are included.
