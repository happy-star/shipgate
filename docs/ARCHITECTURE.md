# ShipGate architecture

```
┌──────────────────────────────┐
│  Chat bridge (Slack/Discord) │
│  = Switch room surface       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  Switch server + Console     │
│  room template: shipgate.room.yaml
│  agents: triager / fixer / scribe
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐   ┌─────────────────┐
│ Agent hosts │   │ Human (creator) │
│ (Claude /   │   │ APPROVE SHIP /  │
│  Codex /    │   │ REJECT          │
│  Cursor…)   │   └─────────────────┘
└─────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Optional: src/foreman.py     │
│ deterministic gate stub for  │
│ offline / CI demos           │
└──────────────────────────────┘
```

## Why Switch is central
- **Room** = durable shared context + roles (not a one-off chat).
- **Template** = reproducible business workflow (import once, run per incident).
- **Addressing** = agents only act when mentioned / policy allows — supports the human gate.
- **Bridge** = real Slack/Discord/Teams where on-call already lives (hackathon requirement).

## Trust boundary
Agents prepare; humans decide. No secrets in the repo. Production credentials stay in Switch Console / host env, never in YAML.
