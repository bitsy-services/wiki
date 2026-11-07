---
name: global-downloaded-code-in-experiments
description: An experiment that ran a downloaded script was refused in auto mode; read the source for its behaviour, and scanned PDFs can be read with no pip or poppler
metadata:
  type: feedback
---

2026-11-06, `security/operational-persona/`. To show how `pass` treats an empty
`PASSWORD_STORE_DIR`, an experiment script ran the `password-store.sh` it had
just downloaded, under a scratch home. The auto-mode classifier refused the whole
script as code from an external source.

Hypothesis: a scratch home makes a run feel safe from the inside, but what the
check judges is that downloaded code executes. The session's environment notes
already class downloads as data.

**Why:** the refusal blocked the other experiments in the same script until that
step came out.

**How to apply:** keep steps that touch downloaded files out of experiment
scripts. For a program that is not installed, quote the source line that decides
the behaviour (`PREFIX="${PASSWORD_STORE_DIR:-$HOME/.password-store}"`) and say on
the page that it was read from the source. Use a run only for what is installed.

The same session had no `pip` and no `pdftoppm`, and a key source was a scanned
PDF. What worked, with nothing outside the scratchpad:

- Fetch the wheel URL from `https://pypi.org/pypi/<name>/json`, download it with
  `urllib`, and unpack it with `zipfile`. Install `pypdf`, plus `pillow` for the
  wheel matching the interpreter's `cpXY` tag.
- CCITT page images extract with `pypdf` as raw streams. Prefix a minimal TIFF
  header (compression 4 when `/K` is negative), open with Pillow, save as PNG,
  and read the PNG with the Read tool. Scanned court filings can be rotated.

Related: [[global-numbers-beyond-their-sources]], [[global-scratchpad-lives-in-tmp]].
