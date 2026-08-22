---
title: "Aggregate Root"
weight: 20
---

The **aggregate root** is one of the central tactical patterns from Eric Evans' *[Domain-Driven Design](https://www.domainlanguage.com/ddd/)* (2003). It is a deliberate, modelling-layer answer to the [entity-addressing question](/wiki/cs/entity-addressing): some entities should be referenceable from anywhere in the system, and others should be reachable only by going through one of those privileged entities.

An **aggregate** is a cluster of associated domain objects that should be treated as a single unit for the purposes of data changes. The **aggregate root** is the one entity in the cluster that the outside world is allowed to hold a reference to. Everything else inside the aggregate is addressed as *(root, local id)* -- second-class within the application's object graph, even if it happens to be persisted as its own row in a relational store.

## Why aggregates exist

The pattern solves three problems that show up in any non-trivial domain model:

1. **Consistency boundaries.** Some invariants involve multiple objects ("the sum of an order's line items must equal the order total"). Without a defined boundary, every change to any object could in principle violate any invariant, and the system becomes impossible to reason about. An aggregate declares: "these invariants are enforced together, atomically, inside this boundary."
2. **Concurrency control.** If the consistency boundary is explicit, concurrent modifications can be serialised at the boundary -- typically with an optimistic lock (a `version` column) on the root. Without aggregates, you either lock too little (and corrupt invariants) or too much (and kill throughput).
3. **Reference discipline.** Without rules, external code accumulates references to whatever interior objects happen to be convenient, and the model loses its shape. Aggregates make those references illegal, forcing callers to go through the root.

## The rules

Evans' formulation reduces to a handful of constraints:

- **One root per aggregate.** It is an [entity](https://en.wikipedia.org/wiki/Domain-driven_design#Building_blocks) -- it has a global identity and a lifecycle.
- **External references point only at the root.** Other aggregates, services, and repositories may hold a reference to the root but never to an interior entity or [value object](https://en.wikipedia.org/wiki/Value_object).
- **Interior entities have only local identity.** A line item's identity is meaningful only inside its order. The same numeric id in another order refers to a completely different line item.
- **The root mediates all changes.** External code calls methods on the root; the root may delegate internally, but invariants are checked at the root before returning control.
- **Repositories return only roots.** There is one [repository](https://martinfowler.com/eaaCatalog/repository.html) per aggregate type, and it loads and saves whole aggregates -- never half of one.
- **Transactions match aggregate boundaries.** A single transaction modifies exactly one aggregate instance. Multi-aggregate consistency, when needed, is achieved through [eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency) and [domain events](https://martinfowler.com/eaaDev/DomainEvent.html) rather than distributed transactions.

The classic example is an `Order` aggregate containing `OrderLine` entities. External code references the order by its order number; an order line is reached as `order.lineFor(productId)`. There is no `OrderLineRepository`. Cancelling an order, adding a line, applying a discount -- all go through methods on `Order`, which is responsible for keeping the total consistent with the lines.

## How aggregates relate to the broader tension

Aggregates make a conscious choice on each side of the [entity-addressing trade-off](/wiki/cs/entity-addressing) at different levels:

- **Externally, the root is a first-class object.** Other aggregates hold direct references to it (typically by its identity, not by an in-memory pointer, to keep aggregates independently loadable). The root has its own lifecycle and is durably addressable.
- **Internally, interior entities are rows in a container.** They are addressed by (root, local id). They cannot outlive the root. They cannot be referenced by anyone outside the aggregate.

This is the same distinction made by [relational databases vs. OODBMS](/wiki/cs/entity-addressing/relational-vs-oodbms), but applied at the *modelling* layer rather than the storage layer. An aggregate can be persisted to a relational store, an [object-oriented store](/wiki/cs/entity-addressing/relational-vs-oodbms), or a document store -- the pattern is about which entities the *application* treats as first-class, not how they happen to live on disk.

## Sizing aggregates

Aggregate size is the perennial design question, and getting it wrong has predictable costs:

- **Too large.** Every modification to any interior object loads, locks, and saves the whole aggregate. Concurrency drops; reads get heavier. A `Customer` aggregate that includes every order the customer has ever placed will collapse under its own weight.
- **Too small.** Invariants that should be enforced inside one aggregate end up split across two, requiring eventual-consistency machinery (domain events, sagas) where a single transaction would have sufficed.

The usual advice -- attributed to Vaughn Vernon in *[Implementing Domain-Driven Design](https://www.informit.com/store/implementing-domain-driven-design-9780321834577)* -- is to **prefer small aggregates**, reference other aggregates by identity, and reach for eventual consistency only when the use case genuinely tolerates it. A common failure mode is to start with an over-large aggregate because the relational schema suggested it; the schema is not the model.

## Aggregates and event sourcing

The aggregate boundary aligns naturally with [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html): the aggregate is the unit whose state is reconstructed by replaying its event stream. Each appended event is checked against the in-memory aggregate state, so invariants are enforced before the event is persisted. CQRS (command query responsibility segregation) systems typically use aggregates as the write model and a separate denormalised projection as the read model.

This pairs the pattern with another resolution of the [entity-addressing tension](/wiki/cs/entity-addressing): the *write* side treats data as first-class objects with strict boundaries; the *read* side flattens them back into row-shaped projections optimised for query patterns. The mismatch is moved out of the storage layer and into the model deliberately, rather than fought against in an object-relational mapper (ORM).

## When the pattern does not fit

DDD's tactical patterns assume a transactional, behaviour-rich domain. They fit awkwardly when:

- The system is essentially CRUD (create, read, update, delete) -- there are no interesting invariants, and an aggregate root adds ceremony without value.
- The data is naturally a graph with no clear roots -- social networks, knowledge graphs, dependency graphs. Forcing aggregate boundaries onto a graph either creates artificial roots or fragments the graph in ways that hurt queries.
- The dominant access pattern is analytical, not transactional. Aggregates exist to make transactional consistency cheap; an analytics workload does not need them.

In those cases the [first-class object stance](/wiki/cs/entity-addressing/actor-model), a document model, or a graph model often serves better than imposing aggregate boundaries that the domain does not actually demand.

## Further reading

- Evans, Eric. *[Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.domainlanguage.com/ddd/)* (2003) -- the original treatment.
- Vernon, Vaughn. *[Effective Aggregate Design](https://kalele.io/papers/)* -- a three-part essay specifically on sizing.
- Martin Fowler, *[DDD Aggregate](https://martinfowler.com/bliki/DDD_Aggregate.html)*.
