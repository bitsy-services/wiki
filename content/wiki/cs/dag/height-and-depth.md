---
title: "Height and Depth in a DAG"
weight: 1
---

A recurring question when working with dependency [DAGs](/wiki/cs/dag/) is what to call this quantity:

```text
level(v) = 0                                  if v has no dependencies
         = 1 + max(level(d) for d in deps(v)) otherwise
```

A node with nothing below it is `0`; every other node is one more than the deepest thing it depends on. Is that **height** or **depth**? The short answer: by the standard tree analogy it is **height**, but the word is convention-dependent and the only safe practice is to define the recurrence explicitly rather than rely on the label. This page explains why the ambiguity exists and how to reason about it precisely.

## Trees: the Baseline

The terms come from rooted trees, where they are unambiguous and *opposite* in direction:

- **Depth** of a node is the number of edges from the **root** down to it. The root has depth `0`. Depth grows as you move *away from the root*.
- **Height** of a node is the number of edges on the longest path from it down to a **leaf**. Leaves have height `0`. Height grows as you move *toward the root*.

The two are measured from opposite ends. Depth counts down from the root; height counts up from the leaves.

## Mapping the Recurrence onto the Tree Picture

The recurrence above bottoms out at nodes with *no dependencies* and assigns them `0`. Those nodes are the **sinks** of the "depends-on" relation — the analogue of a tree's leaves. The value then increases as you move toward the nodes that depend on everything else.

That is exactly the tree definition of **height**: leaves are `0`, and a node is `1 + max` over its children. So the quantity you asked about is **height** — specifically, *the length of the longest path from the node to a dependency-free sink.*

The dual quantity — `0` at the **sources** (nodes nothing depends on) and `1 + max` over *predecessors* — is **depth**: the length of the longest path from a source down to the node.

| | Recurrence bottoms out at | Counts toward | Equals |
|---|---|---|---|
| **Height(v)** | sinks (no dependencies) | sources | longest path *from* `v` to a sink |
| **Depth(v)** | sources (nothing depends on it) | sinks | longest path *to* `v` from a source |

Your recurrence is the **Height(v)** row.

## Direction Is the Real Source of Confusion

A DAG has no single root, so "up" and "down" are not intrinsic — they depend entirely on **which way you orient the edges and which end you call the bottom.** This is why people disagree:

- Draw dependencies *below* their dependents (the common "the foundation is at the bottom" mental model) and the leaf-level dependency-free nodes sit at the bottom. Counting up from them is naturally "height."
- Draw dependents *below* (a "drill-down into what this needs" mental model) and the same nodes sit at the bottom of a different picture, and many practitioners call your recurrence the **dependency depth** — "how deep does this thing's dependency tree go."

Both camps are internally consistent. Graph-theory-by-tree-analogy says **height** (leaves = 0). Everyday "how deep is the dependency tree" usage says **depth**. Neither is wrong; they have just fixed different ends as the origin.

**Recommendation:** in code and docs, do not lean on the bare word. Either spell it out — `longestPathToLeaf`, `dependencyDepth`, `topoLevel` — or state the recurrence next to the name. If you want a single defensible convention, use **height** with "sinks are 0," because it matches the rooted-tree definition every data-structures text already agrees on.

## The Pair Does Not Sum to a Constant

It is tempting to assume `depth(v) + height(v)` is the same for every node (the total DAG "length"). It is not. For a node `v`:

```text
depth(v) + height(v) = length of the longest path that passes through v
```

That equals the DAG's overall critical-path length **only if `v` lies on a longest path**. Off the critical path the sum is strictly smaller — the difference is the scheduling *slack* of that node. This is precisely the ASAP/ALAP reasoning used in project scheduling by the program evaluation and review technique (PERT) and the critical path method (CPM).

## Pseudocode

A memoised depth-first traversal computes height in `O(V + E)`:

```python
def height(v, deps, memo):
    if v in memo:
        return memo[v]
    if not deps(v):                 # no dependencies -> a sink
        memo[v] = 0
    else:
        memo[v] = 1 + max(height(d, deps, memo) for d in deps(v))
    return memo[v]
```

This terminates only because the graph is acyclic. If `deps` ever forms a cycle, the recursion revisits a node already on the call stack — the standard way to *detect* that the "DAG" is not actually acyclic. A robust implementation tracks an in-progress set and raises on a back edge:

```python
def height(v, deps, memo, on_stack):
    if v in memo:
        return memo[v]
    if v in on_stack:
        raise ValueError(f"cycle through {v!r}: not a DAG")
    on_stack.add(v)
    memo[v] = 0 if not deps(v) else 1 + max(
        height(d, deps, memo, on_stack) for d in deps(v)
    )
    on_stack.discard(v)
    return memo[v]
```

## Related Terms You Will Encounter

The same quantity travels under several names depending on the field:

- **Level** or **rank** — graph drawing (Sugiyama layered layout) calls longest-path layering the node's *level*.
- **Topological generation** — the set of all nodes sharing a given height; generation 0 is exactly the sinks.
- **Longest-path layering** — the layout algorithm that assigns each node its height (or depth, depending on orientation).
- **ASAP / ALAP** — "as soon/late as possible" schedules are depth and `criticalPath − height` respectively.

They are all the same recurrence; only the orientation and the application's vocabulary differ.

## External Links

- [Wikipedia: Tree (data structure) — terminology](https://en.wikipedia.org/wiki/Tree_(data_structure)#Terminology) — the root/leaf, depth/height definitions
- [Wikipedia: Longest path problem (acyclic graphs)](https://en.wikipedia.org/wiki/Longest_path_problem#Acyclic_graphs)
- [Wikipedia: Critical path method](https://en.wikipedia.org/wiki/Critical_path_method) — where height/depth slack is used in practice
- [Layered graph drawing](https://en.wikipedia.org/wiki/Layered_graph_drawing) — longest-path layering
