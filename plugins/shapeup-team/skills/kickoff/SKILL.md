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
2. Every row in `team.md` › Roles must have its stack pack installed (load each with the Skill tool). A missing pack stops the kickoff: offer `/stack new <name>`.
3. The pitch must have status `bet`. If it's `ready`, ask the user to confirm the founders' bet, then set `bet` and log it (`phase`).
4. Create the branch and draft PR, run `scaffold.py kickoff`, commit `S0 Conductor: kickoff`, push, log the `action`.
5. Orient: spawn every developer role in `team.md` › Roles (`backend-dev` / `frontend-dev` with its role id) and `dba`, in parallel, with `Mode: orient (read-only)`.
6. Map scopes in sequence: backend roles draft → frontend roles amend → `dba` marks schema scopes → `qa-engineer` writes "Done when" → `product-owner` checks against the pitch.
7. Add tech.md when a scope touches the schema or adds an endpoint (`dba` draws Entities, the backend role Classes, Flows and the API contract).
8. Run the Kickoff gate and `scaffold.py lint`; log the result. Report to the user in ≤5 lines: branch, PR, scopes, first scope, open HUMAN rows.
