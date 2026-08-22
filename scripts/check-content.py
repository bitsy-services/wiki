#!/usr/bin/env python3
"""Verify wiki content against the rules in .claude/rules/.

Checks, in order of severity:

  link      internal link points at a page that does not exist
  anchor    internal link points at a heading that does not exist
  h1        body contains an `# H1` (Hugo Book renders frontmatter title as h1)
  fence     fenced code block has no language for syntax highlighting
  frontmatter  missing title, or non-integer weight
  acronym   an acronym is unregistered, or used on a page that never expands
            or links it (registry: scripts/acronyms.txt)

Exit status is 1 if any error is found, 0 otherwise, so this can be used as a
deterministic gate (see .claude/hooks/verify.sh).

Usage:
  scripts/check-content.py             # check everything
  scripts/check-content.py FILE...     # check only these files (links are still
                                       # resolved against the whole site)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# Markdown inline links: [text](target). Ignores image links (![...]) via lookbehind.
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(\s*([^)\s]+?)\s*(?:\"[^\"]*\")?\)")


ACRONYMS_FILE = ROOT / "scripts" / "acronyms.txt"
# A candidate acronym: an all-caps run of 2-6 chars containing at least two
# letters, with an optional lowercase plural suffix that is not part of the
# acronym ("AMMs" -> AMM, "DEXes" -> DEX). The two-letter floor skips version
# tags such as V3, L2 and Q64.
ACRONYM_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,5})(?:es|s)?\b")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_LABEL_RE = re.compile(r"(?<!!)\[([^\]]*)\]\([^)]*\)")


def load_acronyms():
    """Return {ACRONYM: expansion or None}. None means 'no expansion needed'."""
    reg = {}
    if not ACRONYMS_FILE.exists():
        return reg
    for raw in ACRONYMS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        acro, _, exp = line.partition("\t")
        exp = exp.strip()
        reg[acro.strip()] = None if exp in ("", "-") else exp
    return reg


def normalize(text):
    """Lowercase, fold -ise/-ize spelling, flatten non-alphanumerics to spaces.

    The spelling fold is applied to both sides of the comparison, so "decentralised
    oracle network" matches an expansion written the American way.
    """
    text = text.lower().replace("isation", "ization").replace("ise", "ize")
    return re.sub(r"[^a-z0-9]+", " ", text)


# How far apart the acronym and its spelled-out form may sit and still read as a
# definition. Wide enough for "Foo Bar (FB)" and for a parenthetical aside; too
# narrow for the expansion to be in a different paragraph.
BIND_WINDOW = 180


def binds(page_text, acro, expansion):
    """True if some use of `acro` sits next to its expansion.

    Requiring proximity is the whole point: a page that happens to contain the
    words somewhere and uses the acronym somewhere else has not defined it. The
    reader has to be able to see the two together.
    """
    want = normalize(expansion)
    for m in re.finditer(r"\b" + re.escape(acro) + r"(?:es|s)?\b", page_text):
        lo = max(0, m.start() - BIND_WINDOW)
        if want in normalize(page_text[lo : m.end() + BIND_WINDOW]):
            return True
    return False


def prose_lines(clean):
    """Yield (lineno, text) with inline code and link *targets* removed.

    Link labels are kept: `[AMM](/wiki/...)` still reads as the word AMM, which
    is what a reader sees, and what the 'is it linked?' test needs.
    """
    for lineno, line in clean:
        line = INLINE_CODE_RE.sub(" ", line)
        line = LINK_LABEL_RE.sub(lambda m: m.group(1), line)
        yield lineno, line


def split_frontmatter(text):
    """Return (frontmatter_lines, body_lines, body_offset)."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1 :], i + 2
    return [], lines, 1


def strip_code(body_lines, offset):
    """Yield (lineno, line) for lines outside fenced code blocks.

    Also yields fence-open events separately via the returned fences list.
    """
    out, fences = [], []
    fence = None  # (marker_char, length)
    for idx, line in enumerate(body_lines):
        lineno = offset + idx
        m = FENCE_RE.match(line)
        if m:
            marker, info = m.group(2), m.group(3).strip()
            if fence is None:
                fence = marker[0], len(marker)
                fences.append((lineno, info))
                continue
            if marker[0] == fence[0] and len(marker) >= fence[1] and not info:
                fence = None
                continue
        if fence is None:
            out.append((lineno, line))
    return out, fences


def slugify(text):
    """Approximate Hugo's default (github-style) auto heading IDs."""
    text = re.sub(r"`([^`]*)`", r"\1", text)  # inline code
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    text = re.sub(r"[*_~]", "", text)  # emphasis
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)  # punctuation
    # Each whitespace character becomes its own dash — Hugo does not collapse
    # runs, so "a — b" (em dash stripped) yields "a--b", not "a-b".
    text = re.sub(r"\s", "-", text)
    return text


def page_url(path):
    """Map a content file to the URL Hugo will serve it at (no trailing slash)."""
    rel = path.relative_to(CONTENT).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "_index":
        parts.pop()
    return "/" + "/".join(parts)


def main(argv):
    registry = load_acronyms()
    files = sorted(CONTENT.rglob("*.md"))
    files = [f for f in files if f.name != "CLAUDE.md"]

    pages = {}  # url -> {"anchors": set, "path": Path}
    parsed = {}

    for f in files:
        text = f.read_text(encoding="utf-8")
        fm, body, offset = split_frontmatter(text)
        clean, fences = strip_code(body, offset)

        anchors, seen = set(), {}
        for _, line in clean:
            m = HEADING_RE.match(line)
            if not m:
                continue
            slug = slugify(m.group(2))
            if not slug:
                continue
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            anchors.add(slug if n == 0 else f"{slug}-{n}")

        url = page_url(f)
        pages[url] = {"anchors": anchors, "path": f}
        parsed[f] = (fm, clean, fences)

    # Restrict reporting to the requested subset, but resolve links site-wide.
    if argv:
        targets = set()
        for a in argv:
            p = Path(a).resolve()
            if p in parsed:
                targets.add(p)
    else:
        targets = set(parsed)

    errors = []

    def err(kind, path, lineno, msg):
        errors.append((kind, path.relative_to(ROOT), lineno, msg))

    for f in sorted(targets):
        fm, clean, fences = parsed[f]

        fm_text = "\n".join(fm)
        if not re.search(r"^title:", fm_text, re.M):
            err("frontmatter", f, 1, "missing `title` in frontmatter")
        wm = re.search(r"^weight:\s*(.+)$", fm_text, re.M)
        if wm and not re.fullmatch(r"-?\d+", wm.group(1).strip()):
            err("frontmatter", f, 1, f"weight is not an integer: {wm.group(1).strip()}")

        for lineno, info in fences:
            if not info:
                err("fence", f, lineno, "fenced code block has no language")

        for lineno, line in clean:
            m = HEADING_RE.match(line)
            if m and len(m.group(1)) == 1:
                err("h1", f, lineno, "body H1 — Hugo Book already renders the title as h1")

            for target in LINK_RE.findall(line):
                if re.match(r"^(https?:|mailto:|tel:|data:|//)", target):
                    continue
                if target.startswith("#"):
                    anchor = target[1:].lower()
                    if anchor and anchor not in pages[page_url(f)]["anchors"]:
                        err("anchor", f, lineno, f"no such heading on this page: {target}")
                    continue
                if not target.startswith("/"):
                    continue  # relative links: not used in this wiki
                base, _, anchor = target.partition("#")
                base = "/" + base.strip("/")
                if base in ("/",):
                    continue
                # Static assets are served from static/ verbatim.
                if (ROOT / "static" / base.lstrip("/")).exists():
                    continue
                if base not in pages:
                    err("link", f, lineno, f"no such page: {target}")
                elif anchor and anchor.lower() not in pages[base]["anchors"]:
                    err("anchor", f, lineno, f"no such heading on {base}: #{anchor}")

        # --- acronyms ---------------------------------------------------
        # A page must, somewhere, either spell out each acronym it uses or
        # link it to the page that does. Registry entries with no expansion
        # ("-") are common knowledge and exempt.
        page_text = " ".join(t for _, t in prose_lines(clean))
        linked = set()
        for _, line in clean:
            for label in LINK_LABEL_RE.findall(line):
                linked.update(ACRONYM_RE.findall(label))

        first_use = {}
        for lineno, text in prose_lines(clean):
            for acro in ACRONYM_RE.findall(text):
                # Two letters minimum: skips version tags (V3, L2, Q64, D1).
                if sum(c.isalpha() for c in acro) < 2:
                    continue
                first_use.setdefault(acro, lineno)

        for acro, lineno in sorted(first_use.items(), key=lambda kv: kv[1]):
            if acro not in registry:
                err("acronym", f, lineno,
                    f"unregistered acronym {acro!r} — expand it here and add it "
                    f"to scripts/acronyms.txt")
                continue
            expansion = registry[acro]
            if expansion is None or acro in linked:
                continue
            if binds(page_text, acro, expansion):
                continue
            err("acronym", f, lineno,
                f"{acro!r} is never bound to its expansion on this page "
                f"(expected {expansion!r} beside a use of {acro})")

    order = {"link": 0, "anchor": 1, "acronym": 2, "h1": 3, "fence": 4, "frontmatter": 5}
    errors.sort(key=lambda e: (order[e[0]], str(e[1]), e[2]))

    for kind, path, lineno, msg in errors:
        print(f"{path}:{lineno}: {kind}: {msg}")

    if errors:
        counts = {}
        for kind, *_ in errors:
            counts[kind] = counts.get(kind, 0) + 1
        summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
        print(f"\n{len(errors)} problem(s): {summary}", file=sys.stderr)
        return 1

    print(f"content OK — {len(pages)} pages, no problems")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
