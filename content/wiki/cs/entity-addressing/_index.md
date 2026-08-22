---
title: "Entity Addressing"
weight: 25
bookCollapseSection: true
---

A recurring tension runs through computer science: when you model a collection of related entities, do you treat them as **rows inside a container** -- addressed by *(container, local id)* -- or as **first-class objects** with their own identity, addressable directly?

The choice is rarely framed in those terms, but it shows up everywhere. Databases, domain modelling, programming-language design, distributed systems, and web architecture all wrestle with the same question, often arriving at incompatible answers that then have to be reconciled at every boundary.

## The two stances

| Aspect | Container-with-rows | First-class objects |
|---|---|---|
| Identity | Local to the container (`order #42 inside cart #7`) | Global (`actor pid <0.123.0>`, `URI /orders/42`) |
| Addressing | Indirect: navigate container, then look up by key | Direct: dereference the reference |
| Lifecycle | Coupled to the container | Independent |
| Sharing | Hard -- the row "belongs to" one container | Natural -- any holder of the reference can use it |
| Consistency | Easy within the container, hard across | Each object is its own boundary |
| Cost | Cheap storage, simple schemas | Per-object overhead, identity bookkeeping |

Neither stance is universally right. Container-with-rows wins when the contained entities have no meaningful existence outside the container -- order line-items, journal entries in a ledger transaction, characters in a string. First-class objects win when the entities are referenced from multiple places, evolve on independent timelines, or need to be observed and addressed by parties who do not know about the container.

## Where the tension surfaces

- **[Relational vs. object-oriented databases](/wiki/cs/entity-addressing/relational-vs-oodbms)** -- Codd's relational model normalises everything into tables of rows joined by foreign keys; OODBMSs gave each entity its own object identity and let applications follow references. The "object-relational impedance mismatch" is exactly the cost of translating between the two views every time an object-relational mapping (ORM) layer marshals data.
- **[Aggregate roots](/wiki/cs/entity-addressing/aggregate-root)** in domain-driven design make the distinction explicit at the modelling layer: an aggregate has one externally addressable root, and interior entities are addressed *through* the root rather than directly. This is the container stance applied deliberately, to limit what external code can entangle itself with.
- **[The actor model](/wiki/cs/entity-addressing/actor-model)** takes the opposite stance to its logical conclusion: every entity is its own actor with a globally unique identity (a PID, an actor reference), private state, and a mailbox. There is no enclosing container -- the runtime addresses actors directly and routes messages to them.
- **[First-class vs. second-class entities](/wiki/cs/entity-addressing/first-class-entities)** in programming-language theory frames the same distinction over language constructs. A first-class entity can be named, stored, passed, and returned; a second-class one lacks one or more of those affordances and must be referred to indirectly through whatever container privileges it.
- **[Resource-oriented vs. RPC](/wiki/cs/entity-addressing/resource-vs-rpc)** at the web layer: REST gives each resource its own URI and addresses it directly with uniform verbs; RPC exposes operations on a service and passes resource IDs as parameters. The same domain can be exposed either way, and the choice has lasting consequences for cacheability, evolvability, and how clients are written.

## Why the choice keeps coming back

The pattern recurs because each level of the stack faces the same trade-off independently. A storage engine chooses how to lay rows out on disk; a domain model chooses how to expose those rows to business logic; a service layer chooses how to expose the domain to clients; a UI chooses how to address widgets. At each level, the designer either commits to local-id-within-a-container (cheaper, more rigid) or to globally addressable first-class objects (more flexible, more bookkeeping).

The mismatches between layers -- ORM impedance, REST-over-RPC adapters, actor references serialised through database foreign keys -- are the visible scars of choices made differently at different levels of the same system. Recognising the underlying distinction makes it easier to see why a particular boundary feels awkward and what the alternatives would cost.

## Wiki Pages

{{< section >}}
