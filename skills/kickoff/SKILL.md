---
name: kickoff
description: >
  This skill should be used when the user types "/kickoff", or says "kick off a pitch", "hand a pitch over to the team",
  "the founders bet on a pitch" or "start cycle an id". Runs Shape Up phase 3: branch, draft PR, board, scopes and tech.md.
metadata:
  version: "0.1.0"
---

# /kickoff <pitch slug> <cycle id>

1. Load the `shapeup-team` skill with the Skill tool and follow its "Phase 3: Kickoff" section. You are the Conductor.
2. The pitch must have status `bet`. If it's `ready`, ask the user to confirm the founders' bet, then set `bet` and log it (`phase`).
3. Create the branch and draft PR, run `scaffold.py kickoff`, commit `S0 Conductor: kickoff`, push, log the `action`.
4. Orient: spawn `backend-drf`, `frontend-react` and `dba` in parallel with `Mode: orient (read-only)`.
5. Map scopes in sequence: `backend-drf` drafts → `frontend-react` amends → `dba` marks schema scopes → `qa-engineer` writes "Done when" → `product-owner` checks against the pitch.
6. Add tech.md when a scope touches the schema or adds an endpoint (`dba` draws Entities, `backend-drf` Classes, Flows and the API contract).
7. Run the Kickoff gate and `scaffold.py lint`; log the result. Report to the user in ≤5 lines: branch, PR, scopes, first scope, open HUMAN rows.
