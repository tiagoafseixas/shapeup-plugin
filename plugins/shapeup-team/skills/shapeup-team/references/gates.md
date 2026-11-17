# Gates

A gate passes when every row is ✓. Whoever runs the gate appends the result to the pitch's `log.md`
(kind `gate`): `<Gate name>: pass`, or `<Gate name>: fail on rows 2, 5: <one clause each>`.

## Bootstrap gate (Conductor + user, once per repo, offline)

Bootstrap only reads files and asks the user. No network, no database, no test runs, no installs (SKILL.md › Offline until kickoff).

| # | Check | How |
|---|---|---|
| 0 | `.shapeup.json` names the docs folder the user confirmed | read it |
| 1 | `<docs>/team.md` filled: no `<…>` left | read the repo's files (`package.json`, `requirements*.txt`, `pyproject.toml`, settings, CI config); ask the user what files can't tell |
| 2 | Every row in `team.md` › Roles names a stack pack that's installed (or written with `/stack new`) | load each pack with the Skill tool |
| 3 | `team.md` › Table volumes lists the largest tables (rows, size), as the user gave them, or says "ask per pitch" | ask the user |
| 4 | No production credentials in the repo (`.env*`, config files) | grep the repo's files for connection strings; report file paths, never values |
| 5 | Ponytail plugin installed | if missing, give the user the install command (`/plugin install ponytail@ponytail`); don't install it |

## Ready gate (PO, before a pitch goes to the betting table)

| # | Check |
|---|---|
| 1 | Problem: baseline → workaround → cost, no solution words (`roles/po.md` › Writing the problem); its evidence is logged in log.md |
| 2 | Appetite: size in the header table (rounds from `team.md`); one imperative sentence on what the bet builds |
| 3 | Solution: the elements are concrete enough to start, rough enough to leave design room |
| 4 | Wireframes: present when a screen is new or changes layout, at fat-marker level |
| 5 | Every rabbit hole has a patch, or has become a no-go |
| 6 | No-gos listed explicitly |
| 7 | Tech check logged in log.md whenever the pitch touches the schema, a new integration or a new library; its risks are in Rabbit holes |
| 8 | Works when: 3–5 outcomes a user can observe |
| 9 | ≤600 words outside code blocks (wireframes excluded). Passes the final check in `writing-style.md`. No task lists. |
| 10 | log.md records the shaping decisions taken with the user |
| 11 | `scaffold.py lint <repo> <slug>` is clean |
| 12 | The pitch stands alone: no other pitch named, no justifications (they live in log.md) |

## Kickoff gate (Conductor)

| # | Check |
|---|---|
| 1 | Branch exists and is pushed; draft PR is open |
| 2 | 2–7 scopes, each a vertical slice named in ≤5 domain words |
| 3 | Each scope has an owner, must or `~`, and a "Done when" written by QA |
| 4 | DBA has marked the scopes that touch the schema |
| 5 | PO confirmed: every scope traces back to the pitch, and no no-go appears |
| 6 | The first scope is the most core and the most unknown |
| 7 | tech.md exists if any scope touches the schema (Entities) or adds an endpoint (Flows + API contract), with sections that don't apply deleted |
| 8 | `scaffold.py lint <repo> <slug>` is clean |
| 9 | First run of the environment, now that the cycle starts: `gh auth status` OK and the remote reachable; the local or test database (same engine and major as production) runs the migrations; the Small and Medium test commands in `team.md` run green on the base branch | run them; a failure is a `HUMAN` row, not a fix |

## Scope gate (QA, per scope)

| # | Check | How |
|---|---|---|
| 1 | Every "Done when" item verified | run it, or test it by hand; one QA row per item that fails |
| 2 | Small and Medium tests, lint and typecheck green; no Small test over 0.5 s | commands in `team.md`, with `--durations` |
| 3 | Large tests for the scope's journeys written and green | QA |
| 4 | Developer tests pass the review in `roles/qa.md`: written first, behaviour not implementation, DAMP, sizes respected, every test change cites its source | git log, the tests, board Log |
| 5 | Code review done | `/ponytail-review` on the scope's commits; its `must fix` items become QA rows |
| 6 | Edge cases tried: empty, zero, max, another user's object, unauthenticated, double submit | by hand or with tests |
| 7 | List endpoints have a test that the query count stays flat as rows grow | read the tests |
| 8 | Every migration has a DBA `approve` | board Log |
| 9 | No no-go was built | compare against pitch.md |
| 10 | tech.md diagrams and the API contract match the scope's code | read both |
| 11 | No open `must` QA rows for this scope | QA table |

Pass → QA writes `DONE` and sets Hill to 100.

## Ship gate (QA, then the Conductor)

| # | Check | How |
|---|---|---|
| 1 | All must scopes are DONE | Scopes table |
| 2 | Small, Medium and Large tests, lint and typecheck green on the branch | `team.md` commands |
| 3 | `/ponytail-review` on the whole branch vs the base: no `must fix` left | run it |
| 4 | `makemigrations --check` clean; migrations apply from zero on an empty DB | run them |
| 5 | runbook.md written if the release needs manual ops; otherwise the PR body says "No ops" | DBA |
| 6 | tech.md matches the branch; log.md has every decision, cut and gate result | read both |
| 7 | PR body updated from the board: shipped, cut, risks | Conductor |
| 8 | No `open` rows on the board | board Log |
| 9 | `scaffold.py lint <repo> <slug>` is clean | run it |
