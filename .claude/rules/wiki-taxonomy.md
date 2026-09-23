---
description: The shape of the wiki's section tree, and how to decide where a new page or section goes
---

# Wiki Taxonomy

Where a page goes is decided before it is drafted, not after. `wiki-scope.md`
says *whether* a subject belongs in the wiki; this file says *where*, and what
the tree should look like as it grows.

Placement is the one decision that is expensive to revise. Hugo does not check
internal links, so a move is a link rewrite across every inbound page plus a
redirect for every moved URL, and any URL already indexed by a search engine
survives only because someone remembered the redirect.

## The current shape

Directly under `/wiki/`, in sidebar order:

| Section | Holds |
| --- | --- |
| `economics` | how value is created, priced, and moved — DeFi, payments, regulation, fraud |
| `ai` | getting work out of coding agents, and taking the models apart |
| `security` | handling keys, secrets, and credentials on a developer machine |
| `social` | building and moderating communities on social platforms |
| `cs` | the durable ideas underneath the rest — theory, not tools |
| `git` | an opinionated version-control workflow |
| `web` | publishing and serving documents: building a site, and getting it to a browser |
| `microsoft` | programming against Microsoft's platforms |

Each section's `_index.md` is the authority on what belongs in it. This table is
an index to those charters, not a substitute for reading the one you are about
to add to.

**`git` and `microsoft` are grandfathered, not precedent.** One is a single tool
at the top level and the other is a vendor; both predate these rules. Do not
reason "Git is top-level, so my tool can be" — that inference put the Hugo
section at `/wiki/hugo` and it had to be moved to `/wiki/web/hugo`.

## The shape of a good taxonomy

**A node is a subject, not a container.** Sections are named for what their
pages are about. *Tools*, *Guides*, *Reference*, *Notes*, *Misc* name the form
of the material and predict nothing about its contents. The test is whether a
reader seeing the name in the sidebar can say what is inside before clicking.

**The top level is for fields, not for named things.** A product, library,
protocol, or company belongs inside the field that explains what it is for:
`web/hugo`, not `hugo`. The test is whether a second, unrelated thing of the
same kind could plausibly join it as a sibling. *Hugo* has no siblings. *Web*
has many — hosting, HTTP caching, DNS, browser APIs.

**Siblings are the same kind of thing.** Under one `_index.md`, children should
be comparable in grain: all mechanisms, or all products, or all subdomains, not
one of each. Mixed siblings usually mean the parent is really two parents.

**Every segment must narrow the subject.** `economics/defi/options/call-option`
narrows four times and every word is doing work. A segment that only groups —
`.../pages/`, `.../topics/`, `.../other/` — is a segment to delete.

**Depth is a cost the reader pays**, in the breadcrumb and in every link that
has to spell the path out. Five segments after `/wiki/` is the practical ceiling
here. Past that, the subject usually wants a sibling section rather than a
deeper one. A section placed *at* the ceiling can never subdivide, so a section
that may still grow is kept a segment short of it.

**Breadth is a cost too, paid by a different reader.** A reader who knows a
page's name can bisect an alphabetical list, so its length barely matters. A
reader who knows the *concept* but not the name — anyone arriving from a search
engine — reads a categorical list label by label, and attention drops off
sharply after the first few entries. The menu research finds categorical
grouping beats alphabetical for exactly that reader (McDonald, Stone & Liebelt
1983). The working ceiling is **about fifteen siblings**; past it, subdivide
(see *Subdividing a section* below). The number is a judgment, not a
measurement: fifteen is as broad as the depth-versus-breadth studies tested
(Landauer & Nachbar 1985), and it is roughly what one expanded section can show
on a laptop screen beneath the sections above it. DeFi reached fifty-six.

**Every section index states its boundary.** The `_index.md` says what belongs
and — where a neighbouring section could plausibly claim the material — what
does not, and where that lives instead. `cs/_index.md` is the model:
*"Cryptographic theory lives here; the operational business of handling keys and
secrets on a real machine is in Security."* That sentence is what makes the next
placement decision mechanical instead of a re-argument.

**Every section index is a page, not a folder.** The theme renders a section
whose `_index.md` has no body as a label that cannot be clicked. With a body,
it is the page a reader who arrived from a search engine clicks up to from the
breadcrumb, so it carries a definition of the subject and a prose map of the
children in reading order — what each is and why it comes next.
`economics/defi/_index.md` is the model. When a section is subdivided, its map
paragraphs are the drafts of the new sections' indexes.

**A subject with two plausible parents goes under the charter that names it, and
is linked from the other.** Never duplicate a page to satisfy both.
`cs/ipfs/_index.md` does this out loud: it sits under Computer Science rather
than DeFi *because the durable idea is the addressing scheme, not the storage
market built on it*.

## When to create a level

The two altitudes have opposite defaults, because the cost of being wrong runs
in opposite directions.

**A domain section — directly under `/wiki/` — is created as soon as the first
subject needs it.** A thin parent is cheap; a subject parked one level too high
is a move later. `web/` was created to hold one subsection, and that is correct.

**A subject section — anything below that — is created when the third page needs
it.** Do not make a folder for one page. A page becomes a section when three
pages want to sit together, or when one page passes roughly 1,500 words and
splits cleanly along mechanism lines. `cs/ipfs.md` was a single page until it
earned `cs/ipfs/`, which now has `pinning/` beneath it.

**When a section's natural name is already one of its pages, that page becomes
the index.** That is what happened to `cs/ipfs.md`: Hugo serves `foo.md` and
`foo/_index.md` at the same URL, and `scripts/check-content.py` resolves them
the same way, so the promotion rewrites no links and needs no redirect. The
page's definition stays at the top; the map of the children goes beneath it.

## Deciding, in practice

1. Name the subject in one phrase, then find the section whose `_index.md`
   charter covers that phrase. Read the charter — not the section title.
2. If exactly one fits, place it there and link out from the neighbours that
   nearly fit.
3. If two fit, pick the one whose charter names the subject, and say in the page
   why it is there rather than the other.
4. If none fits, the subject needs a new domain section. Propose it before
   writing: the name, the one-sentence charter, its boundary with the two
   nearest existing sections, and the weight. A new top-level section changes
   the shape of the wiki, so it is worth a sentence of confirmation rather than
   a surprise in a diff.
5. State the chosen path and the reason before drafting. Placement reasoning is
   cheap to correct in a sentence and expensive to correct in a move.

## Moving something that is already placed wrongly

```bash
git mv content/wiki/<old> content/wiki/<new>
grep -rl "/wiki/<old>" content/ --include=*.md | xargs sed -i 's|/wiki/<old>|/wiki/<new>|g'
```

Then keep the old URL resolving for anything already linked or indexed. A
single page gets an alias in its frontmatter:

```yaml
aliases: ["/wiki/<old>/<slug>/"]
```

A whole section that moved gets one splat pair in `static/_redirects` instead —
a real 301 rather than a meta-refresh stub, and one line for the subtree rather
than an alias on every file. First match wins, so the deepest rewrite is listed
first:

```text
/wiki/<old>   /wiki/<new>/        301
/wiki/<old>/* /wiki/<new>/:splat  301
```

Then update the parent `_index.md` files on both sides and run
`scripts/check.sh`. The link check is what catches the inbound references the
`sed` missed; the redirects are what the check cannot tell you about, because a
dead external link produces no error anywhere.

## Subdividing a section that has outgrown its list

The trigger is the sibling ceiling: a section whose expanded list passes about
fifteen entries. The operation is one new level, never two, and it is done
once. Readers who have visited a few times find a page by remembered position,
and after moderate practice that beats any rule-based order (Somberg 1987);
every restructure spends it. Land the whole subdivision in one commit rather
than moving a few pages at a time.

1. **Groups are subjects, named so the sidebar predicts the contents.** The
   `##` headings of the section's own index are the first draft. Strike any
   that names a form — *Foundations*, *Tooling*, *Other* — and find the subject
   underneath it. Each group holds between three and about fifteen pages.
2. **Named things go into the field that explains them.** A chain, a protocol
   or a product that already has a section of its own nests under the group
   for its kind — `chains/ethereum/`, `oracles/chainlink/` — so the reader
   looking for "the oracle one" finds it beside the oracle mechanism pages.
3. **Large subject sections stay where they are.** A section at the grain of
   the new groups — a subdomain, not a named thing — with fifteen or more pages
   of its own is already what the subdivision is producing. It stays a sibling
   of the new groups: nesting it spends its readers' remembered position and,
   at the depth ceiling, forecloses subdividing it in turn.
4. **Keep the reading order.** Within each group the pages keep the relative
   order they had; the numbers change, the sequence does not. Number the groups
   in the order the section's index already presents them.
5. **Rewrite the inbound links first, then add the redirects**, as above, and
   run `scripts/check.sh`. The order matters: a rewrite that runs after the
   aliases are written rewrites the aliases too, and an alias pointing at the
   page's own new URL generates nothing. Check the build output for the stub
   at one old URL before calling the move done.

## Weights

`weight` orders siblings in the sidebar. Number in tens so a later arrival can
be slotted in without renumbering, and leave the existing numbers alone when
inserting — pick an unused multiple of ten between the neighbours instead.

The order is **reading order**: the first page is the one a reader with no
background needs first, and each page follows the ones it assumes. Not
alphabetical — the reader who knows the name has search, and the one who knows
only the concept cannot use the alphabet — and not by importance. The first
slot is the one readers actually look at, so it goes to the entry point, not
the most-visited page. This is the simple-to-complex sequence of instructional
design (Reigeluth's elaboration theory); it is well-motivated and thinly
measured, so treat it as the default rather than a finding.

Weights are never renumbered for tidiness. Returning readers find a page by
where it sits, and a reorder costs every one of them that knowledge and buys
nothing. Two siblings sharing a weight is a defect — Hugo breaks the tie by
title, an order nobody chose — and the fix is to move the later arrival to an
unused number, not to resequence the run.

## Sources

The sibling ceiling, the ordering rule and the no-renumbering rule rest on
three menu-search studies, all of which measure time to find a known target
rather than anything about learning: McDonald, Stone & Liebelt, *Searching for
Items in Menus* (1983); Landauer & Nachbar, *Selection from Alphabetic and
Numeric Menu Trees* (1985); Somberg, *A Comparison of Rule-Based and
Positionally Constant Arrangements of Computer Menu Items* (1987). Nothing in
that literature covers sequencing pages for a reader who is learning; the
reading-order rule borrows that from instructional design instead.
