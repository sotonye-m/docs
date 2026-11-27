# Navigation and endpoint changes

A record of menus, pages and endpoints that were hidden, removed or renamed on purpose.

**Don't bring any of these back** (in `docs.json`, `openapi-fiat.yaml` or the guides) unless the docs owner explicitly asks for that item to return. This applies even when the endpoint still exists in the API, or when another source (the backend's `api-guide/`, an old commit, a generator) still describes it.

`nav-records/` is excluded from the site in `.mintignore`. The exact removed `docs.json` blocks are in [`disabled-nav.json`](disabled-nav.json), so a hidden menu can be restored as it was.

## Removed navbar / anchors

| Date | Item | Why |
|---|---|---|
| 2026-10-26 | Navbar **Get Started — Crypto** | Crypto dashboard URL removed from public docs |
| 2026-10-26 | Global anchor **Crypto Dashboard** | Crypto dashboard URL removed from public docs |

## Hidden from the menu (pages kept)

The page files still exist and are still reachable by URL. Only the menu entry is gone.

| Date | Menu | What's hidden | Why |
|---|---|---|---|
| 2026-11-06 | Platform guides → Authentication | `yativo-platform/authentication` (Team API Keys integration guide from `api-guide/team-api-keys-integration.md`) | Duplicate of Fiat auth docs; do not re-sync or republish unless the docs owner asks. Redirect `/yativo-platform/authentication` → `/yativo-fiat/authentication` |
| 2026-11-06 | API Reference → Compliance RFIs | `POST /business/rfis/{id}/realtime/auth`, `fiat-api-reference/rfis/realtime-auth` | Admin workspace only; not for integrators. Redirect `/fiat-api-reference/rfis/realtime-auth` → `/yativo-fiat/rfis` |
| 2026-10-21 | Yativo Crypto tab | The whole tab | Unpublished 2026-11-16. Do not restore |
| 2026-10-21 | Crypto API References tab | The whole tab | Unpublished 2026-11-16. Do not restore |
| 2026-10-21 | API Reference → Beneficiaries | Create, List, Get, Update, Delete, Archive and Unarchive Beneficiary (`fiat-api-reference/beneficiaries/{create,list,get,update,delete,archive,unarchive}`) | Beneficiaries are now just saved payment methods. Nothing links a payment method to a separate beneficiary record |
| 2026-10-21 | API Reference → Wallets | Create Wallet (`fiat-api-reference/wallets/create`) | Not offered to integrators |

## Removed (page, spec entry and guide sections deleted, redirect added)

| Date | Item | Endpoint | Redirect |
|---|---|---|---|
| 2026-10-21 | API Request Logs | `GET /business/logs/all`. Also removed the request-log sections from `yativo-fiat/developer.mdx` and `yativo-fiat/webhooks.mdx` | `/fiat-api-reference/developer/logs` → `/fiat-api-reference/developer/events` |
| 2026-10-21 | Provision Funding Address | `POST /corporate-card/wallet`. `GET /corporate-card/wallet` creates the address on first call | `…/corporate-cards/wallet-provision` → `…/corporate-cards/wallet-get` |
| 2026-10-21 | Get Employee KYC | `GET /corporate-card/employees/{employee_id}/kyc`. Integrators can submit employee KYC but not read it back. The `kyc` object on Get Employee and the full KYC record in the Submit Employee KYC response aren't documented either | `…/corporate-cards/kyc-get` → `…/corporate-cards/employees-get` |
| 2026-10-21 | Login History | `GET /auth/login-history` and the "Account Security" tag. Removed the "Review sign-in activity" section of `yativo-fiat/security.mdx` and the changelog entry | `/fiat-api-reference/security/login-history` → `/yativo-fiat/security` |
| 2026-10-21 | Batch Payout | `POST /payout/batch`. Removed the Batch Payout section and `/batch` mentions from `yativo-fiat/payouts.mdx` | `/fiat-api-reference/payouts/batch` → `/fiat-api-reference/payouts/simple` |
| 2026-10-26 | Send Money | `POST /sendmoney`. Removed the Send Money guide and send-money sections from exchange rates, regional payouts and related pages | `/yativo-fiat/send-money` → `/yativo-fiat/payouts`, `/fiat-api-reference/payments/send-money` → `/fiat-api-reference/payments/payout` |
| 2026-10-26 | Get Send Money Quote | `POST /sendmoney/quote` | `/fiat-api-reference/payments/send-money-quote` → `/fiat-api-reference/payments/exchange-rate` |
| 2026-10-26 | Add Transfer Purpose | `POST /sendmoney/purpose` | `/fiat-api-reference/payments/send-money-purpose` → `/fiat-api-reference/payments/payout` |
| 2026-10-26 | Activate Customer for Virtual Cards | `POST /customer/virtual/cards/activate`. Issue a card with `POST /customer/virtual/cards/create` | `/fiat-api-reference/virtual-cards/activate` → `/fiat-api-reference/virtual-cards/create` |
| 2026-11-09 | Create withdrawal link | `POST /card-checkout/customers/{customer_id}/withdrawal`. Integrators save payout details with `POST /card-checkout/customers/{id}/payout-methods` | `/fiat-api-reference/card-checkout/customers-withdrawal` → `/fiat-api-reference/card-checkout/payout-methods-create` |
| 2026-11-16 | Yativo Crypto docs | Unpublished `yativo-crypto/`, `api-reference/`, `sandbox/`, `sdks/`, `extensions/`, `openapi-crypto.yaml`, and the crypto `guides/` pages (the crypto dashboard was crypto.yativo.com). Files kept on disk and excluded in `.mintignore`. Do not restore | `/yativo-crypto/:slug*` → `/yativo-fiat/introduction`, `/api-reference/:slug*` → `/yativo-fiat/introduction`, `/sandbox/:slug*` → `/yativo-fiat/sandbox`, `/sdks/:slug*` → `/yativo-fiat/sdks/overview`, `/extensions/:slug*` → `/yativo/introduction` |
| 2026-11-18 | Plans and billing (`yativo-fiat/plans`, `yativo-platform/business/subscriptions`) | `/business/subscription*`, `/business/billing/*`, and `/business/plans/*`. Plans, subscriptions, and billing are managed in the dashboard UI (**Settings → Billing**) only, not via API. Removed the **Products** group, **Business → Plans & Subscriptions**, fee-page links, and changelog API bullets | `/yativo-fiat/plans` → `/yativo-fiat/fees`, `/yativo/subscriptions` → `/yativo-fiat/fees`, `/yativo-platform/business/subscriptions` → `/yativo-platform/money-movement/fees` |
| 2026-11-27 | Upload File | `POST /storage/upload`. KYC file fields accept base64 data URIs or file URLs directly; do not expose a separate upload option | `/fiat-api-reference/kyc/upload` → `/yativo-fiat/kyc#upload-documents` |

## Renamed

| Date | Old | New |
|---|---|---|
| 2026-11-27 | Navigation tabs: branded product names | `Guides`, `API Reference`, `Company` |
| 2026-10-21 | Fund or Withdraw Card Balance (`corporate-cards/balance-update`) | Fund Employee (`corporate-cards/employees-fund`) |
| 2026-10-21 | Get Card Balance (`corporate-cards/balance-get`) | Get Employee Balance (`corporate-cards/employees-balance`) |
| 2026-10-21 | Add / List / Get / Update / Delete Payment Method (`beneficiaries/payment-methods-*`) | Add Beneficiary, List Beneficiaries, Get Beneficiary, Update Beneficiary, Delete Beneficiary. Same pages and endpoints (`/beneficiaries/payment-methods…`). In the guides, saving a payment method is "adding a beneficiary", and `beneficiary_id` isn't used |

Wording rule for corporate cards: the employee is the cardholder. Cards are denominated in, and spend from, the employee's balance. Say "employee's balance", not "card balance".

## Regrouped

| Date | Menu | New layout |
|---|---|---|
| 2026-10-21 | API Reference → Corporate Cards | Subgroups: Funding, Employees, Employee Balance, Cards, Memos, Locations |
| 2026-10-21 | API Reference → KYC / KYB | Subgroups: Individual, Business, Shared |
| 2026-10-21 | API Reference → KYC Lookups | Subgroups: Individual, Business, Shared |

## Adding to this record

When you hide, remove or rename a menu item, add a row here, and add the removed `docs.json` block to `disabled-nav.json`.
