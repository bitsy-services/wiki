# Verbal Tics — Writing Standard

`anthropic-claude.md` is a ledger, and the other pages here are ordinary wiki pages under
the general rules. Everything below is about the ledger.

## Adding an entry

When the user points out a tic, in this repo or by pasting an example from
elsewhere, add it to `anthropic-claude.md`. Do not wait to be asked twice, and do not
argue that it is not a tic: a reader noticing it is the evidence.

1. Check the existing entries first. If the new observation is another filler
   for a slot that an entry already names, add the example to that entry and
   append `caught <date>` to its "Known by" cell. Do not create a second entry
   for the same frame.
2. Otherwise add a row at the bottom of the table for the register where it was
   seen (Words, Constructions, Paragraph and page shape, Conversation, Agentic
   work, Fiction), with the next unused number for that letter.
3. Name the **frame with its slot**, not the string: *The catch is*, *The trick
   is* and *The point is* are one entry. A phrase-level entry is answered with a
   synonym, which is the finding the mitigation page is built on.
4. Quote the example exactly, and link the wiki page it came from if it has one.
5. "Known by" is `caught YYYY-MM-DD`. Never mark a reader-supplied entry
   `named`: that mark means the model listed the habit unprompted on
   2026-10-05, and it is a historical fact about that draft.

## What does not change

- **Numbers are permanent.** Other pages cite `C1`, `W1`. Never renumber, never
  reuse a number, never delete an entry because the habit seems to have
  stopped. A model version that drops a habit can be followed by one that
  brings it back.
- **Counts are dated snapshots.** `wiki:` figures were taken on 2026-10-05 by
  `scripts/count-tics.py`, run on the tree at commit `c536471`, and the page
  gives the date. Do not update one figure in isolation. A recount replaces
  all of them and changes the date in "How an entry is known". C2 and C3
  over-match, so their figures are what was left after reading every match;
  W4 and W10 are run with `--exclude overused-words`, the page that lists
  those words, and the page says so.
- **No count without a source.** A `wiki:` or `novels:` figure is something a
  script printed or a cited page states. A rate recalled from memory is not
  entered.

## Writing these pages without committing the tics

A page about tics that is full of them undermines itself. Tables, block quotes
and code are quotation; prose is commitment. Before finishing any page in this
directory, read its prose against the Constructions table in `anthropic-claude.md`, in
particular C1 (*X, not Y*), C4 (*, which is why*), C6 (the em dash), C7 (the
closing maxim), C9 (*Two things follow*) and S1 (a bold label opening every
paragraph; use a `###` heading where the label is really a section, and plain
prose where it is not).
