# Neural Network — Writing Standard

These pages teach the parts every neural network is built from — what the object
is, what each component does, and how training fills in the weights — to a
reader who is a strong engineer with no ML background. They are the prerequisite
for `content/wiki/ai/llm/`, which assumes them.

Inherit the LLM section's standard (`../llm/CLAUDE.md`): summary-first opening
paragraph, motivate before mechanism, no bare jargon, length follows the
concept, one concept per page, end with a falsifiable check and a
"Depends on / leads to" line consistent with the sidebar `weight`.

Everything below is what differs.

## Architecture-neutral framing, concrete examples

This is the rule the section exists to enforce, and the one most easily lost.

- **The framing must be neutral.** The opening paragraph and every section
  heading describe the general object. A page whose first sentence says
  "transformer" is misfiled — that was the bug this section was created to fix.
- **The examples should be concrete.** GPT-2 small is the worked example
  throughout, because it is small enough to run on a laptop and every
  `Check yourself` is reproducible against it. Naming it is fine. Framing the
  page around it is not.

The test: could this page stand unchanged if the wiki grew a section on
convolutional networks or diffusion models? If yes, the framing is neutral. If a
paragraph would have to be rewritten, rewrite it now.

When the transformer's version of a mechanism is substantial enough to teach
separately, it gets its own page under `llm/` and the two link to each other —
`multi-layer-perceptron.md` here and `llm/the-mlp.md` there are the worked
example of that split.

## Vocabulary

`glossary.md` pins this section's terms. Two deliberate divergences from `llm/`:

- **Use "layer" freely.** It means one multiply-and-bend, and it is the general
  literature's word. The LLM section drops it because inside a transformer it is
  ambiguous between a block and a piece of one; that ambiguity does not exist
  here.
- **Do not use `llm/` vocabulary.** *Row*, *residual stream*, *`d_model`*,
  *block*, *head*, and *attention pattern* are transformer terms. Say
  *activations*, *running total*, *width*, *layer*. Link to the `llm/` page when
  naming the transformer's version of something.

**bend**, **unit**, and **feature** are defined here, not in `llm/glossary.md`.
Don't reintroduce them there.

## Linking direction

Links from here into `llm/` are fine for worked examples and for "the
transformer's version of this" pointers — `gpt-2.md` and `running-the-checks.md`
in particular, since the checks depend on that setup. Links the other way are
the normal prerequisite direction and need no justification.
