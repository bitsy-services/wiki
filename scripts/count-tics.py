#!/usr/bin/env python3
"""Count the frames listed on /wiki/ai/verbal-tics/anthropic-claude in the wiki's prose.

A measurement, not a gate: it always exits 0 and is not run by check.sh. It is
the source of every `wiki:` figure on that page. Prose means the body of each
page with frontmatter, fenced code, inline code, tables, block quotations,
headings and everything from a Related / Sources / Further reading heading down
removed, so a page that quotes a frame is not charged for using it.

Two entries cannot be counted by pattern alone. C2 and C3 over-match, and the
page reports the number left after reading every match by hand. W4 and W10 are
reported with `--exclude overused-words`, the page that lists those words.

Usage:
  scripts/count-tics.py                       # the whole wiki
  scripts/count-tics.py DIR                   # another tree, e.g. a git archive
  scripts/count-tics.py --exclude SUBSTR ...  # skip paths containing SUBSTR
  scripts/count-tics.py --show ID             # print every match for one frame
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "wiki"

FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.S)
# Everything from the first reference-list heading to the end of the page. The
# heading must fill its line: "## Related parts" on the LLM pages is body text.
TAIL_RE = re.compile(
    r"^## (?:Sources|Further reading|Related|References|External links|External references"
    r"|Resources|Wiki pages)\s*$.*",
    re.S | re.M | re.I)
LIST_LINE_RE = re.compile(r"^\s*(?:[-*+]|\d+\.) .*$", re.M)
STRIP = [
    (re.compile(r"^```.*?^```", re.S | re.M), ""),      # fenced blocks
    (re.compile(r"`[^`\n]+`"), " "),                    # inline code
    (re.compile(r"^\s*>.*$", re.M), ""),                # block quotations
    (re.compile(r"^\s*\|.*$", re.M), ""),               # tables
    (re.compile(r"^#{1,6} .*$", re.M), ""),             # headings
    (re.compile(r"\{\{<.*?>\}\}", re.S), " "),          # shortcodes
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), " "),         # images
    (re.compile(r"\[([^\]]*)\]\([^)]*\)"), r"\1"),      # links -> their text
]
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SENTENCE_START = r"(?:^|(?<=[.!?] )|(?<=\n))"

# (ledger id, label, pattern). PAIR is counted by neg_pairs(); NOLIST patterns
# are counted on prose lines only, with list items removed first.
PAIR = None
NOLIST = "nolist:"
FRAMES = [
    ("W1", "genuinely", r"\bgenuinely\b"),
    ("W1", "honestly", r"\bhonestly\b"),
    ("W2", "actually", r"\bactually\b"),
    ("W3", "exactly / precisely, all senses", r"\b(?:exactly|precisely)\b"),
    ("W3", "  of which exact quantities (exactly one, zero, once, 4096)",
     r"\bexactly (?:one|zero|once|twice|two|three|four|five|six|half|\d)"),
    ("W4", "load-bearing", r"\bload-bearing\b"),
    ("W5", "quietly", r"\bquietly\b"),
    ("W5", "silently", r"\bsilently\b"),
    ("W6", "at all", r"\bat all\b"),
    ("W7", "worth <-ing|a|an|it|the>", r"\bworth (?:\w+ing|a|an|it|the)\b"),
    ("W8", "nothing", r"\b[Nn]othing\b"),
    ("W10", "sixteen general-list words",
     r"\b(?:delv(?:e|es|ed|ing)|tapestr(?:y|ies)|testament|multifaceted|intricate"
     r"|underscor(?:e|es|ed|ing)|pivotal|realm|foster(?:s|ed|ing)?|leverag(?:e|es|ed|ing)"
     r"|seamless(?:ly)?|robust|comprehensive|nuanced?|crucial(?:ly)?|landscape)\b"),
    ("C1", ", not Y tail",
     r",\s+not\s+(?:a|an|the|by|from|in|on|to|for|because|of|as|what|how|that|with)\b"),
    ("C1", "rather than", r"\brather than\b"),
    ("C2", "It is not X. It is Y. (over-matches)", PAIR),
    ("C3", "is the whole/entire X (over-matches)", r"\b(?:is|was|are) the (?:whole|entire) \w+\b"),
    ("C3", "the only", r"\bthe only\b"),
    ("C4", "which is why/what/where/how/exactly", r"\bwhich is (?:why|what|where|how|exactly)\b"),
    ("C4", "which is/was (the novels' pattern)", r"\bwhich (?:is|was)\b"),
    ("C6", "em dash, all", r"—"),
    ("C6", "em dash, outside list items", NOLIST + r"—"),
    ("S2", "list items containing an em dash", r"^\s*(?:[-*+]|\d+\.) [^\n]*—"),
    ("C8", "The catch/trick/point/... is that|to|not|what",
     r"\b[Tt]he (?:catch|trick|point|upshot|result|problem|fix|answer|lesson|difference"
     r"|consequence|reason|rule|cost|risk|question) is"
     r"(?: that| to|:| not| whether| what| how| why| simple)\b"),
    ("C9", "Two/Three/... things|caveats|reasons ...",
     r"\b(?:Two|Three|Four|Five) (?:\w+ ){0,2}(?:things|limits|points|reasons|facts"
     r"|consequences|caveats|ways|questions|rules|problems|details|properties|cases"
     r"|mechanisms|failures|costs)\b"),
    ("C11", "because", r"\bbecause\b"),
    ("C15", "short question, short answer", r"[A-Z][^.!?\n]{3,60}\?\s+[A-Z][^.!?\n]{1,40}\."),
    ("S1", "paragraph opening on a bolded phrase", r"^\*\*[^*\n]{3,80}\*\*"),
    ("F3", "not the same (thing) as", r"\bnot the same (?:thing )?as\b"),
]


def prose(path):
    """Return the countable prose of one page."""
    raw = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(raw)
    if m:
        raw = raw[m.end():]
    raw = TAIL_RE.sub("", raw)
    for pattern, replacement in STRIP:
        raw = pattern.sub(replacement, raw)
    return raw


def sentences(paragraph):
    flat = re.sub(r"\s+", " ", paragraph).strip()
    return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z*"“\[])', flat) if s.strip()]


def neg_pairs(text):
    """A negated sentence of at most 30 words followed by one opening It/That/They is|was."""
    negation = re.compile(
        r"\b(?:is|are|was|were|does|did|do|has|have|can|could|would|will)\s+not\b|\bnot\b")
    correction = re.compile(r"^(?:It|That|This|They|What)\s+(?:is|was|are|were)\b(?! not)")
    hits = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph or re.match(r"^(?:[-*+]|\d+\.) ", paragraph):
            continue
        ss = sentences(paragraph)
        for first, second in zip(ss, ss[1:]):
            if negation.search(first) and len(WORD_RE.findall(first)) <= 30 \
                    and correction.match(second):
                hits.append(f"{first} {second}")
    return hits


def main(argv):
    args = list(argv)
    show = args.pop(args.index("--show") + 1) if "--show" in args else None
    if "--show" in args:
        args.remove("--show")
    exclude = []
    if "--exclude" in args:
        i = args.index("--exclude")
        exclude, args = args[i + 1:], args[:i]
    root = Path(args[0]) if args else CONTENT

    pages = {
        p: prose(p) for p in sorted(root.rglob("*.md"))
        if p.name != "CLAUDE.md" and not any(e in str(p) for e in exclude)
    }
    words = sum(len(WORD_RE.findall(t)) for t in pages.values())
    print(f"{len(pages)} pages, {words:,} words of prose\n")
    print(f"{'id':5}{'frame':46}{'n':>6}{'/10k':>7}{'pages':>7}")

    for fid, label, spec in FRAMES:
        total, used_on, matches = 0, 0, []
        prose_only = spec is not PAIR and spec.startswith(NOLIST)
        pattern = spec[len(NOLIST):] if prose_only else spec
        for path, text in pages.items():
            if prose_only:
                text = LIST_LINE_RE.sub("", text)
            if pattern is PAIR:
                hits = neg_pairs(text)
            else:
                hits = [m.group(0) for m in re.finditer(pattern, text, re.M)]
            if hits:
                used_on += 1
                total += len(hits)
                if show == fid and pattern is PAIR:
                    matches += [f"  {path.relative_to(root)}: {h}" for h in hits]
                elif show == fid:
                    for m in re.finditer(pattern, text, re.M):
                        lo, hi = max(0, m.start() - 70), min(len(text), m.end() + 70)
                        context = re.sub(r"\s+", " ", text[lo:hi])
                        matches.append(f"  {path.relative_to(root)}: …{context}…")
        print(f"{fid:5}{label[:44]:46}{total:>6}{10000 * total / max(words, 1):>7.1f}{used_on:>7}")
        if matches:
            print("\n".join(matches))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
