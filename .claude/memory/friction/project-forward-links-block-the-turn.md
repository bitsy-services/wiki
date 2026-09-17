---
name: project-forward-links-block-the-turn
description: Linking to pages that are still waiting on research makes the Stop hook block the turn; create the target (or hold the link) before ending a turn
metadata:
  type: feedback
---

2026-09-16, token-registration per-site pages. Research for five sites was
still running in background agents, and pages already drafted linked to
`etherscan`, `coinmarketcap` and a `#the-token-property-schema` anchor that did
not exist yet. Ending the turn to wait for the agents tripped the Stop hook
(`scripts/check.sh` red: 2 dead links, 6 dead anchors), which forced
provisional drafts of five pages from older material — pages that were then
rewritten in full once the research arrived.

Hypothesis: when work is parallelised across background research, the natural
pause point ("wait for the notification") is also a turn end, and the gate
runs at every turn end, not just the last one. A forward link is a debt the
gate collects at the first pause.

**Why:** the provisional pages cost a full extra draft each, and their content
was briefly less accurate than what the section already said.

**How to apply:** before ending a turn that waits on background agents, run
`scripts/check.sh` yourself. Either write the link targets first (a real
section heading in the index, a short page with the facts already on hand) or
leave the link out until the target exists. Related:
[[project-green-check-says-nothing-about-content]],
[[global-name-the-blocker]].
