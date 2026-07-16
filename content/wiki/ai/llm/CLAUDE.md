# LLM Internals — Writing Standard

These pages teach transformer internals to a reader who is a strong engineer
with no ML background. They are the on-ramp, not a recap for someone who
already knows the material.

These rules are for the writer. `_index.md` is reader-facing only — don't
restate the standard there.

## Start with the summary

The first paragraph is a high-level summary of the concept the page names —
what it is and what it's for, in plain language. No notation, no matrix names,
no dimensions, no numbers. A reader who stops after that paragraph should still
be able to say what the concept is and why it exists.

Detail starts in the second paragraph, never the first.

## Teach, don't recap

- **Motivate before mechanism.** Establish the gap the reader should feel — and
  why the obvious approach falls short — before the mechanism arrives. Give it a
  reason to exist.
- **Build in named steps.** Section headings are the reader's next question, not
  a taxonomy: "Why the score sees only the gap," not "Properties."
- **Reach for a concrete analogy** on the hardest idea. An everyday mechanism the
  reader already understands does more work than another equation.
- **Land the payoff.** End on what the concept buys — the capability it enables
  or the limit it explains.

## No bare jargon

Every term not pinned in the glossary (`glossary.md`) is defined inline at first
use or linked to a page that defines it. No exceptions. The glossary fixes this
subsection's recurring vocabulary; it is not a substitute for introducing a
concept.

If a term has no page yet, write a stub — `.claude/rules/wiki-linking.md`
requires it, and `scripts/check.sh` enforces the link.

This applies to code and notation too. A tensor attribute, a keyword argument,
or a matrix name is jargon: say what it does before leaning on it.

## Length follows the concept

There is no word cap. A page runs as long as teaching its one concept takes.
Brevity is not the goal; a reader who finishes and understands is.

## Structural rules

- **One concept per page.** If two ideas need each other, they get two pages and
  a link. A page doesn't teach everything about its subject; it teaches the one
  thing it names.
- **Fixed vocabulary.** Terms pinned in the glossary are reused exactly. No
  synonyms for variety. `conventions.md` lists the words this subsection avoids.
- **Diagrams follow the spatial convention** in `conventions.md`, which never
  varies from page to page. Use as many diagrams as help.
- **End with a falsifiable check** — a claim the reader can confirm or break in
  nanoGPT or GPT-2 small.
- **Close with "Depends on / leads to"** links. These set the subsection's
  reading order, so they must stay consistent with the sidebar `weight`.
