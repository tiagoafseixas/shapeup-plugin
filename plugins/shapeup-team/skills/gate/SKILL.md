---
name: gate
description: >
  This skill should be used when the user types "/gate", or asks to "run the ready gate", "check if the pitch is ready",
  "run the scope gate on S2", "run the ship gate" or "is a pitch ready to ship". Runs one Shape Up gate and logs the result.
metadata:
  version: "0.1.0"
---

# /gate <ready | kickoff | scope S<n> | ship> <pitch slug>

1. Load the `shapeup-team` skill with the Skill tool. Gates live in `references/gates.md`.
2. Who runs it:

| Gate | Run by |
|---|---|
| ready, kickoff | this session (Conductor; Shaper for ready) |
| scope S<n> | spawn the `qa-engineer` agent with `Your turn: Scope gate S<n>` |
| ship | spawn the `qa-engineer` agent with `Your turn: Ship gate`, then this session does the Conductor rows (PR body, mark it ready with the PR tool, report) |

3. Check every row; a row passes only with evidence (command output, file, board row). The ready gate is offline: evidence comes from files and the user's answers, never from running anything external.
4. Append the result to the pitch's log.md (`scaffold.py log … --kind gate`): `<Gate>: pass`, or `<Gate>: fail on rows 2, 5: <one clause each>`.
5. Reply with the result and, on a fail, the failing rows and who owns each fix.
