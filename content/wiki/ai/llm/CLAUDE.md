# Large Language Models — Writing Standard

These pages teach the concepts of the LLM space — how a model is built, how it
runs, how it was trained, and what it costs — to a reader who is a strong
engineer with no ML background. They are the on-ramp, not a recap for someone
who already knows the material.

The scope is not only what's inside the model. Training (loss, backprop,
fine-tuning, RLHF) and serving (KV cache, context length, speculative decoding)
belong here too. If a concept lives in the LLM space and a reader needs it, it
gets a page.

`_index.md` is the section's landing page and the wiki's link target for "large
language model" as a concept. It teaches the topic at a high level and hands off
to the subpages; keep it readable on its own, and don't restate this standard
there.

## Every page is the manual for one named part

Same headings, every page, in this order, so a reader who has used one page
knows where to look on the next.

| # | Heading | Holds |
| --- | --- | --- |
| 1 | `Part` | What the thing is: name, job, where it sits |
| 2 | `Data` | Table — name, contents, GPT-2 small size, who writes it, who reads it |
| 3 | `Transforms` | Numbered: pile → operation → pile |
| 4 | `Fits here` | Neighbours left and right, sequence top and bottom, reading order |
| 5 | `Does not do` | Wrong jobs, each linked to the page that does that job |
| 6 | `Related parts` | Contains / used by / see also, and the sources |
| 7 | `Check` | One runnable check, with the shape or number to expect |
| 8 | `Spec` | GPT-2 small constants only |

`Fits here` uses the spatial conventions in `conventions.md` — depth left to
right, sequence top to bottom. The reading order that used to live in a closing
"Depends on / leads to" line goes here as one sentence, and must stay consistent
with the sidebar `weight`.

### `Part` is the whole job of the page

One to three sentences — not one. The strict one-sentence version of this rule
produced *"the list of numbers a transformer keeps for each chunk of input
text"*, where *chunk* was a dodge around *token*. Spend the extra sentence and
name the thing.

The test is the first in `.claude/rules/wiki-voice.md`: after `Part`, a reader
can say what the object is without following a link. Name the data structure —
the list of numbers, the table, the matrix — not what it accomplishes.

Provenance and scope caveats do not belong in `Part`. A citation goes at the
claim it supports; "this page assumes pre-norm" goes beside the post-norm
contrast in `Transforms`. Both were in `Part` once, and both answered a question
the reader did not have yet.

## No bare jargon

Every term not pinned in `glossary.md` is defined in the same sentence that
first uses it. **A link is not a definition.** Link *and* gloss: the reader
arrived from a search engine and will not open eight tabs to finish a sentence.

This applies to code and notation. A tensor attribute, a keyword argument or a
matrix name is jargon — say what it does before leaning on it. A table keyed on
`wte`, `c_proj` and `ln_f` needs those named above it, not a cross-reference to
the page that names them.

## Cite the source

Most of this material is someone's paper. Name it at the claim it supports, with
a link — Elhage et al. 2021 for the residual stream and the circuits framing,
Vaswani et al. 2017 for the original architecture. Restating a paper without
attribution reads as invention.

## GPT-2 is the worked example, not the universe

GPT-2 small is what every `Check` runs against. Where a claim holds for GPT-2
and not for transformers generally — pre-norm, learned position tables, tied
embeddings — say so at the claim. `gpt-2.md` lists the swappable choices.

## Length follows the concept

There is no word cap. A page runs as long as teaching its one concept takes.
Brevity is not the goal; a reader who finishes and understands is.

## Structural rules

- **One concept per page.** If two ideas need each other, they get two pages and
  a link.
- **Fixed vocabulary.** Terms pinned in the glossary are reused exactly, with no
  synonyms for variety. `glossary.md` lists the words this subsection avoids.
- **Glossary entries are one-line specs**, not metaphors.
- **Diagrams follow the spatial convention** in `conventions.md`, which never
  varies from page to page. Use as many as help.
- **`Check` is falsifiable and has been run.** Quote the number it actually
  printed, not the number it should print, and say how to make it fail so the
  reader knows it is not vacuous.
