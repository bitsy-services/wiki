# Wiki Workflow

## Default Intent

Treat the first message of a conversation as a request to create a new wiki page unless the intent is clearly something else (e.g. a question, bug report, or explicit edit request). Draft the page, choose a sensible path under `content/wiki/`, and set appropriate frontmatter.

## Show the opening before writing the body

For a new page or a substantial rewrite, write the first section and show it
before drafting the rest. It costs the user thirty seconds and it is the only
check that catches an unreadable opening: a subagent review, a green
`scripts/check.sh` and five measurement scripts all passed a page whose first
sentence did not parse, and three questions from the user found it immediately.

Expect those questions to be the page's spine — what is this made of, is it one
per X or shared, how many can there be, what happens at the limit — and answer
them in that order.

## Do not disable the review

`wiki-reviewer` reads the page in a fresh context, which is the point. Telling
it which rules to ignore removes the only reader who has not already been
convinced by the draft. If a rule genuinely no longer applies, change the rule
first and let the reviewer check against the new one.
