# Team config — {{product}}

## Roles

One row per developer role and one for the database. The agent does the work; the stack pack tells it how in this stack.
Add a row for each extra stack (a second backend, a mobile app). Paths are relative to this repo.

| Role id | Agent | Stack pack | Path |
|---|---|---|---|
| <backend-drf> | backend-dev | <stack-django-drf> | <backend/> |
| <frontend-react> | frontend-dev | <stack-nextjs-chakra, stack-react-mui> | <frontend/, or ../<web-repo> when it's a separate repo> |
| <database> | dba | <stack-postgres-cloudsql> | — |

House rules per role, when the repo has its own conventions: `shape/stack/<role id>.md`.

## Commands

| Command | Run |
|---|---|
| <backend-drf> Small tests | <cd backend && pytest -q */tests/small --durations=10> |
| <backend-drf> Medium tests | <cd backend && pytest -q */tests/medium> |
| <backend-drf> lint | <cd backend && ruff check .> |
| <backend-drf> migrations check | <cd backend && python manage.py makemigrations --check --dry-run> |
| <frontend-react> Small tests | <cd frontend && npm test -- --run small> |
| <frontend-react> Medium tests | <cd frontend && npm test -- --run medium> |
| <frontend-react> lint + build | <cd frontend && npm run lint && npm run build> |
| Large tests | <cd frontend && npx playwright test> · <API journeys command> |
| Local DB | <docker compose up -d db> |

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
| Budget Big batch | 20 rounds |
| Ponytail level | full |
| Model: tech check, ideas, PO build, uphill dev turn, QA gates | sonnet |
| Model: mechanical turn (downhill, fully specified) | haiku |
| Model: DBA review and runbooks | opus |
| PR reviewers | <github logins> |
