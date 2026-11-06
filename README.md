# ShipGate

**Flip the Switch — Track 01: Best Business Workflow**  
Human-gated ship workflow built **on Switch Rooms**: agents triage and draft; only a human `APPROVE SHIP` unlocks merge/deploy.

- Hackathon: [Flip the Switch](https://www.wemakedevs.org/hackathons/switch) (deadline **Nov 7, 2026 11:59 PM IST**)
- Switch docs: [Getting started](https://docs.switchagents.ai/switch-rooms/getting-started) · [Room templates](https://docs.switchagents.ai/switch-rooms/administer/room-templates)
- Switch source: [sandbox-quantum/switch](https://github.com/sandbox-quantum/switch)
- Submit: [wemakedevs submit](https://www.wemakedevs.org/hackathons/switch/submit)

> Switch is not a side integration — **the product is a Switch room**. Slack/Discord/Teams is the bridge; `shipgate.room.yaml` is the workflow.

## Problem

Incident chats fill with agent noise. Someone pastes a patch, CI looks green-ish, and a merge lands without a crisp owner decision. Business risk: bad hotfix, no audit trail, unclear rollback.

ShipGate turns that into a **repeatable Switch workflow**:

1. **Triager** classifies severity + blast radius  
2. **Fixer** drafts the smallest safe fix + verification  
3. **Scribe** keeps the ship log / release note  
4. **Human gate** — only `APPROVE SHIP` or `REJECT` continues  

Agents never merge or deploy on their own.

## Why Switch (judging notes)

| Criterion | How ShipGate uses Switch |
| --- | --- |
| Real Switch usage | Room template + three agents + kickoff; importable in Switch Console |
| Chat surface | Room mirrored to Slack / Discord / Teams / Telegram / Mattermost via Switch bridge |
| Agent collaboration | Triager → Fixer → Scribe with Switch addressing policies |
| Human in the loop | Hard gate in room instructions; creators must reply in-room |
| Business workflow | Incident → brief → patch plan → approve → ship log (on-call ready) |
| Reproducible | `shipgate.room.yaml` + agent markdown briefs + fixtures |

Official template style mirrored from Switch examples (`params`, `agents`, `room`, `kickoff`). See [red-blue workroom](https://github.com/sandbox-quantum/switch/blob/main/examples/room-templates/red-blue-workroom.template.yaml) and [triage-pair](https://github.com/sandbox-quantum/switch/blob/main/examples/agent-templates/triage-pair.template.yaml).

## Agents

| Agent | Role |
| --- | --- |
| `{team}-triager` | Severity, blast radius, ship-or-hold brief (`agents/triager.md`) |
| `{team}-fixer` | Minimal fix + verification; stops before merge (`agents/fixer.md`) |
| `{team}-scribe` | Timeline, gate record, release note (`agents/scribe.md`) |

Optional offline stub: `src/foreman.py` — same gate policy without a live Switch server (for CI / camera backup).

## Repo layout

```
shipgate.room.yaml      # Switch room template (import this)
agents/                 # Agent instruction briefs
src/foreman.py          # Deterministic human-gate demo stub
fixtures/               # Sample incident + fake CI log
demo/                   # DEMO-SCRIPT + sample chat transcript
docs/ARCHITECTURE.md    # Diagram + trust boundary
```

## Setup (Switch-first)

### 1. Install Switch
Follow [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started): install **Switch Console**, start a local server (or join a team server), pick an agent provider (Claude Code / Codex / Cursor / OpenCode / Antigravity).

### 2. Connect a messaging app
Connect Slack or Discord (hackathon expects a real chat surface). Docs: [messaging apps](https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/).

### 3. Import ShipGate
1. Clone this repo next to your agent working dirs.  
2. Switch Console → **Templates** → **Import template** → paste / load `shipgate.room.yaml`.  
3. Or ask `switch-buddy` / Switch expert: *“Import and run the ShipGate room template from this folder.”*  
4. Fill params (`team`, provider, bridge). Create room + agents.

### 4. Run the demo incident
Kickoff already points agents at `fixtures/sample-incident.md` and `fixtures/fake-ci-log.txt`.  
Watch the room: brief → fix plan → scribe log → **you** type `APPROVE SHIP` or `REJECT …`.

### 5. Offline gate stub (optional)
```bash
python3 src/foreman.py
# or: python3 src/foreman.py --auto-reject
```

## Demo

See [`demo/DEMO-SCRIPT.md`](demo/DEMO-SCRIPT.md) and sample transcript [`demo/CHAT-TRANSCRIPT.md`](demo/CHAT-TRANSCRIPT.md).

Record 3–5 minutes showing the **Switch room** (not only the Python stub).

## Deploy later (Vultr)

Target host: `140.82.0.23` (XRDP + Docker). This scaffold only publishes the GitHub repo. Next install steps:

1. SSH/RDP to the host; install / open **Switch Console** (or self-host Switch server via Docker per [self-host docs](https://docs.switchagents.ai/switch-rooms/deploy/self-host)).  
2. `git clone https://github.com/happy-star/shipgate.git && cd shipgate`  
3. Import `shipgate.room.yaml`; point agent working directories at the clone.  
4. Connect Slack/Discord bridge; run kickoff.  
5. Keep secrets in host env / Switch Console — **never** commit `.env`.

## License

MIT — see [`LICENSE`](LICENSE).

## Disclaimer

No production credentials, API keys, or customer data are included. Fixtures are synthetic.
