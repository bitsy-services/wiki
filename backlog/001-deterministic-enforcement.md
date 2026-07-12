# 001 — Deterministic enforcement layer (hooks)

- **Priority:** P1 (highest leverage, smallest change)
- **Status:** done (2026-07-12) — user approved the settings.json wiring

## What is already done (2026-07-12)

- `scripts/check-content.py` — internal links, `#anchors`, code-fence languages,
  frontmatter. Its slugifier is verified identical to Hugo's across all 142 pages.
- `scripts/check.sh` — build + content check. The definition of done.
- `.claude/hooks/verify.sh` — Stop hook. Blocks the turn while `check.sh` is red;
  honours `stop_hook_active` so it cannot loop.
- `.claude/hooks/guard-write.sh` — PreToolUse deny for `themes/`, `public/`,
  `resources/`, and `~/.claude/`.
- `.github/workflows/check.yml` — the same gate in CI, so it holds even with the
  hooks unwired.

Both hooks were exercised by piping their input JSON in directly: the write-guard
denies a `themes/` edit and permits a `content/` edit; the Stop hook stays silent
on a clean tree and blocks with actionable output on a planted broken link.

## The settings.json wiring (applied)

Worth recording *why* this step needed a human: it grants the agent's own scripts
auto-run permission and installs a hook that executes them. The auto-mode
classifier refused to let the agent do that to itself off the back of a general
"make yourself more autonomous" brief, which is the correct call — see
`.claude/memory/patterns/global-permission-and-config-hygiene.md`. The user
approved it explicitly.

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Edit|Write|NotebookEdit",
      "hooks": [
        { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard-write.sh", "args": [] }
      ]
    }
  ],
  "Stop": [
    {
      "hooks": [
        { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/verify.sh", "args": [], "timeout": 120,
          "statusMessage": "Verifying the site builds and content passes checks" }
      ]
    }
  ]
}
```

and add to `permissions.allow` so the gate never stalls on a prompt:

```json
"Bash(scripts/check.sh)",
"Bash(./scripts/check.sh)",
"Bash(python3 scripts/check-content.py *)"
```

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
