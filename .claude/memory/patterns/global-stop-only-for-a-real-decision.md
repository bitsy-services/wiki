---
name: global-stop-only-for-a-real-decision
description: A stop for the user's input costs a round trip; finish the work, announce defaults, and stop only for a decision the user alone can make, named in one line
metadata:
  type: feedback
---

Consolidates three Gen 0 observations (`global-unnecessary-prompting`,
`global-name-the-blocker`, `project-opening-check-out-of-context`) on
2026-10-18. The recurring issue is stopping to ask when the work could have
continued. Each instance cost a round trip and asked the user for a judgement
they did not need to make, or could not make well.

- **Closing questions.** Ending a finished task with "Want me to adjust
  anything?" or "Should I proceed?" when the direction was already clear. It
  shifts load onto the user and implies uncertainty where there is none; the
  user can volunteer changes unprompted.
- **An illegible stop.** 2026-09-11, RoPE invariance page. A legitimate stop
  (the opening check) was bundled with a decision that already had a default,
  as one compound question at the end of a long message, and the prose to
  review sat in a code fence as the last of six sections. The user asked
  "What specifically are you waiting for?" and then "I do not recall you
  showing me a paragraph."
- **A stop for a fragment.** Same session: following `wiki-workflow.md`
  ("Show the opening before writing the body"), the opening paragraph was
  shown for approval. After two rounds of confusion the user said: "I don't
  want to read something out of context. Use your judgement. If I don't like
  it I will tell you."

**Why:** a stop the user cannot decode, or one that asks them to judge a
fragment without its context, costs the round trip it was meant to save.

**How to apply:** finish the work, run the gate and the reviewer, and present
the result with the opening where the user sees it first. Announce anything
with a sensible default as the default ("doing X unless you say otherwise")
rather than asking. Stop only when proceeding under any assumption would make
the work wrong or unsafe; then name exactly what is needed in one line, and put
any prose to review first, rendered as prose, not in a code fence.

**Open conflict:** `wiki-workflow.md` still says to show the opening before
drafting the body. The user's words are the more recent evidence, so follow
them; changing the rule is a Gen 2 promotion and needs the user's yes.

Related: [[global-permission-and-config-hygiene]] (asking before widening
permissions is the exception), [[project-forward-links-block-the-turn]].
