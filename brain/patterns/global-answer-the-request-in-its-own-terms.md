---
name: global-answer-the-request-in-its-own-terms
description: One page per question the reader brings, titled in their words, answer in the first paragraph, one recommended way; a "how" page is a procedure followable top to bottom, and reference nobody asked for is cut, not kept behind it
metadata:
  type: feedback
---

Consolidates three observations on the same section, `ai/claude-accounts/`.

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
- **2026-11-01.** "This whole section illustrates every crappy practive of
  every poorly written technical garbage ever written. It is information
  vomit. No knowledge and certainly no wisdom." The user named three
  questions with different lifecycles (which accounts: decided once;
  mapping an account to a directory: set up once; switching: daily) and
  asked for one simple page each, with how to switch in the first
  paragraph. The October fix had kept six reference pages behind a
  266-line procedure page that still carried a file table, tested-in
  provenance, three mapping mechanisms and a status-line script. The
  rebuild deleted the reference pages (aliases keep their URLs), wrote one
  page per question with the answer as its first paragraph, and picked
  one mechanism per job (an alias to switch, direnv to map) instead of
  offering several. The old pages had also gone stale within six days:
  Anthropic renamed Max 20x to Ultra and changed its limits.

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
- One page per question the reader brings, sized to how often they bring
  it. The first paragraph is the answer (the command, or the decision),
  not a definition of the mechanism behind it.
- Wisdom is choosing for the reader: recommend one way and say when it
  does not apply, rather than laying out every way. A fact earns a place
  only if the reader acts on it; test provenance ("tested in Bash 5.3")
  belongs in the commit message, not the page.
- Keep volatile figures (prices, plan limits) to the few the decision
  needs. Every extra one is a sentence that goes stale.
- Give the reviewer the request verbatim and ask it to judge the page against
  it. In the report, map each goal to its page.

Related: [[project-green-check-says-nothing-about-content]],
`.claude/rules/kit/collaboration.md`.
