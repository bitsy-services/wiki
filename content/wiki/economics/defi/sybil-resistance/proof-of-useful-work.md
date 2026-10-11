---
title: "Proof of Useful Work"
weight: 90
---

A proof of useful work is a [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work) whose computation produces something of value besides the proof. Ordinary proof of work has a miner try billions of hashes whose only product is a number below a target. The proposal is to have the miner solve a problem somebody wants solved, in a form that still shows the computation was done.

The appeal is the electricity. The obstacle is that a mining puzzle needs a set of properties that useful problems rarely have, and each attempt to supply them has taken away some of the usefulness. No widely used chain runs on useful work. The idea is as old as the term proof of work: the 1999 paper that formalized proof of work also defined a "bread pudding protocol", one in which the effort "may be reused by the verifier to achieve a separate, useful, and verifiably correct computation."

## What a mining puzzle needs

A puzzle that decides who adds the next block has to satisfy several requirements together.

- **Cheap to check.** Every node verifies every block. The answer must be far quicker to verify than to find.
- **Adjustable difficulty.** The network tunes the puzzle so that blocks arrive at a steady rate as hardware comes and goes, so difficulty has to be adjustable in fine steps.
- **Bound to the block.** A solution must be valid for one block only. Otherwise it could be reused for another block or prepared in advance.
- **No shortcuts across instances.** Solving many puzzles must cost as much as solving each alone, and nobody may hold a head start on particular instances.
- **Random completion time.** The time to solve must vary from attempt to attempt, so that the fastest machine does not win every block.

Hashing has all five almost by construction. A real problem tends to come with structure, and structure is what an attacker exploits. The authors of one design put the dilemma this way: "If the work solved is truly useful then the attackers may direct the system towards solving problem instances that are easy for them", and "minimizing the attacker's ability to manipulate the system may render the system's computations useless in practice".

## Primecoin

Primecoin, launched by Sunny King in 2013, is an early attempt to run a chain on something other than hashing. Its miners search for chains of prime numbers of three kinds. In a Cunningham chain of the first kind each prime is one more than double the one before, in a chain of the second kind one less than double, and a bi-twin chain is a sequence of twin-prime pairs with each pair roughly double the last.

The design shows how the requirements shape the choice of problem.

- Chains were chosen over record-size primes because "the work needs to be efficiently verifiable by all nodes of the network", which rules out primes that are large enough to be records.
- The work is tied to the block by requiring that the chain's starting point "be divisible by the block header hash".
- Difficulty is the length of the chain, with a fractional part taken from how close the next number comes to being prime. Chain length alone moves in whole steps, which would be too coarse.

The paper admits a cost to that last device: because difficulty is not strictly linear, "an attacker may only need somewhat less than 50% of total network mining power". Its claim for the output is modest, "additional potential scientific value". A later paper is blunter, calling the prime chains "mathematical objects of dubious usefulness".

## The formal attempts

**Ball, Rosen, Sabin and Vasudevan** (2017) built puzzles from problems studied in the theory of fine-grained complexity, "including Orthogonal Vectors, 3SUM, All-Pairs Shortest Path", and proved, under assumptions about the hardness of those problems, that their puzzles "cannot be amortized across multiple instances". The first page of that paper now carries a note from the authors that its definition of usefulness "is already satisfied by a generic naive construction", and points to a revised version. The puzzles also take a predictable time to solve, which fails the last requirement above.

**Ofelimos** (2021), by Fitzi, Kiayias, Panagiotakos and Russell, starts from the observation that the concept "still lacks a convincingly secure realization". Its miners run steps of a randomized search on optimization problems that clients post to the chain, with the search arranged so that miners cannot pick out easy steps. The paper measures how much of the work is useful, and the answer shows the price of security. By its own analysis no more than half of the computation steps go to the useful search, and on its headline benchmark the search took about twice as many steps as an ordinary solver. It is a protocol with a security proof and experiments, and no deployed network was reported.

## The economic objection

A separate argument says the goal is confused even when the engineering works. Paul Sztorc made it in a 2015 essay with a section headed "Making The 'Work' Useful (Won't Work)", in two parts.

If the miner captures the side benefit, nothing is saved. His example is a mining machine that also heats a room. A miner who earns the block reward plus five dollars' worth of heat will spend up to that larger sum on mining, and difficulty rises to match. The benefit becomes "just another increase in hardware-efficiency, resulting in a higher difficulty".

If the public captures the benefit, as with newly found primes, the accounting works out: miners gain nothing extra, so they spend nothing extra, and society receives the by-product for free. But then "there is no incentive for Miners to switch to such a system". In his words, "The very thing which makes this scheme less-wasteful also makes it less-practical."

## Nearby ideas

Some systems reward useful computation without using it to secure the chain. Gridcoin describes itself as rewarding volunteer scientific computing "on top of" proof of stake.

[Proof of storage](/wiki/economics/defi/sybil-resistance/proof-of-storage) is the nearest thing to useful work in production. On Filecoin the resource that weights consensus is disk space holding customers' data, and its specification calls this the network's "useful Proof-of-Work". The usefulness there has its own qualification, since empty storage counts too.

## Sources

- Jakobsson & Juels, [Proofs of Work and Bread Pudding Protocols](https://doi.org/10.1007/978-0-387-35568-9_18) (1999)
- King, [Primecoin: Cryptocurrency with Prime Number Proof-of-Work](https://web.archive.org/web/2023/https://primecoin.io/bin/primecoin-paper.pdf) (7 July 2013)
- Ball, Rosen, Sabin & Vasudevan, [Proofs of Useful Work](https://eprint.iacr.org/2017/203) (2017; revision of February 2021)
- Fitzi, Kiayias, Panagiotakos & Russell, [Ofelimos: Combinatorial Optimization via Proof-of-Useful-Work](https://eprint.iacr.org/2021/1379) (2021)
- Sztorc, [Nothing is Cheaper than Proof of Work](https://www.truthcoin.info/blog/pow-cheapest/) (4 August 2015)
- Gridcoin, [project site](https://gridcoin.us/), read 10 October 2026
