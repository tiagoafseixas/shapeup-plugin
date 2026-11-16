<p align="center">
  <img src="docs/logo.svg" width="600" alt="Five round characters on a hill chart: the frontend dev with a paintbrush and the backend dev with a gear climbing, the PO holding a flag at the top, QA with a magnifier and the DBA carrying a database coming down.">
</p>

<h1 align="center">shapeup-team</h1>

<p align="center"><em>Five agents. One hill. Work gets done.</em></p>

---

You have an idea. Everyone has an idea.

The PO reads it, asks what people do today instead, and cuts it in half. Then cuts the half.
What's left fits on one page and says, in writing, what it won't do.

The founders bet on it. Or they don't, and it waits. Nothing carries over.

Then the crew walks up the hill.

**The frontend dev** goes first, paintbrush in hand. Queries by role, never by CSS class. Has opinions about empty states.

**The backend dev** follows with a gear. Thin handlers, fat models, a service for anything with a side effect. Writes the failing test first, every time, and commits it so you can check.

**The PO** stands at the top holding the flag. Not to celebrate. To mark the line: past it, nothing new gets figured out. It only gets made.

**QA** comes down the other side with a magnifier. Wrote "Done when" before anyone wrote code. Will not let you change a test to make it pass.

**The DBA** carries the database like it's fragile, because it is. In production: backups. Only backups. And asks first.

Somewhere below, the Conductor counts rounds. At 75% of the budget, the scope gets hammered. At 100%, the build stops.
Nobody extends it but you.

They don't do standups. They write one row on the board and get back to work.

This plugin puts that crew inside Claude.

---

**What it is.** A Shape Up product team of Claude agents. The main Claude session is the **Conductor**: it runs the phases,
dispatches the roles and enforces the gates. The roles are stack-agnostic; **stack packs** teach them your stack.
A hook blocks what the team must never do: work outside its area, rewrite git history, deploy, or write to production.
The process is fixed. How each role solves its step is up to the role.

## Install

The repo is a plugin marketplace: the team, plus one plugin per stack pack. Install the team and the packs your project uses.

| Where | How |
|---|---|
| Claude Code | `/plugin marketplace add tiagoafseixas/shapeup-plugin`, then `/plugin install shapeup-team@shapeup` and each pack, e.g. `/plugin install stack-react-mui@shapeup` |
| Claude app | Build each `.plugin` file (`cd plugins/<name> && zip -r ../../<name>.plugin . -x '*.DS_Store'`) and upload it |

Needs `python3` on the PATH (the guard hook) and `gh` (branches and draft PRs). The [Ponytail](https://github.com/DietrichGebert/ponytail) plugin is recommended for code review.

## How a pitch moves

| # | Phase | Who | Output | Command |
|---|---|---|---|---|
| 0 | Setup (once per repo, offline) | Conductor + user | `shape/team.md` filled from the repo's files and your answers, stack packs installed | `/gate setup` |
| 1 | Shape (offline) | User + PO | `pitch.md` with status `ready`, `log.md` | `/shape` |
| 2 | Bet | Founders | Pitch status `bet` with a cycle id | — |
| 3 | Kickoff | Conductor → all roles | Branch, draft PR, board with scopes, `tech.md` | `/kickoff` |
| 4 | Build | Roles, in rounds | Scopes move over the hill to done | `/round` |
| 5 | Ship | QA → Conductor | PR marked ready, runbook if ops are needed | `/gate ship` |
| 6 | Cool-down | Conductor + PO | Retro; cut items in `shape/ideas.md` | `/round` (after the merge) |

Setup and shaping are offline: the team reads files and asks you. No GitHub calls, no database connections (local or production),
no test runs, no installs; the hook asks you before any of them while no pitch has a board. The kickoff is the first time anything runs.

Appetite is a round budget, not a calendar: Small batch 8 rounds, Big batch 20 by default. At 75% the PO hammers scope; at 100%
the build stops and the default is drop and re-shape. Only the user extends.

## Commands

| Command | Does |
|---|---|
| `/shape [idea or slug]` | Shapes a pitch with the user; role agents run read-only tech checks; Ready gate |
| `/kickoff <slug> <cycle>` | Checks the stack packs, then branch `cycle/<cycle>-<slug>`, draft PR, board, scope map, `tech.md`, Kickoff gate |
| `/round <slug> [count]` | Runs build rounds (PO → DBA → backend roles → frontend roles → QA), applies the circuit breaker, batches questions for the user |
| `/gate <setup / ready / kickoff / scope S<n> / ship> <slug>` | Runs one gate and logs the result |
| `/stack [list / new <name> / house <role id> / lint <dir>]` | Lists the project's packs, writes a new pack from the stack's official docs, adds house rules |

## Roles

| Agent | Role | Default model | May edit (hook-enforced) |
|---|---|---|---|
| `product-owner` | PO: answers questions during the build, hammers scope, guards no-gos | Sonnet | `shape/**` except `team.md` |
| `backend-dev` | Backend developer, any stack: domain, services, APIs, migrations | Sonnet | Its role's path from `team.md` › Roles; the pitch's `tech.md`, `board.md`, `log.md` |
| `frontend-dev` | Frontend developer, any stack: screens, components | Sonnet | Its role's path; the pitch's `tech.md`, `board.md`, `log.md` |
| `qa-engineer` | QA: "Done when" checks, Scope and Ship gates, Large tests | Sonnet | Test files; the pitch's `board.md`, `log.md` |
| `dba` | DBA, any database: migration review, indexes, runbooks, backups | Opus | Migrations; the pitch's `tech.md`, `runbook.md`, `board.md`, `log.md` |

Shaping runs in the main session on Opus. The Conductor drops a turn to Haiku when the work is fully specified, and escalates one
step up when a turn fails. Call a role directly: "DBA, review migration 0008 on deal-win-tracking", "frontend-react, pick up S1".

## Stack packs

Three layers of knowledge, each with one job:

| Layer | Says | Lives in | Wins over |
|---|---|---|---|
| Process | What to do and when: tests first, handoffs, gates, guardrails | `shapeup-team` (role files, standards) | everything, on process |
| Stack pack | How, in this stack: layering, rules, test tools per size, performance, review checklist, indexed docs | one plugin per stack, e.g. `stack-react-mui` | the generic role file, on how |
| House rules | How, in this repo: only what differs from the pack | `shape/stack/<role id>.md` in your repo | the pack |

| Pack | Layer | Covers |
|---|---|---|
| `stack-django-drf` | backend | Django 5–6, DRF: thin views, fat models, service layer; pytest-django or the Django runner |
| `stack-nextjs-chakra` | frontend | Next.js App Router, React 18–19, Chakra UI v3 |
| `stack-react-mui` | frontend | React 18–19, Material UI v7 and v9, MUI X; Vite or Next.js |
| `stack-postgres-cloudsql` | database | PostgreSQL 13–18 on Cloud SQL: zero-downtime migrations (Django operations included), read-only user, backups |

Your project wires roles to packs in `shape/team.md`. Each developer role is an agent plus a pack; a project with two backends has two rows:

```markdown
| Role id        | Agent        | Stack pack              | Path      |
|----------------|--------------|-------------------------|-----------|
| backend-drf    | backend-dev  | stack-django-drf        | backend/  |
| frontend-react | frontend-dev | stack-react-mui         | ../web    |
| database       | dba          | stack-postgres-cloudsql | —         |
```

Moving from Chakra to MUI is one cell: change the pack, install it. No stack in the list? `/stack new <name>` scaffolds a pack,
indexes the stack's official docs into `references/sources.md`, writes the rules from them, and lints the result (`scaffold.py lint-pack`).
Every pack has the same sections, so the agents always know where to look.

## Guardrails (hook-enforced)

The guard runs before every `Write`, `Edit` and `Bash` call in a repo with `shape/team.md`, and on every call made by a team agent.

| Blocked | Asks the user first |
|---|---|
| Edits outside the role's area (Roles table) | Before the first kickoff: any `gh` call, git remote call, install, database client, test run, container or `curl` |
| | Any production connection: `$READONLY_DATABASE_URL`, a database client aimed at a remote host, `cloud-sql-proxy`, `gcloud sql` / `aws rds` reads (backend role and DBA only) |
| `.env*` writes | `gcloud sql backups create`, `aws rds create-db-snapshot` (DBA only) |
| Force-push, push to `main`/`master`, merge, rebase, `gh pr merge`, `--no-verify` | |
| Deploys: `gcloud app/run/functions deploy`, `gcloud builds submit`, `deploy.sh`, `terraform apply`, `kubectl apply` | |
| Every other `gcloud sql` or `aws rds` write; any production access by the PO, QA or frontend roles | |
| Any `…DATABASE_URL` other than `READONLY_DATABASE_URL`, `PGPASSWORD=`, `MYSQL_PWD=`, literal non-local database URLs, production settings | |

Production is off by default. When the backend role or the DBA needs a production fact (table volumes, a plan), it reads
`team.md` › Table volumes, then asks you: state it, run a read-only query it hands you, or let it connect read-only for that one
question. It connects only on that last answer, and the hook asks you again first. Backups by the DBA follow the same pattern.
Everything else in production becomes a runbook step for you. Only you merge.

## Standards the team follows

| Standard | Rule of thumb | File |
|---|---|---|
| Writing | Direct, affirmative, imperative; tables over prose; every block stands alone; decisions in docs, reasons in `log.md` | `references/writing-style.md` |
| Testing | Small (≤0.5 s, memory only) and Medium written before the code in a `red` commit; QA owns Large; DAMP; behaviour, not implementation; a test changes only when a source proves it wrong | `references/testing.md` |
| Diagrams | Mermaid: entity, class, sequence, state, activity; ASCII wireframes in pitches | `references/diagrams.md` |
| Messages | Board Log rows: NOTE, ASK, ANSWER, HANDOFF, BLOCK, FLAG, DECIDE, HUMAN, DONE; fixed turn report | `references/protocol.md` |

Paths are under `plugins/shapeup-team/skills/shapeup-team/`.

## What it creates in your repo

```
shape/
  team.md                  roles and their stack packs, commands per role and size, table volumes, versions, budgets
  stack/<role id>.md       house rules, when the repo differs from the pack
  ideas.md                 raw ideas, not a backlog
  decisions.md             conventions that outlive one pitch
  betting/<date>.md        betting pack for the founders
  pitches/<slug>/
    pitch.md               one page plus wireframes
    log.md                 audit trail: every decision and action
    board.md               scopes, hill, message log, QA findings
    tech.md                Mermaid diagrams and API contract
    runbook.md             manual ops for the release, when needed
```

## Repository layout

| Path | Holds |
|---|---|
| `.claude-plugin/marketplace.json` | The `shapeup` marketplace: the team and the stack packs |
| `plugins/shapeup-team/` | The team: Conductor skill (process, role files, gates, standards, templates, `scaffold.py`), the five commands, five agents, the guard hook |
| `plugins/stack-<name>/` | One stack pack each: `skills/stack-<name>/SKILL.md` and `references/sources.md` |
| `docs/` | Logo and the script that draws it (`python3 docs/make_logo.py` redraws the logo and the icon) |
| `tests/` | Guard behaviour tests |

## Develop

| Task | Command |
|---|---|
| Run the guard tests | `pytest -q tests` |
| Validate the marketplace and each plugin | `claude plugin validate .`, then `claude plugin validate plugins/<name>` |
| Lint a stack pack | `python3 plugins/shapeup-team/skills/shapeup-team/scripts/scaffold.py lint-pack plugins/stack-<name>` |
| Lint a pitch | `python3 plugins/shapeup-team/skills/shapeup-team/scripts/scaffold.py lint <repo> <slug>` |
| Add a stack pack to the marketplace | `/stack new <name>` with `plugins/` as the location, then add it to `marketplace.json` |

## Sources

| Source | Used for |
|---|---|
| [Shape Up](https://basecamp.com/shapeup), Basecamp | Shaping, appetite, betting, scopes, hill charts, circuit breaker |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Minimal-code ladder and code review |
| [Test sizes](https://testing.googleblog.com/2010/12/test-sizes.html), [The way of TDD](https://testing.googleblog.com/2026/03/the-way-of-tdd.html), [DAMP tests](https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html), [Change-detector tests](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html), Google Testing Blog | Testing standard |
| [The Elements of Style](https://www.gutenberg.org/ebooks/37134), Google and Microsoft style guides, plain-language guidelines | Writing standard |
| Each pack's `references/sources.md`: the official Django, DRF, Next.js, Chakra UI, Material UI, PostgreSQL and Cloud SQL docs | Stack packs |

## License

[MIT](LICENSE)
