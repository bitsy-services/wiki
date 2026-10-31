---
name: global-answer-the-request-in-its-own-terms
description: A request with a "how" in it wants one procedure page a reader can follow top to bottom, under a title in the request's words; reference pages come after and link from it
metadata:
  type: feedback
---

Consolidates two observations on the same section, `ai/claude-accounts/`.

- **2026-10-27.** The request asked for pages on "why and how to optimally and
  cost effectively use multiple Claude accounts". Eight pages shipped,
  organised by mechanism, after two review rounds and a green gate. With the
  cost page open in the editor, the user asked: "Which page tells me how to
  use multiple accounts cost effectively?" The answer was there, under a
  title naming a mechanism, in the page's fifth to seventh sections, as
  conditionals.
- **2026-10-30.** "This whole section is nearly useless. I want recipes for
  easily switching between accounts. Why, what, how. How to configure things,
  and how to switch. There needs to be one page that does not beat around the
  bush. It needs to be direct, and easy to follow." The setup existed, but
  spread across `config-directories`, `layouts` and `credentials`, each recipe
  wrapped in provenance, test notes and caveats, in the third-person reference
  register. The fix was a single page, `switching.md`, first in the sidebar:
  why in three bullets, what in one table, then numbered steps with
  copy-paste commands, then pitfalls.

**Why:** a reader who wants to do something scans for the steps. The wiki's
voice rules (third person, density, imperatives only in procedures) are
written for explanation; applied to a how-to request they turn the procedure
into reference prose that has to be assembled from several pages. Neither the
gate nor the reviewer checks a page against the request unless told to.

**How to apply:**

- List the goals the request names, in its own words, before choosing pages.
  Each gets a page or heading that answers it in those words, answer first.
- When a goal is a task ("how to set up", "how to switch"), the first page is
  one procedure: numbered steps, commands that paste, imperatives, the why in
  a few bullets and the pitfalls at the end. Test: can a reader follow it end
  to end without opening another tab?
- Mechanism and reference pages follow it and are linked from it, not the
  other way round. Do not split one procedure across pages.
- Give the reviewer the request verbatim and ask it to judge the page against
  it. In the report, map each goal to its page.

Related: [[project-green-check-says-nothing-about-content]],
[[global-stop-only-for-a-real-decision]].
