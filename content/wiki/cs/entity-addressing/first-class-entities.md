---
title: "First-Class vs. Second-Class Entities"
weight: 40
---

In programming-language theory, an entity is **first-class** if it can be treated like any other value in the language: named with a variable, passed as an argument, returned from a function, stored in a data structure, and tested for equality. An entity is **second-class** if it lacks one or more of those affordances and must instead be referred to indirectly -- through whatever container or syntactic construct privileges it.

The terminology is due to Christopher Strachey's 1967 lecture notes *[Fundamental Concepts in Programming Languages](https://web.archive.org/web/20060326035955/http://www.cs.cmu.edu/~crary/819-f09/Strachey67.pdf)*, where he observed that in many languages "procedures are second-class citizens -- they always have to appear in person and never can be represented by a variable or expression." The phrase stuck, and the distinction it captures has turned out to be one of the most useful lenses for comparing language designs.

It is also a clear instance of the [container-vs-objects tension](/wiki/cs/entity-addressing). A second-class entity exists only inside some enclosing construct (a function definition, a class, a module); the only way to refer to it is to refer to its container and pick it out by name. A first-class entity has its own identity that can be carried around independently of any container.

## What "first-class" actually requires

The usual checklist, formalised by various authors but consistent in spirit:

- **Bindable to a name.** `let f = ...` works for any first-class entity.
- **Passable as an argument.** A function takes it as a parameter.
- **Returnable from a function.** A function can produce it as its result.
- **Storable in a data structure.** It can live in a list, a tuple, a map.
- **Constructible at runtime.** Not just declared statically but built dynamically.
- **Anonymous.** It does not require a name to exist -- a literal form is available.

Different authors emphasise different subsets, but the spirit is uniform: a first-class entity is a value, and the language treats it the way it treats other values. A second-class entity is a syntactic or semantic construct that the language can refer to but not, in itself, manipulate.

## Classic examples

### First-class functions

The original case Strachey called out. In ALGOL 60, [Pascal](https://en.wikipedia.org/wiki/Pascal_(programming_language)), and pre-C99 C, functions could be defined and called but not constructed at runtime, not returned as values from other functions, not stored arbitrarily, and not anonymous. They were second-class.

In Lisp, ML, Haskell, Scheme, JavaScript, Python, and most modern languages, functions are first-class. The same `+` that adds two numbers can be passed to `map`, stored in a dictionary, returned from a factory, and built dynamically as a closure. This makes [higher-order programming](https://en.wikipedia.org/wiki/Higher-order_function) -- map, filter, fold, function composition -- a natural style rather than a workaround.

C's *function pointers* are the awkward middle ground: they let you pass functions around but only ones that were defined at compile time. There is no way to construct a new function at runtime, so closures must be simulated by hand-rolled struct-plus-function-pointer pairs. C++11 lambdas and Rust closures fixed this by making the compiler do the rolling.

### First-class types

In a language with first-class types, a type is a runtime value. You can compute one, pass it to a function, store it in a list of types, and pattern-match on it. [Dependent type systems](https://en.wikipedia.org/wiki/Dependent_type) -- Coq, Agda, Idris, Lean -- and dynamic languages with strong reflection (Python, Ruby) treat types as values.

C++ templates and Java generics are an interesting failure mode: types parameterise code but are not themselves values at runtime. You cannot say "give me the type that was passed in and store it in a list." You can ask whether one type is assignable to another, but only through reflection APIs that are clearly bolted on. This is the difference between *generic over a type variable* and *first-class with respect to types*.

### First-class continuations

Scheme's `call/cc` and Smalltalk's continuations make the call stack a first-class value: you can capture the rest of the computation as a function-like object and resume it later, possibly many times. This is the most extreme example of taking something that is usually invisible (the implicit return address) and making it a value the language can manipulate.

Most languages have second-class control flow: `return`, `break`, `continue`, exceptions. They can be used but not constructed, named, or stored. Generators (Python `yield`, JavaScript `function*`) and `async`/`await` are a middle ground -- they expose a *restricted* form of continuation as a value, enough to implement coroutines without going all the way to `call/cc`.

### First-class modules

In ML-family languages, *modules* are usually a separate language layer with their own (often more powerful) abstraction mechanisms but cannot be treated as values. OCaml's [first-class modules](https://v2.ocaml.org/manual/firstclassmodules.html) explicitly remove that restriction: a module can be packaged into a value, passed around, and unpacked. Standard ML and Haskell's type-class machinery work without first-class modules but bake more into the static type system to compensate.

### First-class environments / scopes

A few languages -- Tcl, some Smalltalks, [Kernel](https://web.cs.wpi.edu/~jshutt/kernel.html) (Shutt's Scheme dialect) -- expose the lexical environment as a value. This collapses the usual gap between "compile-time lexical scope" and "runtime data" but tends to defeat optimisation, because the compiler can no longer assume that a name resolves the same way each time.

## Why the distinction matters

Making something first-class is not free. It costs:

- **Runtime representation.** A first-class function needs a closure object (function pointer + captured environment). A first-class type needs a runtime type descriptor.
- **Optimisation barriers.** First-class entities tend to be opaque to the compiler; a function-as-value can be called through any pointer, defeating inlining.
- **Type-system complexity.** Anywhere a second-class construct is now a value, the type system has to be able to describe its type -- function types, kinds, dependent types, module signatures.

In return, you get:

- **Abstraction without boilerplate.** Higher-order functions replace whole categories of design pattern. The Strategy and Visitor patterns are largely artefacts of languages without first-class functions.
- **Compositional libraries.** A library that takes a first-class function can adapt to any caller's needs; a library that takes a "callback interface" with one method is doing the same thing more verbosely.
- **Reflection and metaprogramming.** First-class types and modules are the basis of generic programming, object-relational mappers (ORMs), serialisation, and dependency injection.

The trade-off is the language designer's recurring problem, and the answer differs by language because different runtimes can afford different costs. A systems language is happy to keep continuations second-class to avoid the heap allocation; a research language is happy to make everything first-class to keep the semantics clean.

## Connection to the broader pattern

The container-vs-objects distinction from [entity addressing](/wiki/cs/entity-addressing) shows up here in two related ways:

- **At the language level**, a second-class entity is a *row in a container*: a method exists inside a class, a function definition inside a module, a continuation inside a stack frame. To refer to it, you have to name the container and pick it out. A first-class entity is a *standalone object*: it has its own identity as a value and can be passed around without dragging the container with it.
- **At the design level**, the choice of how many things to make first-class has the same flavour as the choice between [relational rows](/wiki/cs/entity-addressing/relational-vs-oodbms) and [OODBMS objects](/wiki/cs/entity-addressing/relational-vs-oodbms), or between [aggregate-internal entities](/wiki/cs/entity-addressing/aggregate-root) and externally-referenceable roots. Each level of the stack faces a version of the same question.

The history of programming-language design is in large part the history of making more things first-class -- functions, then types, then modules, then continuations, then effects -- because each promotion enables abstractions that were too painful to express before. The cost is paid once in runtime and tooling; the benefit accrues forever in expressiveness.

## Further reading

- Strachey, Christopher. *[Fundamental Concepts in Programming Languages](https://web.archive.org/web/20060326035955/http://www.cs.cmu.edu/~crary/819-f09/Strachey67.pdf)* (1967) -- where the term originates.
- [Wikipedia: First-class citizen](https://en.wikipedia.org/wiki/First-class_citizen).
- Felleisen, Friedman, Krishnamurthi, Wand. *[Essentials of Programming Languages](https://eopl3.com/)* -- on continuations and higher-order language design.
- John Reynolds, *[Definitional Interpreters for Higher-Order Programming Languages](https://homepages.inf.ed.ac.uk/wadler/papers/papers-we-love/reynolds-definitional-interpreters-1998.pdf)* (1972).
