# Team config — {{product}}

## Roles

One row per developer role and one for the database. The agent does the work; the stack pack tells it how in this stack.
Add a row for each extra stack (a second backend, a mobile app). Paths are relative to this repo.

| Role id | Agent | Stack pack | Path |
|---|---|---|---|
| <backend-<stack>: backend-drf, backend-spring, …> | backend-dev | <stack-<name>: stack-django-drf, …> | <backend/> |
| designer | designer | <the frontend role's pack> | <the frontend path> (optional row: without it, the frontend role designs) |
| <frontend-<stack>: frontend-react, …> | frontend-dev | <stack-<name>: stack-react-mui, stack-nextjs-chakra, …> | <frontend/, or ../<web-repo> when it's a separate repo> |
| <database> | dba | <stack-<name>: stack-postgres-cloudsql, …> | — |

House rules per role, when the repo has its own conventions: `<docs>/stack/<role id>.md`.

## Commands

| Command | Run |
|---|---|
| <backend role id> Small tests | <the command that runs this role's Small tests, as the repo runs them> |
| <backend role id> Medium tests | <…> |
| <backend role id> lint | <…> |
| <backend role id> migrations check | <the command that fails when a model change has no migration> |
| <frontend role id> Small tests | <…> |
| <frontend role id> Medium tests | <…> |
| <frontend role id> lint + build | <…> |
| Large tests | <the e2e command> · <API journeys command> |
| Local DB | <how a local database runs> |

## Table volumes

Production sizes the backend role and the DBA plan migrations and queries against. The user fills this in; agents add a row
when the user answers a volume question. Agents never connect to production to fill it.

| Table | Rows | Size | Growth | As of | Source |
|---|---|---|---|---|---|
| <largest tables first, or "ask per pitch"> | <≈4.2M> | <≈3 GB> | <≈50k rows/month> | <date> | <user / read-only query> |

## Settings

| Key | Value |
|---|---|
| Product | {{product}} |
| Base branch | <main> |
| Remote | <origin> |
| Versions | <runtime and framework majors per role, database engine and major> |
| Prod DB instance | <identifier the database pack's commands take> |
| Read-only DB access | <none, or: read-only user on <replica or primary>; the user sets READONLY_DATABASE_URL in the session when they allow a connection> |
| Budget Small batch | 8 rounds |
| Pitch word limit | 600 |
| Scopes per pitch | 2–7 |
| Small test time limit | 0.5 s |
| PR tool | <gh, glab, or none (the user opens PRs)> |
| Branch pattern | cycle/<cycle>-<slug> |
| Budget Big batch | 20 rounds |
| Ponytail level | full |
| Model: tech check, ideas, Shaper build, uphill dev turn, QA gates | sonnet |
| Model: mechanical turn (downhill, fully specified) | haiku |
| Model: DBA review and runbooks | opus |
| PR reviewers | <github logins> |
