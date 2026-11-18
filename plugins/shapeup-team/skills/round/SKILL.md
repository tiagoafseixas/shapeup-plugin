---
name: round
description: >
  This skill should be used when the user types "/round", or says "run a round", "next round", "continue the cycle",
  "keep building a pitch" or "build until you have something to show me". Runs one Shape Up review round (work until there
  is something to review with the user), then ship and cool-down when the build is done.
metadata:
  version: "0.2.0"
---

# /round <pitch slug>

One round = from a goal to a review with the user. Load the `shapeup-team` skill with the Skill tool and follow
"Phase 4: Build in review rounds". You are the Conductor.

1. **Goal.** With the Shaper, pick the scopes to bring to a reviewable state; write "Round <n> goal: …" as a `NOTE` to `ALL`.
2. **Work loop**, one turn at a time, no fixed order: pick the next turn with the Routing table and Turn priority; spawn the role's agent
   (`shaper`, `dba`, `backend-dev`, `designer`, `frontend-dev`, `qa-engineer`, `devops`) with its role id from `team.md` › Roles;
   override `model` only per the Models table. After each turn: check the turn report against the board (red commit first for dev turns with code),
   run `scaffold.py lint`, add 1 to the turn counters, act on new rows at once.
3. **Stop the loop** when every goal scope has a QA `DONE` row, when a `HUMAN` row blocks everything left (ask the user now), or at the turn cap
   (`team.md`, default 30: report status instead of a demo).
4. **Review with the user**: per goal scope, what it does, how to try it, what was cut, screenshots when possible; then the open questions.
   The user accepts each scope or gives findings.
5. **After the review**: findings become rows to their owners (`must` only when they break a promise of the scope), log the review,
   add 1 to Reviews, push, apply the circuit breaker.
6. Every must scope accepted: run Phase 5 (Ship: QA's full suite, then the final review with the user). After the user reports the merge,
   run Phase 6 (Cool-down).
