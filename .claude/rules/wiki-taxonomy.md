---
description: The shape of the wiki's section tree, and how to decide where a new page or section goes
---

# Wiki Taxonomy

Where a page goes is decided before it is drafted, not after. `wiki-scope.md`
says *whether* a subject belongs in the wiki; this file says *where*, and what
the tree should look like as it grows.

Placement is the one decision that is expensive to revise. Hugo does not check
internal links, so a move is a link rewrite across every inbound page plus an
`aliases` entry on every moved file, and any URL already indexed by a search
engine survives only because someone remembered the alias.

## The current shape

Directly under `/wiki/`, in sidebar order:

| Section | Holds |
| --- | --- |
| `economics` | how value is created, priced, and moved — finance, DeFi, regulation, fraud |
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

**Every segment must narrow the subject.** `economics/finance/defi/options/call-option`
narrows five times and every word is doing work. A segment that only groups —
`.../pages/`, `.../topics/`, `.../other/` — is a segment to delete.

**Depth is a cost the reader pays**, in the breadcrumb and in every link that
has to spell the path out. Five segments after `/wiki/` is the practical ceiling
here. Past that, the subject usually wants a sibling section rather than a
deeper one.

**Every section index states its boundary.** The `_index.md` says what belongs
and — where a neighbouring section could plausibly claim the material — what
does not, and where that lives instead. `cs/_index.md` is the model:
*"Cryptographic theory lives here; the operational business of handling keys and
secrets on a real machine is in Security."* That sentence is what makes the next
placement decision mechanical instead of a re-argument.

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

Then add an alias to every moved file, so the old URL keeps resolving for
anything already linked or indexed:

```yaml
aliases: ["/wiki/<old>/<slug>/"]
```

Then update the parent `_index.md` files on both sides and run
`scripts/check.sh`. The link check is what catches the inbound references the
`sed` missed; the aliases are what the check cannot tell you about, because a
dead external link produces no error anywhere.

## Weights

`weight` orders siblings in the sidebar. Number in tens so a later arrival can
be slotted in without renumbering, and leave the existing numbers alone when
inserting — pick an unused multiple of ten between the neighbours instead.
