---
title: "Homoiconicity"
weight: 20
---

Homoiconicity is a property of programming languages in which programs are represented using the language's own data structures. The term combines the Greek *homo* (same) and *icon* (representation) -- code and data share the same form, and the language can manipulate its own code with the same tools it uses to manipulate any other data.

## Why it matters

When code is data, a program can inspect, generate, and transform other programs (or itself) at compile time or runtime using ordinary language constructs. This makes several things practical that are awkward or impossible in non-homoiconic languages:

- **Macros that operate on syntax.** Rather than text substitution (C preprocessor) or limited template expansion, homoiconic macros receive the program's actual structure as a data argument and return transformed structure. They are functions from code to code.
- **Domain-specific languages (DSLs).** Because the host language can restructure its own syntax trees, embedding a DSL is a matter of writing macros that translate DSL forms into host-language forms -- no external parser or code generator needed.
- **Serialization and transmission of code.** If code is a data structure, it can be serialized, sent over a network, and evaluated elsewhere. This is the foundation of mobile-code systems and some distributed computing models.
- **Metaprogramming and introspection.** Programs can reason about their own structure -- examining function definitions, rewriting optimization passes, or generating boilerplate automatically.

## Homoiconic languages

### Lisp

Lisp is the canonical example. All Lisp code is written as S-expressions -- nested lists that are also Lisp's primary data structure. The expression `(+ 1 2)` is simultaneously a function call and a list of three elements. Lisp's `quote` form prevents evaluation, letting you treat code as data:

```lisp
(defmacro when (condition &body body)
  `(if ,condition (progn ,@body)))
```

This macro receives code (the condition and body forms), restructures it into an `if` expression, and returns the new code. The backtick/comma syntax is just shorthand for list construction.

### Clojure

Clojure inherits Lisp's homoiconicity but extends the set of literal data structures beyond lists to include vectors `[]`, maps `{}`, and sets `#{}`. Clojure macros work the same way as Lisp macros -- they receive and return data structures that represent code:

```clojure
(defmacro unless [condition & body]
  `(if (not ~condition) (do ~@body)))
```

Clojure's emphasis on immutable data structures makes macro-generated code easier to reason about, since the data representing the code cannot be mutated after construction.

### Rebol and Red

Rebol (and its successor Red) take a different approach. Rather than parenthesized S-expressions, they use a flat block syntax where everything -- code, data, markup -- is composed from a common set of datatypes (words, blocks, strings, integers, etc.). A block `[print "hello"]` is both executable code and an inert data container depending on context:

```red
rule: [some digit]
parse "123abc" rule   ; uses the block as a parsing grammar
do [print "hello"]    ; uses the block as code
```

This design trades the regularity of S-expressions for a more natural-looking syntax while preserving the code-is-data property.

## Homoiconicity vs. reflection

Languages like Python, Ruby, and Java offer reflection -- the ability to inspect and sometimes modify program structure at runtime. This overlaps with homoiconicity but is not the same thing. Reflection operates on an *external* representation of the program (class metadata, method objects, AST nodes accessed through special APIs), whereas homoiconicity means the program's *primary* representation is already a manipulable data structure. The distinction is ergonomic: in a homoiconic language, metaprogramming is a natural consequence of the language's design, not a bolted-on API.
