#!/usr/bin/env python3
"""ShipGate foreman — deterministic demo of the human ship gate.

This is a local stub so judges can see the gate without a live Switch server.
In production the same policy is enforced inside the Switch room: agents prepare,
only an explicit human APPROVE SHIP continues.

Usage:
  python3 src/foreman.py                 # interactive gate demo
  python3 src/foreman.py --auto-reject   # non-interactive reject path
  python3 src/foreman.py --auto-approve  # non-interactive approve path (demo only)
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


@dataclass
class ShipBrief:
    title: str
    severity: str
    blast_radius: str
    suspected_cause: str
    recommendation: str
    verification: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)


@dataclass
class GateResult:
    decision: str  # APPROVE SHIP | REJECT | PENDING
    actor: str
    reason: str
    at_utc: str


def load_incident() -> str:
    path = FIXTURES / "sample-incident.md"
    return path.read_text(encoding="utf-8") if path.exists() else "(missing fixtures/sample-incident.md)"


def draft_brief() -> ShipBrief:
    return ShipBrief(
        title="checkout-api 5xx spike after deploy",
        severity="SEV2",
        blast_radius="~12% of checkout POSTs failing in us-east; payments still settle",
        suspected_cause="Null pointer in tax calculator when cart has zero-rate SKU (see fake-ci-log.txt)",
        recommendation="prepare hotfix",
        verification=[
            "unit: tax_calculator handles zero-rate SKU",
            "smoke: POST /checkout with fixture cart returns 200",
            "canary: 5% traffic for 10 minutes, error rate < 0.5%",
        ],
        risks=[
            "Hotfix touches shared tax module — keep diff ≤ 20 LOC",
            "No secret rotation required",
        ],
    )


def print_brief(brief: ShipBrief) -> None:
    print("=== ShipGate brief (agent-prepared) ===")
    print(f"Title:          {brief.title}")
    print(f"Severity:       {brief.severity}")
    print(f"Blast radius:   {brief.blast_radius}")
    print(f"Suspected cause:{brief.suspected_cause}")
    print(f"Recommendation: {brief.recommendation}")
    print("Verification:")
    for step in brief.verification:
        print(f"  - {step}")
    print("Risks:")
    for risk in brief.risks:
        print(f"  - {risk}")
    print()
    print("HARD GATE: agents stop here. Only a human may continue.")
    print("Reply exactly: APPROVE SHIP   or   REJECT <reason>")
    print()


def decide(raw: str, actor: str) -> GateResult:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = (raw or "").strip()
    upper = text.upper()
    if upper.startswith("APPROVE SHIP"):
        return GateResult("APPROVE SHIP", actor, text, now)
    if upper.startswith("REJECT"):
        reason = text[6:].strip() or "no reason given"
        return GateResult("REJECT", actor, reason, now)
    return GateResult("PENDING", actor, f"unrecognized input: {text!r}", now)


def main() -> int:
    parser = argparse.ArgumentParser(description="ShipGate human-gate demo stub")
    parser.add_argument("--auto-approve", action="store_true", help="Demo path: approve without prompt")
    parser.add_argument("--auto-reject", action="store_true", help="Demo path: reject without prompt")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result")
    args = parser.parse_args()

    print("--- incident fixture (excerpt) ---")
    print("\n".join(load_incident().splitlines()[:12]))
    print("...\n")

    brief = draft_brief()
    print_brief(brief)

    if args.auto_approve:
        raw, actor = "APPROVE SHIP", "demo-auto"
    elif args.auto_reject:
        raw, actor = "REJECT demo hold — need more canary data", "demo-auto"
    else:
        try:
            raw = input("> ")
        except EOFError:
            raw = ""
        actor = "human"

    result = decide(raw, actor)

    if result.decision == "APPROVE SHIP":
        outcome = "Gate OPEN — document deploy steps; still no auto-merge in this stub."
    elif result.decision == "REJECT":
        outcome = f"Gate CLOSED — {result.reason}"
    else:
        outcome = "Gate still PENDING — agents must not ship."

    payload = {
        "brief": asdict(brief),
        "gate": asdict(result),
        "outcome": outcome,
        "switch_note": "Live runs use Switch rooms + shipgate.room.yaml; this stub is for offline demos.",
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Decision: {result.decision}")
        print(f"Actor:    {result.actor} @ {result.at_utc}")
        print(f"Outcome:  {outcome}")

    return 0 if result.decision in {"APPROVE SHIP", "REJECT"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
