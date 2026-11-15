# Team config — {{product}}

| Key | Value |
|---|---|
| Product | {{product}} |
| Base branch | <main> |
| Remote | <origin> |
| Backend path | <backend/> |
| Frontend path | <frontend/, or ../<web-repo> when the frontend is a separate repo> |
| Backend Small tests | <cd backend && pytest -q backend/*/tests/small> |
| Backend Medium tests | <cd backend && pytest -q backend/*/tests/medium> |
| Backend lint | <cd backend && ruff check . && ruff format --check .> |
| Migrations check | <cd backend && python manage.py makemigrations --check --dry-run> |
| Frontend Small tests | <cd frontend && npm test -- --run small> |
| Frontend Medium tests | <cd frontend && npm test -- --run medium> |
| Frontend lint + build | <cd frontend && yarn lint && yarn build> |
| Large tests | <cd frontend && yarn cypress run> · <API journeys command> |
| Local DB | <docker compose up -d db> |
| Versions | <Python 3.x · Django x.y · DRF x.y · Next.js x · React x · Chakra UI x · Postgres x on Cloud SQL (edition)> |
| Prod DB instance | <project:region:instance> |
| Read-only DB access | <user agent_ro on <replica or primary>; the CTO sets READONLY_DATABASE_URL in the session on request> |
| Budget Small batch | 8 rounds |
| Budget Big batch | 20 rounds |
| Ponytail level | full |
| Model: tech check, ideas, PO build, uphill dev turn, QA gates | sonnet |
| Model: mechanical turn (downhill, fully specified) | haiku |
| Model: DBA review and runbooks | opus |
| PR reviewers | <github logins> |
