---
name: global-mock-api-for-gh-commands
description: Copy-paste gh api commands can be run against a local mock of GitHub's REST API, with no token and no network, to check the exact requests they send
metadata:
  type: feedback
---

2026-10-30, `git/github/team-write-access`. The page gives organization owners
`gh api` commands that create a team and grant roles on a real organization,
which could not be run against a live org without an outward-facing change.
They were run instead against a local mock, and the mock's log showed the
method, path and JSON body of every request.

The mechanism: `gh` treats the host `github.localhost` as a local development
instance and sends its API requests over plain HTTP to
`http://api.github.localhost/`. With `GH_HOST=github.localhost`, a dummy
`GH_TOKEN`, an empty `GH_CONFIG_DIR`, and `HTTP_PROXY`/`HTTPS_PROXY` pointing at
a small Python `ThreadingHTTPServer` on 127.0.0.1 (refusing `CONNECT`, so no
HTTPS request can leave), every `gh api` call lands in the mock. Responses were
shaped from GitHub's OpenAPI description
(`github/rest-api-description`). `--paginate` follows the mock's `Link` headers.

It caught a real defect: with an empty `ROLE`, the undo command sent
`DELETE …/organization-roles/teams/<team>/`, one trailing slash from the
endpoint that removes every role the team holds; the page now uses
`${ROLE:?}`, and an interactive bash survives that guard (only the command is
aborted). It also confirmed a `while read` loop around `gh api` does not
swallow its own stdin.

**Why:** a request shape read from the docs feels as certain as one observed,
and empty-variable paths (`orgs//teams`, trailing slashes) only show up when
the command is run.

What the mock did not find, the first `wiki-reviewer` round did, by giving the
mock state the reader's organization might already have. A team named
`Developers` that already existed made the create fail with 422 while a
hand-typed `TEAM=developers` sent the members and the all-repository role to
the existing team; capturing the slug needed `TEAM=$(...) || TEAM=`, because
`gh api` prints a failed request's error body to stdout and `--jq` does not
filter it. And a mistyped username in the membership loop would have invited
whatever real account it matched; the loop now checks
`GET /orgs/{org}/members/{user}` first.

**How to apply:** for any page with `gh api` or `curl` commands against
GitHub, extract the page's own bash blocks and run them through the mock,
including empty and unset variables, a name that already exists, and an
identifier that names the wrong thing. Feed the snippet to `bash -i` so
`${VAR:?}` guards behave as they do in a reader's terminal. Say in the review
prompt and the report that this verifies requests, not GitHub's server-side
behaviour. Related: [[global-numbers-beyond-their-sources]].
