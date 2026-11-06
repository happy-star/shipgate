# Incident: checkout-api 5xx spike

- **Opened:** 2026-11-06 02:14 UTC
- **Service:** checkout-api (us-east-1)
- **Symptom:** HTTP 500 on `POST /v1/checkout` for carts that include a zero-tax SKU
- **Error rate:** ~12% of checkout POSTs (was <0.2% baseline)
- **Deploy marker:** `checkout-api@2026.11.05.18` rolled out 01:55 UTC
- **Payments:** Stripe/PayPal webhooks healthy; money is not double-charged
- **Customer impact:** Shoppers see "Something went wrong" and retry; ~30 support tickets

## Recent change
Tax calculator refactor landed in the deploy above. CI was green on the PR but the suite did not cover zero-rate SKUs.

## Ask for ShipGate
Triage → draft hotfix → **human APPROVE SHIP** before merge/canary.
