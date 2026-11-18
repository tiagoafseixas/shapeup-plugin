# Docs standard

Which docs exist, what each one holds, and who owns it. How to write them: `writing-style.md`. How to draw: `diagrams.md`.
A fact lives in exactly one doc. If it isn't listed here, the team doesn't write it.

| Doc | Holds | Never holds | Owner | Template |
|---|---|---|---|---|
| `<docs>/team.md` | Paths, commands, versions, budgets | Process rules | Conductor + user | `team.md` |
| `<docs>/shell.txt` | The app shell every sketch is drawn in, and the app's screen conventions | Pitch-specific screens | designer (frontend role without one); filled at bootstrap | `shell.txt` |
| `<docs>/pitches/<slug>/pitch.md` | Problem, appetite, solution elements and breadboard, embedded sketches, rabbit holes, no-gos, works-when | Tasks, estimates, inventories of what exists or must be built, decisions taken after shaping | Shaper + user | `pitch.md` |
| `<docs>/pitches/<slug>/wireframes/` | One `<screen>.txt` per sketch and the `<screen>.svg` drawn from it | Hand-edited SVGs | Shaper + user | `diagrams.md` › Sketches |
| `<docs>/pitches/<slug>/log.md` | Audit trail: every decision, cut, gate result, phase change and action, with who, when and why | Discussion, questions (they go on the board) | everyone, append-only | `log.md` |
| `<docs>/pitches/<slug>/board.md` | Scopes and hill, the message Log, QA findings, retro | Decisions (they go to log.md), long explanations | everyone (own rows) | `board.md` |
| `<docs>/pitches/<slug>/tech.md` | Mermaid diagrams of what changes: entities, classes, flows, processes, delivery; API contract table | Anything the code states plainly; history (that's log.md) | backend role, DBA, frontend role, DevOps | `tech.md` |
| `<docs>/pitches/<slug>/runbook.md` | Manual ops for one release: Release (strategy, success metrics), Before, Steps, Rollback tables | Background or rationale beyond one clause per step; secret values | DBA, DevOps | `runbook.md` |
| `<docs>/betting/<date>.md` | Ready pitches side by side | Recommendations on which to bet | Shaper | `betting.md` |
| `<docs>/decisions.md` | Conventions that outlive a pitch (architecture, vendors, patterns) | Pitch-level decisions (log.md) | whoever decides | `decisions.md` |
| `<docs>/ideas.md` | Raw ideas, cut items, shortcuts to revisit | Commitments, priorities | Shaper | `ideas.md` |
| PR body | Shipped, cut, risks, ops | Code walkthroughs | Conductor | `pr.md` |

## Format rules per doc

| Doc | Rule |
|---|---|
| Runbook | Every step: command, what you should see, what to do if not. Step 1 is a backup when data changes. Rollback is always last. |
| Log row (board) | ≤3 sentences, self-contained: names the scope, the file or endpoint, and what is needed |
| log.md entry | One line of what, one clause of why. Names the thing in full, never "the above". |
| tech.md | One diagram per question, with a one-line caption above it. Only the parts that change, plus their direct neighbours. |
| pitch.md | Within the pitch word limit in `team.md` (default 600) outside code blocks. Sketches are drawn from `wireframes/*.txt`, never hand-made; `scaffold.py lint` flags a stale one. |
