# Repository engineering guide

## Build · Test · Run

- Build: `npx wrangler deploy --dry-run --outdir /tmp/haunt-wrangler-build`
- Test: `node --input-type=module --check < src/worker.js`, then verify there are no unresolved launch placeholders with `rg -n "APP_STORE_URL_TBD|HAUNT_APP_ID_TBD" public src`
- Run: `python3 -m http.server 4747 -d public`, then open `http://127.0.0.1:4747/` and check desktop and mobile layouts
- Lint: none configured
- CI: push to `main` -> Cloudflare Workers builds and deploys the production site
- Done = build succeeds + tests are green + visual changes are run in a browser + focused commit pushed + production deployment verified.

## Project shape

- `public/` contains the static site assets.
- `src/worker.js` enforces the canonical host and serves the static-assets binding.
- `wrangler.toml` defines the Cloudflare Worker; do not add framework or package scaffolding unless the site genuinely needs it.
