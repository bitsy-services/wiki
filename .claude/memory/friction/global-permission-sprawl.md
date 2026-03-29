---
name: permission-sprawl
description: User-level settings.json has 100+ one-off allow entries that could be consolidated with wildcards
type: feedback
---

The user's `~/.claude/settings.json` has accumulated many granular one-off permission entries. These create friction because each new variant of a command prompts again.

**Consolidation candidates:**

1. **git commands** — dozens of entries like `git mv:*`, `git add:*`, `git config:*`, `git submodule:*` plus project-level read-only git. Could consolidate to `Bash(git *)` at user level if the user is comfortable with that (note: this would allow `git push`, `git reset --hard`, etc. without prompting — may want to keep deny rules for destructive git ops).

2. **hugo** — `Bash(hugo version)`, `Bash(hugo --quiet)`, `Bash(/tmp/hugo)` → `Bash(hugo *)`

3. **npm/npx** — `Bash(npm install)`, `Bash(npm install:*)`, `Bash(npm run:*)`, `Bash(npm create:*)`, `Bash(npx tsc:*)`, `Bash(npx tailwindcss:*)`, `Bash(npx hugo)` → `Bash(npm *)` + `Bash(npx *)`

4. **curl** — many one-off curl commands for wikipedia, replicate, nytime5, wikimedia → `Bash(curl *)` (broad but the user seems comfortable with curl)

5. **pip3** — `Bash(pip3 install:*)`, `Bash(pip3 install --user Pillow)`, `Bash(pip3 install --break-system-packages Pillow)` → `Bash(pip3 *)`

6. **python3** — several one-off `python3 -c` entries → `Bash(python3 *)`

7. **forge** — already well-covered at project level with wildcards; user-level has some duplicates

8. **Dead entries** — many entries reference specific file paths or one-time operations that will never match again (e.g., specific curl URLs, specific file paths for `git mv`). These are clutter.

9. **WebFetch** — individual domain entries accumulate; user could consider allowing `WebFetch` broadly or not at all

**Why:** Each new command variant forces a permission prompt, breaking flow. The user's rules in always.md already define a clear policy for when to prompt vs. not — the permission config should reflect that policy.

**How to apply:** Suggest consolidation in batches. Keep deny rules for genuinely dangerous operations (forge script/create/verify, force push). Clean dead entries.
