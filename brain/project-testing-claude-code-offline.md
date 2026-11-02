---
name: project-testing-claude-code-offline
description: How to verify a Claude Code config claim by running the real binary with nothing leaving the machine and the real ~/.claude untouched; the VS Code extension ships the binary
metadata:
  type: project
---

Pages in `ai/claude-accounts/` make claims about what Claude Code does with a
config. On 2026-10-30 every recipe on `switching.md` was checked this way, and
two documented-only behaviours (empty `CLAUDE_CONFIG_DIR`, and
`CLAUDE_CONFIG_DIR=~/.claude` not being the default) were re-confirmed on a
new version.

- **The binary.** No `claude` on `PATH` in the WSL clone, but the VS Code
  extension bundles one:
  `~/.vscode-server/extensions/anthropic.claude-code-<version>-linux-x64/resources/native-binary/claude`.
  Its `package.json` beside it gives each extension setting's `scope`.
- **Isolation.** Run under `env -i HOME=<scratch dir> PATH=/usr/bin:/bin`.
  That keeps the real `~/.claude` and `~/.claude.json` out of reach and drops
  the parent session's `CLAUDE*` variables.
- **No traffic.** Set `ANTHROPIC_BASE_URL` to a local capture server that
  saves each request and answers 400 (a script was kept at
  `tools/capture.py` in that session's scratchpad). The saved requests show
  the `x-api-key` sent, the loaded `CLAUDE.md` text and the skills listed,
  which proves an import or a symlink end to end. `claude auth status`
  (JSON: `configDirectory`, `authMethod`) needs no server at all.
- **Logins.** Stub `xdg-open`, `wslview` and the other browser launchers on
  `PATH` before running `claude auth login` on a pty, or it opens a browser on
  the user's Windows desktop.
- **Shell functions.** `timeout`, `xargs` and `env` run the binary, not a
  shell function named `claude`, so a function test must call it bare.
- **zsh** is not installed; `apt-get download zsh zsh-common` plus `dpkg -x`
  into the scratchpad gives a working `usr/bin/zsh` (run with `-f`). direnv
  comes the same way (`apt-get download direnv`).
- **Screens a reader sees.** A small Python `pty.fork()` driver that sends
  keystrokes on a timer and strips ANSI codes captures first-run onboarding
  (theme, then the login-method menu), the Console sign-in sub-menu, the
  status line and `/status`. Quote menu labels from that capture, not from
  memory.
- **Run the page, not a retyping of it.** Extract each fenced block from the
  Markdown and execute it verbatim in a fresh `HOME` (an interactive
  `bash --rcfile … -i` fed on stdin runs the direnv hook between commands).
  Re-run after every review fix that touches a block.
- **VS Code facts that need no editor.** Setting scopes are in the
  extension's `package.json`; a `machine` setting cannot be per workspace.
  In a remote window it comes from one file per machine,
  `~/.vscode-server/data/Machine/settings.json` (see `machineSettingsResource`
  in the server's `out/server-main.js`), so remote settings are not per
  profile.

Related: [[global-numbers-beyond-their-sources]], [[project-harness-invariants]].
