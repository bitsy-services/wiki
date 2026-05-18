# 001 — Deterministic enforcement layer (hooks)

- **Priority:** P1 (highest leverage, smallest change)
- **Status:** open

## Problem

Every constraint in this repo is an advisory *rule* (probabilistic compliance).
There is no deterministic enforcement. In particular, verification is not
mandated: `hugo` is available and allowlisted, but nothing requires a build
after a content change, so a broken shortcode or malformed frontmatter can ship
— the exact trust-then-verify gap the Claude Code wiki page warns about.
Anthropic is explicit that hooks are for "actions that must happen every time
with zero exceptions," and the cost ladder puts hooks at zero context cost
(cheapest-context-first), so a few constraints belong below the rule layer.

## Proposed fix

Use the allowlisted `update-config` skill (settings.json/hooks are its domain).

1. **Build-verify hook.** Add a `Stop` hook (or `PostToolUse` scoped to
   Write/Edit under `content/`) that runs `hugo` and surfaces a non-zero
   exit / build error back into the turn.
2. **Write-guard hook.** Add a `PreToolUse` hook denying Write/Edit to paths
   outside the editable set (`content/`, `static/`, `layouts/`, `.claude/`,
   top-level config). Must deny writes to `themes/hugo-book` — CLAUDE.md says
   the submodule is do-not-edit; make that structural, not advisory.

Keep hook scripts (if any) under `.claude/hooks/` and the wiring in
`.claude/settings.json`.

## Files

- `.claude/settings.json` — `hooks` block
- `.claude/hooks/` — small scripts if the logic doesn't fit inline

## Verification

- Intentionally write bad YAML frontmatter to a page → build-verify hook fails
  the turn with the Hugo error.
- Attempt an Edit to a file under `themes/hugo-book/` → write-guard hook blocks
  it before the edit applies.
- A normal page edit under `content/` still succeeds and triggers a clean build.
