---
name: round
description: >
  This skill should be used when the user types "/round", or says "run a round", "next round", "continue the cycle",
  "keep building a pitch" or "run rounds until you need me". Runs Shape Up build rounds, ship and cool-down for a pitch.
metadata:
  version: "0.1.0"
---

# /round <pitch slug> [count]

1. Load the `shapeup-team` skill with the Skill tool and follow "Phase 4: Build in rounds". You are the Conductor.
2. Run one round, or `count` rounds. Stop early when a `HUMAN` row needs the user and no other role has work, when the
   circuit breaker hits 100%, or when every must scope is `DONE`.
3. Each round: dispatch PO → DBA → backend roles → frontend roles → QA, one turn per role at most, by spawning the role's agent (`product-owner`, `dba`, `backend-dev`, `frontend-dev`, `qa-engineer`) with its role id from `team.md` › Roles in the brief.
   Override `model` only per the Models table (`haiku` for a mechanical turn, escalation one step up).
4. After each turn, check the turn report against the board (red commit first for dev turns with code) and run `scaffold.py lint`.
5. End of round: increment Rounds, push, apply the breaker, then send the user all open `HUMAN` rows in one message. A DBA backup announcement goes at once.
6. All must scopes `DONE`: run Phase 5 (Ship) with `/gate ship`. After the user reports the merge, run Phase 6 (Cool-down).
