# Sample Switch room transcript (ShipGate)

> Illustrative Slack/Discord-style transcript for judges. Names match `shipgate.room.yaml`.

**system** — Room `shipgate-ship` created from template. Agents joined: shipgate-triager, shipgate-fixer, shipgate-scribe. Users: peter.

**peter** — @shipgate-triager @shipgate-fixer @shipgate-scribe kicking off with fixtures/sample-incident.md

**shipgate-triager** — Ship brief:
- Severity: SEV2
- Blast radius: ~12% checkout POSTs in us-east; payments healthy
- Suspected cause: `tax.py` NPE when `sku.region` is None (see fake-ci-log.txt)
- Recommendation: prepare hotfix
@shipgate-fixer please draft the smallest guard + regression test. Do not merge.

**shipgate-fixer** — Plan:
1. Guard `sku.region is None` → treat as zero-rate
2. Add `test_zero_rate_sku`
3. Verify: unit + smoke POST /checkout
4. Risks: shared tax module — keep diff tiny
Stopping for human gate. @peter reply `APPROVE SHIP` or `REJECT <reason>`.

**shipgate-scribe** — Ship log started (UTC). Waiting on human gate.

**peter** — APPROVE SHIP

**shipgate-scribe** — Gate OPEN recorded. Release note draft ready. Agents still will not auto-merge; peter owns the deploy click / protected-branch merge.
