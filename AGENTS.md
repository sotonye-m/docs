# Documentation project instructions

## About this project

- Yativo's public developer docs, built on [Mintlify](https://mintlify.com) and published at docs.yativo.com
- Pages are MDX files with YAML frontmatter. Configuration, navigation and redirects live in `docs.json`
- Two products: **Yativo Fiat** (`yativo-fiat/`, `fiat-api-reference/`, `openapi-fiat.yaml`) and **Yativo Crypto** (`yativo-crypto/`, `api-reference/`, `guides/`, `sandbox/`, `sdks/`, `openapi-crypto.yaml`). Company pages and the changelog are in `yativo/`
- Fiat reference pages render from `openapi-fiat.yaml` through `openapi:` frontmatter, so request and response shapes belong in the spec
- `ai-knowledge-base/` is excluded from the site (`.mintignore`)

## Checks

Run both before committing. Both must pass:

```bash
npx -y mint@latest broken-links
npx -y mint@latest validate
```

- Add every new page to `docs.json` navigation
- When removing or renaming a page, add an entry to `redirects` in `docs.json`
- Add integrator-visible changes to `yativo/changelog.mdx` under the current month
- Don't escape code fences or backticks in MDX (`` \`\`\` `` breaks parsing)

## Terminology

- **API key**: the `X-Api-Key` + `X-Api-Secret` pair fiat servers send on every request. Use "an API key"
- **Legacy API keys**: the deprecated fiat Account ID + App Secret login (`POST /auth/login`)
- **IP whitelist**: the server IPs allowed to use a fiat API key. Link to `/yativo-fiat/ip-allowlist`
- **Dashboard**: app.yativo.com (fiat) or crypto.yativo.com (crypto). Write UI paths in bold with arrows: **Developers → API Keys**

## Style preferences

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references

## Content boundaries

This repository is public. Document only what an integrator can see and call.

- **No third-party providers.** Don't name the vendors, banks, processors or infrastructure behind a feature. Describe the capability instead ("identity verification", "the hosted verification page")
- **No internal systems.** No databases, queues, hosting, servers, IP addresses, internal service names, admin tooling or descriptions of internal processing
- **No security internals.** Don't describe enforcement switches, bypasses, risk-scoring weights, alerting, logging or past vulnerabilities. Document the errors and fields integrators receive
- **No dashboard-only flows as API docs.** Account registration, sign-in, session refresh, passkeys and two-factor setup happen in the dashboard
- **Crypto docs cover the crypto API only.** Don't document fiat features there (virtual accounts, IBANs, bank or cash withdrawals and payouts, or other features that only exist in the crypto app's UI). Point integrators to the Yativo Fiat API instead, for example `/yativo-fiat/virtual-accounts`
- Field names must match what the API returns, even when they aren't ideal. Don't add commentary around them
