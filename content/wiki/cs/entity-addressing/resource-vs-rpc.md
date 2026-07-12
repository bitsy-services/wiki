---
title: "Resource-Oriented vs. RPC"
weight: 50
---

Two architectural stances dominate the design of networked APIs. **Resource-oriented** designs (the [REST](https://en.wikipedia.org/wiki/REST) family) give every conceptually distinct entity its own URI and address it directly using a small, uniform set of verbs. **Remote-procedure-call** designs ([RPC](https://en.wikipedia.org/wiki/Remote_procedure_call): SOAP, XML-RPC, gRPC, JSON-RPC) expose operations on a service endpoint and pass entity identifiers as parameters.

The distinction maps cleanly onto the [broader entity-addressing tension](/wiki/cs/entity-addressing). REST treats each resource as a first-class object with a global, dereferenceable address. RPC treats resources as rows inside a service container, addressed by parameter rather than by URI.

The choice has consequences that outlast the API version: cacheability, evolvability, client tooling, and even what kind of company can use the API at all.

## RPC: methods on a service

RPC, as a programming model, predates the web. It traces back to Birrell & Nelson's *[Implementing Remote Procedure Calls](https://dl.acm.org/doi/10.1145/357980.357392)* (1984), with earlier antecedents in Xerox's Courier and Sun's [ONC RPC](https://datatracker.ietf.org/doc/html/rfc5531). The premise is that a network call should look like a local function call: the client invokes a named method on a remote service, the runtime serialises the arguments, the server deserialises them, runs the method, and returns the result.

A typical RPC interface looks like a list of verbs:

```text
CustomerService.getCustomer(id)
CustomerService.updateCustomer(id, fields)
CustomerService.listOrders(customerId, since)
OrderService.cancelOrder(orderId, reason)
```

The entity ("customer", "order") shows up as a *parameter* to the call. There is no separate notion of an addressable customer URL -- only `CustomerService` is addressable, and customers are rows reachable through it.

Modern RPC frameworks ([gRPC](https://grpc.io/), [Apache Thrift](https://thrift.apache.org/), [Cap'n Proto](https://capnproto.org/)) lean into this model. They define services and methods in an IDL, generate client stubs in many languages, and use efficient binary serialisation. The framework handles connection management, framing, and (with HTTP/2 underneath) multiplexing. The programming model is essentially the same as a local method call.

## REST: resources with their own URIs

REST -- *Representational State Transfer* -- was named and characterised by Roy Fielding in his 2000 PhD dissertation *[Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)*. Fielding was not inventing a new protocol; he was retrospectively describing the architectural style that made the World Wide Web scalable, in order to give designers vocabulary to preserve those properties.

The defining constraints, in Fielding's terms, are:

- **Client-server.** The two roles are separated.
- **Stateless.** Each request contains all information needed to interpret it; the server keeps no per-client session state.
- **Cacheable.** Responses are explicit about whether they are cacheable, by whom, and for how long.
- **Uniform interface.** All resources are addressed and manipulated through the same small set of operations.
- **Layered system.** Intermediaries (proxies, caches, gateways) can sit between client and server without the client knowing.
- **Code on demand** (optional).

The "uniform interface" constraint is what gives REST its character. It has four sub-constraints, but the one most directly relevant to the entity-addressing question is **identification of resources**: every resource has a URI, and the URI is the canonical way to refer to it.

A REST interface looks like a hierarchy of nouns:

```text
GET    /customers/42
PATCH  /customers/42
GET    /customers/42/orders?since=2026-01-01
POST   /orders/77/cancellations   (or DELETE /orders/77)
```

The customer is a first-class entity with its own URI. The orders belonging to that customer are themselves addressable. Any client that holds the URI can dereference it, link to it, cache it, share it. The service is no longer the container -- the URI namespace is.

## The trade-offs, viewed concretely

| Concern | RPC | REST |
|---|---|---|
| Addressing | Method + parameters | URI |
| Verbs | Per-method, unbounded | Small uniform set (GET/PUT/POST/PATCH/DELETE) |
| Caching | Application-defined, often absent | HTTP cache semantics built in (ETag, Last-Modified, Cache-Control) |
| Tooling | Generated stubs, single language stack per service | Universal: any HTTP client works |
| Discoverability | IDL describes methods | Hyperlinks in responses (HATEOAS, in the strict reading) |
| Versioning | Method-level (often) | URI-level or media-type-level |
| Streaming | First-class (gRPC streams, etc.) | Awkward (SSE, WebSocket as an escape hatch) |
| Performance | Binary protocols, multiplexed | Text-based by default; HTTP/2 helps |
| Mental model | "Calling a function on a remote object" | "Manipulating a resource by reference" |

Neither is universally better. RPC is a strong fit when both sides of the API are owned by the same team, when latency and bandwidth matter, when typed contracts are valuable, and when the operations do not map cleanly onto CRUD on resources (most internal microservice traffic). REST is a strong fit when the API has many unknown consumers, when intermediaries (CDNs, browsers, caches) should be able to participate without special knowledge, when long-term evolvability matters more than peak efficiency, and when the domain genuinely is resource-shaped.

## "REST" in practice

A widely cited piece by Leonard Richardson divides the design space into a [maturity model](https://martinfowler.com/articles/richardsonMaturityModel.html):

- **Level 0** -- one URI, one verb (POST), arbitrary RPC-style bodies. The "REST" label is decorative.
- **Level 1** -- multiple URIs (resources), still one verb. Resources exist; verbs do not.
- **Level 2** -- multiple URIs and HTTP verbs. The common interpretation of "REST" in industry. Most API providers stop here.
- **Level 3** -- adds [hypermedia](https://en.wikipedia.org/wiki/HATEOAS) -- responses include links to related resources, so clients discover the API rather than hard-coding URIs.

Fielding has [argued forcefully](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven) that only Level 3 is actually REST in his original sense; what most people call REST is "Level 2 with REST styling". The pragmatic argument for stopping at Level 2 is that hypermedia is genuinely useful only when clients are written to discover at runtime -- and almost none are, because almost all clients are written against a known API version with code-generated bindings.

## The pendulum

The split has swung several times.

- **1980s-90s.** RPC dominates the internal-systems world (Sun RPC, DCE, CORBA). The web is a content delivery system, not an integration substrate.
- **Late 1990s.** SOAP arrives, attempting to bring RPC-over-HTTP with WSDL contracts. It collapses under its own weight (XML, WS-* specifications, generated tooling that does not interoperate).
- **Mid 2000s.** "REST" rises as a backlash -- simpler, HTTP-native, browser-friendly. AWS exposes both SOAP and REST endpoints early on and the REST ones win.
- **2010s.** The microservice era turns out to need a lot of internal service-to-service traffic where the resource model is awkward and the overhead of HTTP+JSON matters. gRPC, Thrift, and increasingly typed-IDL approaches return for the internal layer.
- **2020s.** [GraphQL](https://graphql.org/) and tRPC blur the line further. GraphQL is RPC-flavoured (a single endpoint, a query language) but resource-aware (queries describe the shape of a graph of typed nodes with stable IDs). tRPC drops the IDL and uses TypeScript types as the contract.

The current pattern in many organisations is "REST or GraphQL at the public edge, gRPC inside" -- the resource-oriented model where addressability and evolvability matter, the RPC model where the consumers are known and efficiency matters.

## The deeper question

What the debate keeps litigating is whether a resource is a *thing the API talks about* or a *thing that exists in its own right at an address*. RPC takes the first view: customers are mentioned in `CustomerService` calls, they are not themselves the address. REST takes the second: the customer at `/customers/42` *is* the customer, in the same way that an [actor's PID](/wiki/cs/entity-addressing/actor-model) *is* the actor, the [aggregate root's identity](/wiki/cs/entity-addressing/aggregate-root) *is* the aggregate, or an [OODBMS object's OID](/wiki/cs/entity-addressing/relational-vs-oodbms) *is* the object.

The decision is identical in structure to every other layer of the stack where the same [container-vs-objects question](/wiki/cs/entity-addressing) arises. The web-architecture vocabulary is just the most user-visible one.

## Further reading

- Fielding, Roy T. *[Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)* (2000).
- Fielding, Roy T. *[REST APIs must be hypertext-driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)* (2008).
- Birrell, A., Nelson, B. *[Implementing Remote Procedure Calls](https://dl.acm.org/doi/10.1145/357980.357392)* (1984).
- Martin Fowler, *[Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)*.
- Google, *[API Design Guide](https://cloud.google.com/apis/design)* -- a resource-oriented design guide for what is largely a gRPC ecosystem.
