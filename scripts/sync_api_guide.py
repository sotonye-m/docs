#!/usr/bin/env python3
"""Sync Yativo-gcloud/api-guide/*.md into Mintlify yativo-platform/*.mdx."""

from __future__ import annotations

import re
from pathlib import Path

GUIDE = Path("/home/ignite/Documents/Yativo/Yativo-gcloud/api-guide")
DOCS = Path("/home/ignite/Documents/Yativo/docs/yativo-platform")

MAPPING: dict[str, str | None] = {
    "account-recovery.md": "business/account-recovery.mdx",
    "affiliate-api-integration.md": "business/affiliate-program.mdx",
    "api-responses-and-errors.md": "api-responses-and-errors.mdx",
    "card-checkout.md": "cards-and-accounts/card-checkout.mdx",
    "corporate-card-integration.md": "cards-and-accounts/corporate-cards.mdx",
    "employee-portal-integration.md": "business/employee-portal.mdx",
    "exchange-rates.md": "money-movement/exchange-rates.mdx",
    "fees.md": "money-movement/fees.mdx",
    "ip-whitelisting.md": "security/ip-whitelisting.mdx",
    "login-history.md": "security/login-history.mdx",
    "mcp-server.md": "testing/mcp-server.mdx",
    "onramp.md": "money-movement/onramp.mdx",
    "passkey-login-integration.md": "security/passkey-authentication.mdx",
    "payin-payout-integration.md": "money-movement/payins.mdx",
    "payout-receive-amount.md": "money-movement/payout-receive-amount.mdx",
    "revenue-split-api-integration.md": "business/revenue-split.mdx",
    "sandbox-testing.md": "testing/sandbox-testing.mdx",
    "SECURITY.md": "security/security-policy.mdx",
    "subscriptions.md": "business/subscriptions.mdx",
    "team-api-keys-integration.md": "authentication.mdx",
    "virtual-card-integration.md": "cards-and-accounts/virtual-cards.mdx",
    "wallet-swap-integration.md": "money-movement/wallet-swaps.mdx",
    "webhook-guide.md": "webhooks/overview.mdx",
    "webhook-resend-ui.md": "webhooks/resend.mdx",
    "TEAM_FUNCTIONALITY.md": "security/team-management.mdx",
}

LINK_MAP = {
    "team-api-keys-integration.md": "/yativo-platform/authentication",
    "TEAM_FUNCTIONALITY.md": "/yativo-platform/security/team-management",
    "ip-whitelisting.md": "/yativo-platform/security/ip-whitelisting",
    "passkey-login-integration.md": "/yativo-platform/security/passkey-authentication",
    "account-recovery.md": "/yativo-platform/business/account-recovery",
    "mcp-server.md": "/yativo-platform/testing/mcp-server",
    "payin-payout-integration.md": "/yativo-platform/money-movement/payins",
    "payout-receive-amount.md": "/yativo-platform/money-movement/payout-receive-amount",
    "card-checkout.md": "/yativo-platform/cards-and-accounts/card-checkout",
    "webhook-guide.md": "/yativo-platform/webhooks/overview",
    "webhook-resend-ui.md": "/yativo-platform/webhooks/resend",
    "individual-kyc-endorsement-resubmission.md": "/yativo-fiat/kyc#resubmit-one-endorsement",
    "api-responses-and-errors.md": "/yativo-platform/api-responses-and-errors",
    "fees.md": "/yativo-platform/money-movement/fees",
    "subscriptions.md": "/yativo-platform/business/subscriptions",
    "sandbox-testing.md": "/yativo-platform/testing/sandbox-testing",
    "employee-portal-integration.md": "/yativo-platform/business/employee-portal",
    "corporate-card-integration.md": "/yativo-platform/cards-and-accounts/corporate-cards",
    "virtual-card-integration.md": "/yativo-platform/cards-and-accounts/virtual-cards",
    "revenue-split-api-integration.md": "/yativo-platform/business/revenue-split",
    "affiliate-api-integration.md": "/yativo-platform/business/affiliate-program",
    "wallet-swap-integration.md": "/yativo-platform/money-movement/wallet-swaps",
    "onramp.md": "/yativo-platform/money-movement/onramp",
    "exchange-rates.md": "/yativo-platform/money-movement/exchange-rates",
    "SECURITY.md": "/yativo-platform/security/security-policy",
    "/webhooks/overview": "/yativo-platform/webhooks/overview",
}

DESCRIPTIONS: dict[str, str] = {
    "authentication.mdx": "Authenticate server-to-server calls with team API keys and manage keys from the dashboard API.",
    "api-responses-and-errors.mdx": "Response envelopes, error_details, validation errors, retries, and rate limits.",
    "webhooks/overview.mdx": "Register endpoints, verify signatures, event catalog, and delivery logs.",
    "cards-and-accounts/card-checkout.mdx": "Verify selling customers, create checkout orders, webhooks, refunds, and sandbox testing.",
    "security/team-management.mdx": "Invite team members, roles, permissions, and how members use the business API.",
    "business/kyc-endorsements.mdx": "Endorsement resubmission for individual and business customers.",
}

DROP_LINE_PATTERNS = [
    re.compile(r"WHOP_PLATFORM"),
    re.compile(r"`App\\Http\\Controllers"),
    re.compile(r"`config/team-roles\.php`"),
    re.compile(r"`ResolveTeamActingUser`"),
    re.compile(r"`EnforceTeamRoutePermission`"),
    re.compile(r"`config/team-legacy-route-permissions\.php`"),
    re.compile(r"`IDENTITY_EXEMPT_PATHS`"),
    re.compile(r"Spatie|Jetstream|tymon/jwt-auth"),
    re.compile(r"Laravel's `api\.php`"),
]


def title_from_markdown(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            body_start = i + 1
            break
    else:
        title = "Guide"
        body_start = 0
    while body_start < len(lines) and lines[body_start].strip() == "":
        body_start += 1
    body = "\n".join(lines[body_start:]).lstrip("\n")
    return title, body


def fix_links(text: str) -> str:
    for old, new in LINK_MAP.items():
        text = re.sub(rf"\]\(\./{re.escape(old)}", f"]({new}", text)
        text = re.sub(rf"\]\({re.escape(old)}", f"]({new}", text)
        if old.startswith("/"):
            text = text.replace(f"]({old}", f"]({new}")
        # Anchor-only variants: fees.md#foo -> /path#foo
        if old.endswith(".md"):
            base = old[:-3]
            text = re.sub(
                rf"\]\({re.escape(old)}(#[^)]+)\)",
                lambda m: f"]({new}{m.group(1)})",
                text,
            )
            text = re.sub(
                rf"\]\({re.escape(base)}\.md(#[^)]+)\)",
                lambda m: f"]({new}{m.group(1)})",
                text,
            )
    return text


def sanitize(text: str, source_name: str) -> str:
    text = fix_links(text)
    text = text.replace("https://test-api.yativo.com", "https://smtp.yativo.com")
    text = re.sub(
        r"\(`https://test-api\.yativo\.com` also serves sandbox\)",
        "(`https://smtp.yativo.com` for sandbox)",
        text,
    )

    if source_name == "card-checkout.md":
        text = re.sub(
            r"Each card payment lands on the \*\*selling customer's own\*\* connected business\naccount \(`biz_…` from card-checkout onboarding\) — not on Yativo's platform\n`WHOP_PLATFORM_COMPANY_ID`\. That platform id is reserved for \*\*Plans &\nSubscriptions Card Payment\*\* and for collecting Yativo's fee from sellers\.\n\n",
            "Each card payment lands on the **selling customer's own** connected business account (`biz_…` from card-checkout onboarding).\n\n",
            text,
        )

    if source_name == "TEAM_FUNCTIONALITY.md":
        # Drop internal architecture section
        text = re.sub(
            r"## Architecture\n.*?(?=## Authorization model)",
            "",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"## Team members on the wider API\n.*?(?=## Team API keys)",
            "## Team members on the wider API\n\n"
            "When a team member signs in to the dashboard, API calls run in the context of the "
            "business account according to their role. Viewers can only send `GET` requests; "
            "other roles need the matching permission for each action. Routes that change the "
            "member's own credentials (PIN, passkeys, profile) always run as that member.\n\n"
            "KYC belongs to the business, not the member. Once the owner passes KYC, members "
            "can use KYC-gated endpoints within their role.\n\n",
            text,
            flags=re.DOTALL,
        )
        text = text.replace(
            "Defined in `config/team-roles.php`. When a team is created, five default roles are seeded from this config",
            "When a team is created, five default roles are seeded",
        )
        text = text.replace(
            "Permissions are grouped for UI rendering (`config('team-roles.groups')`)",
            "Permissions are grouped for UI rendering",
        )

    if source_name == "rfis.md":
        text = text.replace("(Bridge, Noah, Tazapay, etc.)", "(payment partners)")

    out_lines = []
    for line in text.splitlines():
        if any(p.search(line) for p in DROP_LINE_PATTERNS):
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def to_mdx(rel_path: str, title: str, body: str) -> str:
    desc = DESCRIPTIONS.get(rel_path, f"{title} — integration guide for the Yativo API.")
    desc = desc.replace('"', '\\"')
    return (
        f"---\n"
        f'title: "{title}"\n'
        f'description: "{desc}"\n'
        f"---\n\n"
        f"{body.rstrip()}\n"
    )


def main() -> None:
    for source, dest in MAPPING.items():
        if not dest:
            continue
        src_path = GUIDE / source
        if not src_path.exists():
            print(f"skip missing {source}")
            continue
        raw = src_path.read_text(encoding="utf-8")
        title, body = title_from_markdown(raw)
        body = sanitize(body, source)
        out_path = DOCS / dest
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(to_mdx(dest, title, body), encoding="utf-8")
        print(f"wrote {dest} ({len(body.splitlines())} lines)")


if __name__ == "__main__":
    main()
