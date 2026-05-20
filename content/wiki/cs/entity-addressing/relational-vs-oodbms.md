---
title: "Relational vs. Object-Oriented Databases"
weight: 10
---

The relational and object-oriented database camps disagreed about the most basic question a data store has to answer: **what is an entity, and how do you point at one?** The relational model says an entity is a row in a table, identified by the values of its primary-key columns and reachable only by querying that table. An object-oriented database (OODBMS) says an entity is an object with its own machine-level identity, reachable by following a reference -- much like a pointer in a programming language.

Both models survived, but uneasily, and the friction between them is the source of the long-running ["object-relational impedance mismatch"](https://en.wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch) literature and the entire ORM industry that grew up around it. It is a textbook case of the larger [entity-addressing tension](/wiki/cs/entity-addressing).

## The relational model

Edgar F. Codd proposed the relational model in his 1970 paper *[A Relational Model of Data for Large Shared Data Banks](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)*. Its design choices are by now invisible because they won:

- Data lives in **relations** (tables). Each row is a tuple of values.
- A row is identified by the values of its **primary key**, not by any internal identity. Two rows with identical column values are, by definition, the same row.
- Relationships between rows are expressed by **foreign keys** -- a column in one table holding the key value of a row in another.
- The model has no notion of a pointer. Navigation happens through declarative queries (SQL joins), and the query optimiser is free to plan the access however it likes.

Codd's principle of [physical data independence](https://en.wikipedia.org/wiki/Data_independence) follows directly: because rows are addressed by value, the storage engine can move them around -- reorganise indexes, page them in and out, partition them -- without breaking any reference held by application code. There are no references to break.

This is the container-with-rows stance in its purest form. A row exists *inside* a table, addressed by *(table, key)*. It has no independent existence.

## The object-oriented databases

By the late 1980s, application code was largely written in object-oriented languages -- Smalltalk, C++, later Java -- and the cost of translating between the two worlds on every read and write had become obvious. A movement formed around the [Object-Oriented Database System Manifesto](http://www.cs.cmu.edu/~clamen/OODBMS/Manifesto/) (Atkinson et al., 1989), which argued that the database should speak the language's native vocabulary directly.

The notable systems were:

- **[ObjectStore](https://en.wikipedia.org/wiki/ObjectStore)** (Object Design, Inc., 1988) -- mapped database objects directly into application virtual memory using a technique called *pointer swizzling*. C++ code could chase pointers across persistent objects without knowing they were stored on disk.
- **[GemStone](https://en.wikipedia.org/wiki/GemStone/S)** (Servio Logic, 1986) -- a persistent Smalltalk image; the database *was* the object graph.
- **[Versant](https://en.wikipedia.org/wiki/Versant_Corporation)**, **[O2](https://en.wikipedia.org/wiki/O2_(database))**, and **[Objectivity/DB](https://en.wikipedia.org/wiki/Objectivity/DB)** -- variations on the same theme for various language bindings.

What unified them was the **object identity** model. Each persistent object was assigned an OID (object identifier) by the database, distinct from any of its attribute values. Two objects with identical attributes were still distinct objects -- as they would be in the host language. References between objects were direct: not "look up the customer with id 42 in the customer table", but `order.customer`.

This is the first-class-object stance. An object exists in its own right, addressed by its OID, regardless of which collection currently holds it. Adding or removing it from a collection does not change its identity.

## What "impedance mismatch" actually means

The friction between the two models is not just stylistic. It shows up in several concrete places:

- **Identity.** In SQL, `row1 = row2` iff their column values match. In an object model, `obj1 == obj2` iff they are the same object regardless of attribute values. Reconciling the two requires the ORM to maintain an *identity map* -- a per-session table mapping primary keys to in-memory object instances -- so that two queries returning "the same row" yield the same object reference.
- **Inheritance.** Object models support `Manager extends Employee`. SQL has no native equivalent; the ORM must pick a mapping (single-table, joined, or table-per-class), each with its own performance and constraint trade-offs.
- **Associations.** An object reference is one-directional and cheap. A SQL foreign key is also one-directional, but joining across it is not free, and bi-directional navigation requires either denormalisation or two foreign keys to keep in sync.
- **Collections.** `customer.orders` is an attribute in an object model. In SQL it is a query (`SELECT * FROM orders WHERE customer_id = ?`) whose result is materialised lazily, eagerly, or in batches depending on configuration -- giving rise to the infamous *N+1* problem.
- **Transactions.** Object models implicitly track mutations to in-memory objects; the ORM must flush those mutations to the database at the right moments, in the right order, without violating foreign-key constraints.

ORMs like Hibernate, SQLAlchemy, ActiveRecord, and Entity Framework exist to manage exactly this translation, and most of their complexity comes from doing it transparently enough that application code can pretend it is just operating on objects.

## Why the relational model won (mostly)

OODBMSs occupied a real niche -- CAD/CAM systems with deeply linked geometry, telecommunications network models, scientific data with rich type hierarchies -- but never displaced the relational model for general business data. The reasons are usually summarised as:

- **Declarative queries.** SQL's `SELECT ... WHERE ...` is expressed in terms of *what* you want, not *how* to get it. The query optimiser can change strategies as data grows. Pointer-chasing through an object graph is inherently imperative; the application encodes the access plan.
- **Schema as contract.** Tables and columns are a stable, language-agnostic schema. Object models tie the schema to the host language's class definitions, making cross-language and cross-application access awkward.
- **Mature tooling.** Decades of investment in indexing, query optimisation, replication, backup, analytics, and reporting all assumed the relational model.
- **Standardisation.** ANSI SQL provided a single target. The OODBMS world had the [ODMG](https://en.wikipedia.org/wiki/Object_Data_Management_Group) standard, but vendor implementations diverged early.

The compromise the industry settled on was the **object-relational mapper** running over a relational store, plus, later, **object-relational databases** like PostgreSQL that add object-like features (composite types, table inheritance, arrays) on top of a fundamentally relational core.

## The pendulum

The container-vs-object debate did not end; it migrated.

- **Document stores** (MongoDB, CouchDB) sit closer to the object camp -- a document has its own identity (`_id`), can be retrieved directly without a join, and nests its sub-entities as embedded sub-objects. The trade-off they reintroduced is the difficulty of cross-document consistency.
- **Graph databases** (Neo4j, Dgraph) take the object stance further still: nodes are first-class entities, edges are first-class entities, and the language is built around traversal rather than joins.
- **[Content-addressed stores](/wiki/cs/dag)** (Git, IPFS) push the object stance to its limit: an entity's identity is the hash of its content. There is no enclosing container at all -- references are global, immutable, and verifiable without any directory lookup.
- **Modern ORMs** (Prisma, Drizzle) have largely retreated from the goal of "objects all the way down" and now embrace SQL as a first-class output, generating typed query builders rather than hiding the relational model. The mismatch is acknowledged rather than concealed.

The relational model's victory in operational data stores is now more than fifty years old, but the underlying question -- whether an entity is a row in a container or an object with its own identity -- remains a live design choice every time a new storage layer is built.

## Further reading

- Codd, E. F. *[A Relational Model of Data for Large Shared Data Banks](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)* (1970).
- Atkinson et al. *[The Object-Oriented Database System Manifesto](http://www.cs.cmu.edu/~clamen/OODBMS/Manifesto/)* (1989).
- Ted Neward, *[The Vietnam of Computer Science](http://blogs.tedneward.com/post/the-vietnam-of-computer-science/)* (2006) -- the canonical critique of ORM as an unwinnable middle ground.
- [Wikipedia: Object-relational impedance mismatch](https://en.wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch).
