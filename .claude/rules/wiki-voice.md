# Wiki Voice

The register is a knowledgeable colleague at a whiteboard: interested in the
subject rather than in the reader's reaction to it, and content to let a good
fact land on its own. A page earns attention by being dense with information,
not by announcing that what is coming will be important.

A pass over a page in this register is called **deadpanning** it. "Deadpan
`content/wiki/ai/llm/`" means run this file over those pages.

## Three tests on the finished page

These are checks on output. Apply them by reading the page back, not by writing
toward them — the rules this file used to contain were drafting instructions,
and following them produced worse pages than having no rule at all.

**1. After the first paragraph, can a reader say what the thing is?**

Name the object — the data structure, the mechanism, the part — not what it
accomplishes. Two pages have failed this in opposite directions: one described
behaviour for four paragraphs without ever saying what the thing *was*, the
other named it in eight undefined terms. If answering needs a link, the
paragraph has not done its job.

**2. Does every sentence parse when read aloud?**

*"The activation tensor that carries one token position from the embedding
tables to the unembedding"* shipped, passed the gate, and survived a subagent
review. It is not a sentence. Density is not a defence, and a green
`scripts/check.sh` says nothing about this — it checks links, anchors, fences,
frontmatter and acronyms, and cannot see prose.

**3. Is every term plain English, glossed in the same sentence, or in the
glossary?**

A link is not a gloss. The reader arrived from a search engine and will not open
eight tabs to finish the first sentence. Link *and* gloss.

## Write to the reader's next question

Before drafting, list the questions a cold reader asks, in the order they arise,
and check the page answers them in that order. For the residual stream they
were: what is it made of, is it per token or shared, how many are there, what
is the limit, what happens at the limit. That list is the page's spine and is
worth more than any amount of guidance about phrasing.

## Open with the thing itself

A lede's work is the definition and the mechanism: what it is, what it does,
what it is made of. Provenance, citations and scope caveats come later, at the
claim they bear on — in the opening they answer a question the reader does not
have yet.

## Show significance as consequence

When something is the crux, give the reader the fact that makes it the crux —
the number, the failure it causes, the thing that becomes possible — and let
them draw the appraisal.

- *Consequence:* "A push payment is complete the moment it is pushed, so there
  is no consumer-facing recall."
- *Consequence:* "Feeding 1025 tokens raises `IndexError` in the position
  lookup: the limit is a table with 1024 rows, not a degradation."

Superlatives are claims like any other, so support one in the same paragraph
with a measurement or a comparison.

## Metaphor: prefer none

If the reader has no way to picture the mechanism yet, one analogy — introduced
once, mapped explicitly, then dropped for the literal terms. Never in the
opening, and never as the page's organising idea. The reader should leave
holding the machinery, not the metaphor.

Anthropomorphism is the failure mode to watch. A component does not *want*,
*decide*, *know* or *shrug*. *Read* and *write* are borrowed from the
literature and are fine where the source uses them, but say what the arithmetic
is before leaning on them.

## Name the view you are disagreeing with

Positioning against another explanation is worth doing when the disagreement is
specific. Name the source, quote the claim, and say what it holds only for:
*the Uniswap docs describe fee growth as accruing to the position, which is true
once the position is touched and misleading before that.* That is checkable, and
it teaches the reader something on the way past. A page can also simply make the
correct claim well and let it stand alone.

## Address the reader where there is something to do

Second-person imperatives belong in procedures and `Check` sections, where the
reader is running a command or reading a table. In explanation, the third person
keeps the subject in the foreground.

## Two rules that used to be here

Both produced the worst pages in the wiki, and both are gone:

- *"Motivate before mechanism — establish the gap the reader should feel, and
  why the obvious approach falls short, before the mechanism arrives."* This
  produced openings that spend four paragraphs on a strawman design.
- *"The check is deletion: cut a sentence, and if nothing was lost, fold it into
  the sentence it was introducing."* This produced compression past coherence.

The general lesson is that a rule distilled from one correction gets applied
with more force than the correction had. **If a rule in this file is making a
page worse, say so at the time** rather than following it and reporting the
result afterwards.
