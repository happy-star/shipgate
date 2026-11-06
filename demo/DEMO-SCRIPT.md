# ShipGate demo script (3–5 min)

**Track:** Flip the Switch — Track 01 Best Business Workflow  
**Product:** Switch Rooms (agents + human in one room)

## Setup (before recording)
1. Switch Console running (local or Vultr host).
2. Import `shipgate.room.yaml` (Templates → Import) or ask switch-buddy to run it.
3. Connect Slack or Discord as the bridge (hackathon requires a real chat surface).
4. Optional offline path: `python3 src/foreman.py` to show the gate logic.

## Spoken walkthrough
1. **Problem (30s)** — Teams let agents open PRs that merge without a crisp human gate. ShipGate makes APPROVE SHIP a first-class Switch room step.
2. **Room tour (60s)** — Show the Switch room with triager, fixer, scribe + you. Point at room instructions / hard rules.
3. **Kickoff (90s)** — Paste the incident (or let kickoff run). Triager posts severity + blast radius. Fixer drafts the minimal patch + verification. Scribe keeps the log.
4. **Human gate (60s)** — Show agents stopping. You type `APPROVE SHIP` (or `REJECT …`). Narrate that Switch addressing + room policy is what makes this a workflow, not a chatbot.
5. **Close (30s)** — Recap: Switch-native template, real chat bridge, deterministic gate, business value = safer ships without slowing agents.

## Offline backup
If Switch Console is unavailable on camera:
```bash
python3 src/foreman.py
# then type APPROVE SHIP or REJECT ...
```
Still narrate that production is Switch rooms; foreman is the policy stub.
