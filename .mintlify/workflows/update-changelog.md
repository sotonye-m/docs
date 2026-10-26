---
name: Update changelog
on:
  push:
    - repo: sotonye-m/docs
      branch: main
automerge: false
---

When a push to `main` changes what an integrator can call or rely on, add that change to `yativo/changelog.mdx`. If nothing on this push is worth a public changelog entry, do nothing and do not open a pull request.

## What is worth an entry

Add an entry only when an integrator must change their integration, or can newly do something they could not do before:

- A new, removed, or renamed endpoint, webhook, field, or required value
- A behavior change: status codes, limits, authentication, currencies, or which host to call
- A product capability that is now documented for integrators

Skip the push when the only changes are:

- Typos, rewording, heading edits, or nav order
- `ai-knowledge-base/`, `nav-records/`, `.mintlify/`, `.github/`, or this workflow
- A changelog bullet that already describes the same change
- Internal systems, vendors, databases, queues, hosting, or security enforcement

## How to write it

Read `AGENTS.md` and the current month's `<Update>` in `yativo/changelog.mdx`. Match that voice: second person, one sentence per bullet, a bold lead-in, and a link to the page that documents the change.

- Put the bullet under the current month. If that `<Update>` does not exist, add one at the top with `label` set to the month and year, for example `October 2026`.
- File Fiat changes under `### Yativo Fiat`, crypto changes under `### Yativo Crypto`, and docs-only corrections under `### Docs`.
- Do not name third-party providers, banks, or internal services.
- Do not edit older months.
- If an open pull request from this workflow already covers this push, add the bullet there instead of opening another pull request.
