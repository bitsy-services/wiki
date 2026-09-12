# Model Builders — Writing Standard

These pages cover the organisations that train large language models, the
families they ship, and individual models worth a page of their own. They are
the *who* to the rest of the AI section's *how*: `llm/` takes a transformer
apart, `neural-network/` supplies the parts, and this section says who builds
them, what each lab actually discloses, and how the families are named.

Inherit the general rules from `../llm/CLAUDE.md`: no bare jargon, cite the
source, length follows the concept, one subject per page. The eight fixed
headings there are that section's format and do **not** apply here — a company
has no `Transforms` and no `Spec`. Apply the three output tests in
`.claude/rules/wiki-voice.md`, especially the first: after the opening
paragraph a reader can say what the lab is and what it ships.

Everything below is what differs, and the first rule is the one the section
exists to enforce.

## Quarantine what rots

Every other page in this wiki is about something that will be as true in five
years as it is today. These pages are not. A model page names a product that
will be superseded, repriced and eventually retired, and `scripts/check.sh`
cannot see any of that — a green check says the links resolve, not that the
facts hold.

So the material is split, deliberately, and the split is the format:

- **The body is durable.** How the family is tiered and named, what the lab
  discloses and what it withholds, which architectural choices it introduced or
  popularised, who owns it and where its compute comes from, what it has been
  criticised for. This is still true after the next release.
- **One `## Status` section holds everything that rots**, opens with the date
  it was checked, and links the vendor's own page as the live source.

```markdown
## Status

Anthropic's current flagship as of 11 September 2026. The
[model overview](https://docs.claude.com/en/docs/about-claude/models) is the
live source for pricing, context limits and retirement dates.
```

A reader who finds the `Status` section stale has lost one paragraph. A reader
who finds stale figures woven through six paragraphs cannot tell which of the
rest to trust, and that is the failure this rule prevents.

### What never goes in a page at all

- **Price tables.** `wiki-content.md` already decides this for deployed
  addresses: complete and copy-pasteable, or a link to the canonical source.
  Prices change without an announcement, so the link wins. Naming a price in
  prose is fine where it carries an argument — *cache reads cost a tenth of
  fresh input tokens, which is why agentic loops are affordable at all* — and
  the argument survives the exact figure moving.
- **Benchmark scores and leaderboard rankings.** They rot fastest, they are
  gamed, several labs have been caught presenting them selectively, and the
  wiki cannot reproduce any of them. Say what a model is *for* and what it is
  measurably good at in kind, not where it sat on a leaderboard in September.
- **"The best model for X."** The ranking changes monthly. The trade-off that
  produces the ranking — open weights against hosted quality, latency against
  reasoning depth, context length against cost — does not, so write that.

## Say what is disclosed, and say who disclosed it

The eight labs differ enormously in what they publish, and that difference is
one of the most interesting durable facts about them. Meta, DeepSeek, Alibaba
and Mistral publish parameter counts, training-token counts and architecture.
Anthropic, OpenAI and Google publish far less; xAI published everything for one
generation and then stopped.

- **Never state a parameter count, training-set size or architecture for a
  closed model.** The widely-repeated figures for the closed frontier models
  come from leaks, one microphone slip and a great deal of confident
  repetition. Write *"Anthropic has not published parameter counts for any
  Claude model"* — the absence is a fact, and it is a more useful one than a
  laundered rumour.
- **Attribute what the lab claims as a claim.** A training cost, a context
  window and a safety property are things a vendor asserts. *DeepSeek reports a
  training cost of $5.576M for the final V3 run, and says explicitly that the
  figure excludes prior research, ablations and the cost of the cluster* is
  checkable. *DeepSeek trained V3 for $5.576M* is not, and that particular
  number was misreported worldwide precisely because the exclusions were
  dropped.
- **Prefer the primary source.** A vendor's docs, model card, system card or
  paper. The sites that rank for "best LLM 2026" are content farms, several of
  them model-written, and at least one invented a model that does not exist.
  Using one as a citation puts an invented fact in the wiki under this repo's
  name.

## Report criticism, in the same register as everything else

Several of these labs have documented controversies: benchmark presentation,
model outputs that caused real harm, licence terms that are not what the
marketing says, environmental and labour questions around datacentres. A page
that omits them is not neutral, it is a brochure.

Cover them the way `wiki-voice.md` covers anything else — the specific fact,
dated and sourced, and let the reader appraise it. *In July 2025 Grok produced
antisemitic output including praise for Hitler; xAI attributed it to a system
prompt change and removed the posts* is a wiki sentence. *Grok is dangerously
unfiltered* is not, and neither is silence.

The same discipline applies in the other direction. A lab's own framing of
itself — safety-first, open, sovereign, efficient — is a positioning claim.
Report that the lab makes it, and then report what it does, which is usually
the more interesting half.

## Page shapes

**A builder page** (`<builder>/_index.md`) is the family charter as well as the
company page, because most of these labs ship one family. Cover, in this order:
what the lab is and what it ships; the company — who founded and owns it, where
the money and the compute come from; how the family is tiered and named; what
the lab discloses; what is architecturally distinctive about its models;
criticism where it is documented; then `## Status` with the current lineup, then
`## Sources`.

Where a builder genuinely ships two separate families — Google's closed Gemini
and open-weight Gemma — the second gets its own page at the builder level rather
than a folder. A folder is only worth it when a third page needs one, per
`wiki-taxonomy.md`.

**A model page** covers one named model and exists only where there is something
durable to say about it beyond a row in a table — an architecture that was new,
a training method that was new, a release that changed the market. Most models
do not clear that bar and belong in the builder page's lineup table instead.
**Do not create a page per model per generation.** That is a changelog, and the
vendor already publishes one.

## Naming and versioning is the load-bearing content

The thing a reader most often arrives needing is *what do these names mean* —
why Opus and Sonnet and Haiku, why `gpt-5.6` and `o3` coexisted, why Llama 4
Scout and Maverick are the same generation at different sizes, why `8x7B` is
46.7 billion parameters and not 56. Naming schemes are durable, they are
genuinely confusing, and no vendor explains a competitor's. Give them real
space.

## Linking

Link into `llm/` for every mechanism a model page names — mixture of experts,
grouped-query attention, RoPE, the KV cache, RLHF, context length. Those pages
explain the machinery; these pages say who shipped it first and what they
changed. Do not re-teach a mechanism here: one paragraph of gloss so the
sentence parses, then the link.

Links between builder pages are expected and cheap. The interesting facts in
this section are comparative — Mistral's founders wrote the Llama papers,
DeepSeek's distilled models are built on Qwen and Llama bases, Anthropic's
founders left OpenAI — and each of those is a link in both directions.
