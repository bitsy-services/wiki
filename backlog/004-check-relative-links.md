# 004 — Make the link check cover relative links

- **Priority:** P1 (the gate has a blind spot that already hides dead links)
- **Status:** open

## Problem

`scripts/check-content.py` skips every link whose target does not start with
`/`, with the comment `# relative links: not used in this wiki`. That comment is
no longer true. On 2026-09-16, fourteen pages under `content/` contained relative
links, found with:

```bash
grep -rlP "\]\((?!/|https?:|#|mailto:)[^)]+\)" --include=*.md content
```

Hugo renders each page as a directory (`/wiki/.../ticks/`), so a relative target
resolves against the page's own URL, not its parent folder. Some of the existing
links therefore 404 in production without the gate noticing. Two examples:

- `content/wiki/economics/defi/uniswap/ticks.md` links `(fee-distribution)`,
  which resolves to `/wiki/economics/defi/uniswap/ticks/fee-distribution`.
- `content/wiki/economics/defi/vanity-addresses.md` linked
  `(solidity/foundry-broadcast)` and `(ethereum)` the same way; both were rewritten
  as absolute links in the 2026-09-16 token-registration session, which is how the
  gap was found (by the `wiki-reviewer` subagent, not the gate).

## Proposed fix

1. Change the checker so a relative link is an error — `relative link; use an
   absolute /wiki/... path` — rather than resolving it. Every other link in the
   wiki is absolute, and `wiki-linking.md` already writes links that way.
2. Run `scripts/check.sh`, and rewrite each reported link as the absolute path it
   was meant to reach. Where the intended target is ambiguous, check the page's
   git history for the rename that broke it.
3. Hand-pick one known-bad case and confirm the check fails on it before calling
   the gap closed (per `patterns/project-green-check-says-nothing-about-content.md`).

## Files

- `scripts/check-content.py`
- the fourteen pages the grep above reports

## Verification

- `scripts/check.sh` is green.
- The grep above returns nothing.
- Temporarily adding `[x](ethereum)` to any page makes `scripts/check.sh` fail.
