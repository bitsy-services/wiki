---
name: global-name-the-blocker
description: When stopping for input, name the one thing needed in a line; anything with a sensible default is stated as the default, not asked
metadata:
  type: feedback
---

2026-09-11, drafting the RoPE invariance page. The stop was legitimate —
`wiki-workflow.md` requires showing the opening before the body — but the ask
came at the end of a long message as a compound question ("does the opening
read right, and are you happy with the eight headings and the GPT-2 caveat?"),
followed by a second message ending "still waiting on your answer about the
opening and the eight headings." The user replied: "What specifically are you
waiting for?"

Hypothesis: the rule-mandated check and a decision that already had a default
were bundled into one question, so the real blocker was not legible. Only the
first needed the user; the second had a stated plan and should have been
announced as the default.

**Why:** a stop the user cannot decode costs a round-trip, which is the cost the
opening check exists to save.

Then: "I do not recall you showing me a paragraph." It had been shown — inside a
````markdown fence, as the last of six sections in a long message. Fenced and
last, it read as an appendix rather than the thing being asked about.

**How to apply:** when stopping, lead or end with one line naming exactly what
is needed ("your read of the `## Part` paragraph, yes or edits"). Everything
else goes in as "doing X unless you say otherwise." When the thing to review is
prose, put it first and render it as prose, not in a code fence; the evidence
and plan go after it, shorter. Related: [[unnecessary-prompting]].
