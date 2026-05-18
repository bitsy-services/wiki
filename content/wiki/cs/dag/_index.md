---
title: "Directed Acyclic Graphs"
weight: 5
bookCollapseSection: true
---

A **directed acyclic graph** (DAG) is a [directed graph](https://en.wikipedia.org/wiki/Directed_graph) with no directed cycles: starting from any node and following edges in their direction, you can never return to where you began. That single constraint — acyclicity — is what makes DAGs one of the most useful structures in computing. It guarantees a consistent ordering of nodes and lets recursive definitions over the graph terminate.

DAGs generalise both **sequences** (a chain is a DAG where every node has at most one predecessor and one successor) and **trees** (a tree is a DAG where every node has at most one parent). A DAG relaxes the tree's single-parent rule: a node may be reachable along several distinct paths, as long as none of those paths loops back.

## Formal Definition

A DAG is a pair `G = (V, E)` where `V` is a set of vertices and `E ⊆ V × V` is a set of directed edges, such that there is no sequence of edges `v₀ → v₁ → … → vₖ` with `v₀ = vₖ` and `k ≥ 1`.

Two derived notions recur constantly:

- A **source** is a vertex with no incoming edges.
- A **sink** is a vertex with no outgoing edges.

Every non-empty DAG has at least one source and at least one sink — a fact that follows directly from acyclicity and is the basis of most DAG algorithms.

## Why Acyclicity Matters

The defining property is not cosmetic. It buys three things at once:

- **A topological order exists.** A graph admits a [topological ordering](https://en.wikipedia.org/wiki/Topological_sorting) — a linear arrangement of vertices where every edge points "forward" — *if and only if* it is acyclic. This is the formal sense in which a DAG encodes a set of "X must come before Y" constraints.
- **Recursion over the graph terminates.** Any function defined as "compute something for a node in terms of its neighbours" is well-defined on a DAG. The same recurrence on a cyclic graph either fails to terminate or has no fixed point. The [height/depth recurrence](/wiki/cs/dag/height-and-depth) is the canonical example.
- **Dynamic programming applies.** Because there are no cycles, each subproblem is computed once and memoised, giving linear-time solutions to problems (longest path, reachability) that are NP-hard on general graphs.

A practical corollary: running the height/depth recurrence and watching for non-termination (a node that depends on itself transitively) is a standard way to *detect* an illegal cycle in what was supposed to be a DAG.

## Common Operations

| Operation | What it computes | Typical use |
|---|---|---|
| [Topological sort](https://en.wikipedia.org/wiki/Topological_sorting) | A valid linear order respecting all edges | Build/task scheduling |
| [Longest path](https://en.wikipedia.org/wiki/Longest_path_problem#Acyclic_graphs) | The critical path; linear-time on a DAG | Project scheduling (PERT/CPM) |
| Height / depth | Per-node distance to the nearest sink / source | Layering, scheduling slack |
| Transitive reduction | Smallest edge set with the same reachability | Minimal dependency graphs |
| Transitive closure | All reachable pairs | Reachability queries |

## Where DAGs Show Up

DAGs are the implicit data model behind a surprising amount of infrastructure:

- **Build systems** — Make, Bazel, and Ninja model targets and their prerequisites as a DAG, then topologically order the work.
- **Task and dataflow schedulers** — Airflow, Spark, and TensorFlow graphs are DAGs of operations.
- **Version control** — a Git commit history is a DAG (merges give a commit two parents); `git log --graph` renders it.
- **Content addressing** — Merkle DAGs underpin IPFS and Git's object store; a [blockchain](/wiki/defi/blockchain) is the degenerate linear case.
- **Distributed ledgers** — IOTA's [Tangle](/wiki/defi/iota/tangle) replaced the linear chain with a transaction DAG; modern BFT consensus protocols such as Mysticeti are also DAG-structured.
- **Compilers** — expression DAGs share common subexpressions; SSA form and dependency analysis are DAG problems.
- **Probabilistic models** — a [Bayesian network](https://en.wikipedia.org/wiki/Bayesian_network) is a DAG of conditional dependencies.

## External Links

- [Wikipedia: Directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
- [Wikipedia: Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting)
- [CLRS, *Introduction to Algorithms*](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — DAG-shortest-paths and topological sort (Ch. 22, 24)

## Wiki Pages

{{< section >}}
