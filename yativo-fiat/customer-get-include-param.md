# API Update: Get Customer now supports `?include` for embedded data

**Date:** May 13, 2026  
**Endpoint affected:** `GET /customer/{customer_id}`  
**Breaking change:** No — fully backward compatible

---

## What changed

The **Get Customer** endpoint has been updated to support an `?include` query parameter. Previously the endpoint always returned all related data (deposits, payouts, virtual accounts, etc.) embedded in every response.

Going forward, **related data is no longer embedded by default**. The base response returns only the customer's core profile fields. You must explicitly request the relations you need.

---

## New query parameter

| Parameter | Type | Required |
|---|---|---|
| `include` | `string` | No |

**Accepted values:**

| Value | Returns |
|---|---|
| `deposits` | `customer_deposit` — array of deposit transactions |
| `payouts` | `customer_payouts` — array of payout transactions |
| `virtualaccounts` | `customer_virtualaccounts` — array of virtual accounts |
| `virtual_cards` | `customer_virtual_cards` — array of issued virtual cards |
| `crypto_wallets` | `customer_crypto_wallets` — array of crypto wallet addresses |
| `all` | All of the above at once |

Combine multiple values with commas: `?include=deposits,payouts`

---

## Examples

**Return everything (equivalent to old behavior):**
```bash
GET /api/v1/customer/{customer_id}?include=all
```

**Return only virtual accounts and virtual cards:**
```bash
GET /api/v1/customer/{customer_id}?include=virtualaccounts,virtual_cards
```

**Return only the profile (no related data):**
```bash
GET /api/v1/customer/{customer_id}
```

---

## What you need to do

If you are currently calling `GET /customer/{customer_id}` and reading any of these fields from the response:

- `customer_deposit`
- `customer_payouts`
- `customer_virtualaccounts`
- `customer_virtual_cards`
- `customer_crypto_wallets`

**You must add `?include=all` (or the specific fields you need) to your request**, otherwise those keys will be absent from the response.

Requests that only read core profile fields (`customer_name`, `customer_email`, `customer_status`, `customer_kyc_status`, etc.) require no changes.

---

## Updated endpoint path

The canonical path is now:

```
GET /api/v1/customer/{customer_id}
```

> Note: Previous documentation incorrectly showed the path as `/customer/customer/{customer_id}` (double `customer`). The correct path has always been `/customer/{customer_id}`. If you have been using the doubled path and it worked, it was being silently redirected — please update your integration to use the single-segment path to avoid issues in future.

---

## Sample response with `?include=all`

```json
{
  "status": "success",
  "status_code": 200,
  "message": "Request successful",
  "data": {
    "customer_id": "c586066b-0f29-468f-b775-15483871a202",
    "customer_name": "Alex Smith",
    "customer_email": "alex.smith@example.com",
    "customer_phone": "+15551234567",
    "customer_country": "USA",
    "customer_type": "individual",
    "customer_status": "active",
    "customer_kyc_status": "approved",
    "kyc_verified_date": "2026-04-02T12:00:00.000000Z",
    "created_at": "2026-04-02T10:00:00.000000Z",
    "customer_deposit": [ /* deposit transaction objects */ ],
    "customer_payouts": [ /* payout transaction objects */ ],
    "customer_virtualaccounts": [ /* virtual account objects */ ],
    "customer_virtual_cards": [ /* virtual card objects */ ],
    "customer_crypto_wallets": [ /* crypto wallet objects */ ]
  }
}
```

---

## Questions?

Contact [support@yativo.com](mailto:support@yativo.com) or open a ticket in the developer portal.
