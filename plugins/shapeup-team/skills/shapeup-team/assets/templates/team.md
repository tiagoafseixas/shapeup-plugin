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
| <devops-<platform>: devops-gcp, …> | devops | <stack-<name>: stack-gcp-devops, …> | <infra/> (optional row: without it, delivery files stay with the developers and releases with the DBA) |

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
| <devops role id> IaC check | <format + validate + lint of the infrastructure code, no network> |
| <devops role id> pipeline check | <lint of the CI config and the Dockerfile> |
| <devops role id> image build | <how the deployable artifact builds locally> |

## Services

What runs in production and how critical each part is. DevOps reads it at the start of every turn; the tier decides how carefully a
change is released. The user sets the tiers; agents add a row when a pitch adds a service or job, and ask the user for its tier.

| Tier | Means | Default availability target |
|---|---|---|
| 0 | Everything else depends on it: identity, the database, the network, the pipeline | 99.99% |
| 1 | Customer-facing: users or money stop when it stops | 99.95% |
| 2 | Business systems: staff work around it for a few hours | 99.9% |
| 3 | Internal tools, batch work that can wait or be re-run | 99% |

| Service or job | Tier | SLO (overrides the default) | Data it holds | Owner role |
|---|---|---|---|---|
| <api> | <1> | <99.95% availability, p95 < 500 ms> | <personal data / none> | <backend-drf> |

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
| Reviews Small batch | 2 |
| Pitch word limit | 600 |
| Scopes per pitch | 2–7 |
| Small test time limit | 0.5 s |
| PR tool | <gh, glab, or none (the user opens PRs)> |
| Branch pattern | cycle/<cycle>-<slug> |
| Reviews Big batch | 6 |
| Turn cap per round | 30 |
| Ponytail level | full |
| Model: tech check, ideas, Shaper build, uphill dev turn, QA gates | sonnet |
| Model: mechanical turn (downhill, fully specified) | haiku |
| Model: DBA review and runbooks | opus |
| PR reviewers | <github logins> |
| Staging target | <the Cloud Deploy target DevOps may promote to, or none> |
| Staging project | <the cloud project DevOps may deploy to and read without asking, or none; never the production project> |
| Production project | <the production cloud project; staging promotes are off when it equals the staging project> |
