---
title: "Actor Model"
weight: 30
---

The **actor model** is a model of concurrent computation in which every entity is an independently addressable *actor* with its own identity, private state, and behaviour. Computation proceeds by passing asynchronous messages between actors. There is no shared memory, no implicit container holding the actors, and no global lock -- each actor is its own consistency boundary.

It is the maximal expression of the first-class-object stance from the [broader entity-addressing tension](/wiki/cs/entity-addressing): rather than putting many entities inside one process and addressing them by a local id, the actor model gives every entity its own globally unique identity and lets the runtime route messages directly.

## Origin

The model was introduced by Carl Hewitt, Peter Bishop, and Richard Steiger in [*A Universal Modular Actor Formalism for Artificial Intelligence*](https://dspace.mit.edu/handle/1721.1/6952) (1973). Hewitt's motivation was partly philosophical -- he wanted a computational model where everything, including primitive values, was an active entity capable of receiving messages -- and partly practical: by the early 1970s it was already clear that multi-core and multi-machine systems would dominate, and the prevailing shared-memory model did not extend cleanly to either.

Gul Agha's [*Actors: A Model of Concurrent Computation in Distributed Systems*](https://mitpress.mit.edu/9780262511414/actors/) (1986) gave the model its modern formal treatment and influenced most subsequent implementations.

## The core rules

An actor, on receiving a message, may do only three things -- the so-called *axioms* of the model:

1. **Send** a finite number of messages to other actors whose addresses it knows.
2. **Create** a finite number of new actors.
3. **Designate** the behaviour to use for the next message it receives.

That is the entire model. There is no built-in shared state, no synchronisation primitives, no locks, no transactions. Concurrency emerges because actors process messages independently; ordering is constrained only by the per-actor mailbox (each actor handles its own messages one at a time) and causality (an actor can only send to addresses it has been told about).

Three properties follow from those three rules:

- **Identity is a first-class value.** An actor address can be sent in a message, stored, compared, and used to send -- but it cannot be forged or guessed, which is the basis of the model's [object-capability](https://en.wikipedia.org/wiki/Object-capability_model) security properties.
- **No address, no access.** Because addresses are the only way to send messages, an actor that has never been given another's address cannot interfere with it. Authority is conveyed by reference.
- **State is private.** Two actors cannot race on shared state because they do not share state. They race only on the *ordering* of message delivery, which is the easier problem.

## Implementations

### Erlang

Joe Armstrong's [Erlang](https://www.erlang.org/), built at Ericsson starting in 1986, is the most widely deployed actor implementation: Ericsson's telephony switches, RabbitMQ, WhatsApp, and -- through Elixir -- Discord all run on its BEAM virtual machine. Every Erlang process is an actor: it has a PID (process identifier), a private heap, and a mailbox. Processes are cheap (tens of thousands per node is unremarkable), preemptively scheduled by the BEAM VM, and isolated -- one crashing does not corrupt another.

Erlang added two ideas the actor model itself does not require:

- **"Let it crash."** Rather than defensively coding every error path, an actor crashes on unexpected input. A supervising actor restarts it. Fault tolerance becomes a structural property of the [supervision tree](https://www.erlang.org/doc/system/sup_princ.html) rather than something each actor implements.
- **Hot code reloading.** Because actors communicate only by message, swapping an actor's behaviour mid-flight is straightforward -- the new code takes effect on the next message.

[OTP](https://www.erlang.org/doc/design_principles/des_princ) (Open Telecom Platform) is the standard library of actor patterns -- `gen_server`, `gen_statem`, `supervisor` -- and is what most production Erlang systems actually use.

### Akka

[Akka](https://akka.io/) brought the model to the JVM (originally Scala, now also Java). It exposes actor references, mailboxes, and supervision in roughly the Erlang shape, but built on top of cooperative dispatchers running on a shared thread pool rather than preemptive lightweight processes. The trade-off: actors are still cheap, but a misbehaving actor that does CPU-bound work can starve its dispatcher. The Akka ecosystem extends the core with persistence (event-sourced actors), clustering, sharding, and streams.

### Other lineages

- **Pony** ([ponylang.io](https://www.ponylang.io/)) is an actor language with a type system (reference capabilities) that statically prevents data races, even when sending references between actors.
- **Microsoft Orleans** introduced the *virtual actor* model: actors always exist logically, the runtime activates them on demand and migrates them across nodes transparently.
- **Smalltalk and Self** were not actor systems strictly, but their "everything is an object that receives messages" stance was a direct intellectual ancestor.
- **Modern languages** (Swift's [actors](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/#Actors), Rust's [`actix`](https://actix.rs/), Elixir built atop the BEAM) have brought variations of the model into mainstream use.

## Where the actor model differs from shared-state concurrency

Shared-state concurrency -- threads, mutexes, atomics -- treats entities as data structures sitting inside a process's address space, addressable by pointer. Two threads can both reach the same structure and must coordinate explicitly to avoid corrupting it.

The actor model treats each entity as a participant addressable by identity:

| Aspect | Shared-state | Actor model |
|---|---|---|
| Identity | Pointer (process-local) | Actor reference (often network-routable) |
| State sharing | Default; locks prevent corruption | Impossible; only messages cross the boundary |
| Failure | Corrupts shared state | Isolated to one actor |
| Location | Same address space | Local or remote, transparently |
| Scheduling | OS threads or fibers; visible to all participants | Per-actor mailbox; serial within, parallel across |
| Reasoning unit | The lock or atomic | The actor's message handler |

Both are still in wide use. Shared-state wins where the working set is small, the cores are local, and the performance overhead of message passing matters. Actors win where the system is distributed, fault tolerance is structural, and the entities have meaningfully independent lifecycles -- which is most large server systems.

## Limitations and criticisms

- **No built-in transactions across actors.** Multi-actor invariants must be coordinated explicitly, typically via [sagas](https://microservices.io/patterns/data/saga.html) or two-phase protocols. This is the same trade-off [aggregates](/wiki/cs/entity-addressing/aggregate-root) make: small consistency boundaries are easier to reason about but push coordination into application code.
- **Mailbox-bound back-pressure.** An unbounded mailbox can grow without limit if producers outpace consumers; a bounded mailbox blocks senders. Neither is automatic. [Reactive Streams](https://www.reactive-streams.org/) and Akka Streams emerged in part to address this.
- **Debugging is non-local.** A bug often manifests as a message arriving at an unexpected actor in an unexpected state -- finding the originator requires distributed tracing.
- **Type systems struggle.** Most actor implementations type a mailbox as "messages of type T", which means an actor that should respond to several message kinds either widens its type or uses runtime dispatch. Pony's capability system and Akka's *typed actors* address this with varying ergonomic costs.

## Further reading

- Hewitt, Bishop, Steiger. *[A Universal Modular Actor Formalism for Artificial Intelligence](https://dspace.mit.edu/handle/1721.1/6952)* (1973).
- Agha, Gul. *[Actors: A Model of Concurrent Computation in Distributed Systems](https://mitpress.mit.edu/9780262511414/actors/)* (1986).
- Joe Armstrong, *[Programming Erlang](https://pragprog.com/titles/jaerlang2/programming-erlang-2nd-edition/)*.
- [Wikipedia: Actor model](https://en.wikipedia.org/wiki/Actor_model).
