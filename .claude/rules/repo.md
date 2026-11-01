## Deploy

A push of `main` is a production deploy. Cloudflare Workers Builds builds the site as `wrangler.jsonc` says (`npx hugo`, then the static assets in `public/`) and serves it at wiki.bitsy.services; the same push runs `scripts/check.sh` in CI (`.github/workflows/check.yml`). Say so before pushing `main`.

## Gate

Run before every commit.

## Conflict stops

Every file: whenever the two sides assert different things, show both versions and ask.

## Branch names

`add-squashing-page`, `subdivide-defi`, `check-relative-links`
