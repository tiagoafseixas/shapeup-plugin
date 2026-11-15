# Protocol: how roles talk

Roles never talk to each other directly. They write rows in the **Log** table of `board.md`. The Conductor reads the
Log and routes each open row to the next turn. If it isn't in the Log, it wasn't said. Every decision also goes in `log.md`.
All text follows `writing-style.md`.

## Log row

`| # | Rnd | From | To | Type | Message | Status |`

- `#`: next integer. Never renumber. Refer to other rows as `re #12`.
- `Rnd`: the current round (0 during kickoff).
- `From` / `To`: `PO`, `QA`, `DBA`, `Conductor`, `user`, `ALL`, or a developer's role id from `team.md` › Roles (e.g. `backend-drf`, `frontend-react`).
- `Message`: ≤3 sentences, self-contained. A reader must understand it without opening another file: name the scope (`S2`),
  the file or endpoint, and what you need. HUMAN rows add `Options: A) … B) … Rec: A. Waiting: <what>.`
- `Status`: `NOTE`, `ANSWER`, `DECIDE` and `DONE` rows are created `done`. `ASK`, `HANDOFF`, `BLOCK`, `FLAG` and `HUMAN` start `open`,
  and are closed by their addressee (`done`) or by the PO (`dropped`, with the reason).

## Types

| Type | Use it when | Addressee must |
|---|---|---|
| `NOTE` | Orientation or FYI. No answer needed. | — |
| `ASK` | You need a decision or information to continue | Reply with an `ANSWER` row in the next round and close the ASK |
| `ANSWER` | Replying to an ASK (`re #n`) | — |
| `HANDOFF` | Your part is ready for the next role (contracts below) | Pick it up next turn, close it when taken |
| `BLOCK` | You cannot continue any scope without this | Handle it first |
| `FLAG` | Stall, scope creep, budget risk, or something outside the pitch | PO decides: cut, split, ignore, or `HUMAN` |
| `DECIDE` | You decided something others must know. Also append it to log.md as `decision`. | — |
| `HUMAN` | Only the user can decide: the pitch's boundaries, appetite, money, security exceptions, prod ops, merges. Also: requests for read-only DB access, and every DBA backup announcement. | Conductor batches it to the user; the user's answer goes to log.md. A backup announcement is the one HUMAN row sent immediately, not batched. |
| `DONE` | A scope passed QA (QA writes it) | — |

## Handoff contracts

A HANDOFF row without its contract is invalid, and the Conductor sends it back.

| From → To | The row must contain |
|---|---|
| backend → frontend | The endpoints (`METHOD path`), with the full contract in the tech.md API table, committed. Permissions in one line. |
| backend → DBA | Migration file paths and what each does, in plain words. Expected size of the tables touched. |
| DBA → backend | Verdict: `approve`, or `rewrite` with the exact change (or the rewritten files). Whether a runbook is needed. |
| Dev → QA | Scope, what changed (≤2 sentences), how to run it locally, commands already green |
| QA → Dev | One QA table row per finding: severity, case, expected vs actual |
| PO → anyone | The decision, and what is now cut or kept |
| anyone → user | The question, options A/B(/C), a recommendation, and what waits on it |

## Hill chart

Each scope has a `Hill` value from 0 to 100. Only the scope's owner moves it, and only with evidence.

| Value | Meaning | Evidence to claim it |
|---|---|---|
| 0–49 ▲ | Figuring it out: unknowns remain | — |
| 50 | Top of the hill: approach proven, no unknowns left | A working slice or spike in code (commit hash) |
| 51–99 ▼ | Making it happen: just execution | Commits |
| 100 ✓ | Done | QA `DONE` row |

`Moved` holds the round of the last increase. The Conductor uses it for the stall rule. Moving a scope backwards
is allowed and honest: write a `NOTE` with the reason.

## Turn report

Every role ends its turn by returning exactly this (≤10 lines). `TESTS` lists the red run, the tests per size, and each changed test with its `NOTE` row. The Conductor checks it against the board and log.md.

```
ROLE: backend-drf   ROUND: 3   SCOPE: S2
DID: deal_win service + POST /api/deals/{id}/win/ + tests
HILL: S2 35 → 60
LOG: board #14 HANDOFF → frontend-react, #15 ASK→PO · log.md #9 decision
COMMITS: 9f8e7d6 S2 backend-drf: red — owner wins open deal · a1b2c3d S2 backend-drf: win deal service and API
TESTS: red 5 failing → green · small 6 · medium 12 · changed: none
CHECKS: pytest backend/deals -q → 18 passed; ruff → clean
RISK: none | <one line>
```

## Etiquette

- Answer what you were asked, then stop. Follow the turn priority in SKILL.md.
- Never edit another role's rows or scopes. Reply with a new row.
- If the pitch is silent, ASK the PO. Don't invent product behaviour.
- If your work needs a change in another role's files (e.g. the frontend needs a field), send an ASK. Don't make the change yourself.
