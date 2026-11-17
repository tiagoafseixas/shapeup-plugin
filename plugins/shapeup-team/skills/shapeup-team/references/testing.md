# Testing standard

Applies to the backend and frontend roles and QA. Developers write Small and Medium tests before the code. QA owns Large tests.
Every test checks behaviour a user, an API client or a caller can observe.

## Sizes

| Size | Covers | May use | Never uses | Time per test | Data | Written by |
|---|---|---|---|---|---|---|
| Small | One function, class or component | Memory only | Database, files, network, threads, sleep, real clock, env vars | ≤ `team.md` › Small test time limit (default 0.5 s) | 100% built in the test: fakes, stubs, value objects | backend-drf, frontend-react |
| Medium | Several functions or classes working together: service + model + input schema, handler + permission, component + hook + API mock | The local test database, localhost | External systems: they are mocked at the boundary | ≤300 s | Mostly built in the test; rows created in the test database | backend-drf, frontend-react |
| Large | A whole journey of a user or an external API client through the running system: browser → web → API → DB | Everything real | Only external systems we must not touch (payments, email delivery, Google, NewsAPI, AI APIs): stubbed at the network edge | ≤900 s | Set up by the test through the API or fixtures | QA (developers may add one) |

Run each size with its own command from `team.md`. Put each test in the size's place in the repo (e.g. `<app>/tests/small/`).
Make a database access fail inside a Small test, and list the slowest tests on every run: each stack pack says how (Tests per size).
A Small test over the limit is moved to Medium or made faster.

## Test first (red → green → refactor)

| # | Step | Evidence |
|---|---|---|
| 1 | List the behaviours of this turn from "Done when", the API contract in tech.md, and the pitch | Behaviours named in the turn report |
| 2 | **Red**: write the Small and Medium tests for those behaviours. Add only the stubs (signatures) needed for them to run. Run them: each fails on its assertion, never on an import or setup error. | Commit `S<n> <role>: red — <behaviour>` |
| 3 | **Green**: write the least code that makes them pass | All sizes of your side green |
| 4 | **Refactor**: clean the code with the tests green and unchanged | Commit `S<n> <role>: <what>` |
| 5 | Hand off: list the new user journeys in the dev → QA `HANDOFF`, so QA can write the Large tests | Board row |

Code without behaviour needs no new test: settings, a schema-only migration, copy changes.
Before the red commit, tests are drafts. After it, the change rule below applies.

## Changing a test

A failing test means the code is wrong until a source proves the test wrong. Never edit a test to make it pass.

| Situation | Do |
|---|---|
| The test fails and its expectation matches the source (Done when, Works when, tech.md API contract, a Shaper `ANSWER`) | Fix the code |
| The source says something else than the test | Fix the test. Add a `NOTE` row: test name, old expectation, new expectation, the source. Commit `S<n> <role>: fix test — <test>`. |
| No source covers the behaviour | `ASK` the Shaper. Leave the test failing and work on something else. |
| The test is a change detector (below) | Rewrite it to check behaviour, or delete it. Add a `NOTE` row naming it. |
| QA changes a developer's test | Same rules, and the `NOTE` row goes to the owner of the scope |

Deleting, skipping or loosening an assertion (`skip`, `xfail`, `.only`, a wider tolerance) counts as changing the test.

## Behaviour, not implementation

A test fails when behaviour breaks and passes through any refactor that keeps the behaviour.

| Check | Never check |
|---|---|
| Return values, raised errors, HTTP status and body | How many times an internal function ran, or with which arguments |
| Rows written to the test database, state of the object | The order in which collaborators were called |
| What the user sees and can do: text, roles, labels, enabled/disabled | Private methods, CSS classes, UI-library internals, component props |
| What reached an external boundary: the email in the test mail outbox, the request a fake gateway received | Snapshots of logic or of whole components |
| Query count stays flat as rows grow (N+1 guard) | An exact number of queries that changes with any refactor |

Count calls only when the count is the behaviour a user would notice: "charged once", "one email sent".

Examples are pseudo-code; each stack pack shows them in its language.

```text
# Change detector: breaks on any refactor, catches no bug
test "win deal":
    replace Deal.save and notify with mocks
    winDeal(deal, by: owner)
    expect Deal.save called once
    expect notify called with (deal.id, "won")

# Behaviour
test "owner wins an open deal":
    deal = a deal owned by owner, with no outcome
    winDeal(deal, by: owner)
    expect the deal, reloaded from the database, to have outcome "won"
    expect one email in the test outbox
```

## DAMP: descriptive and meaningful phrases

Each test reads alone, top to bottom. Readability beats removing repetition.

| Rule | Do |
|---|---|
| Name | The behaviour and its condition: "other user gets 404 when winning a deal", "shows the empty state when there are no invoices" |
| Data in the body | Create the values this test depends on inside the test. Factories and builders fill everything else with defaults. |
| Shared setup | Only plumbing the behaviour doesn't depend on: the API client, a logged-in user. Never the data under test. |
| One behaviour | One action, then the assertions about its outcome |
| No logic | No loops, conditionals or computed expected values. Write each assertion on its own line with a literal value. |
| Helpers | Build values (a factory or builder: "an invoice due 10 days ago"). Never hide the action or the assertion inside a helper. |

```text
# Too DRY: the data and the check live elsewhere
test "overdue list":
    for each invoice in sharedFixture.invoices:
        expect overdueList() to contain invoice.number

# DAMP
test "overdue list leaves out invoices paid today":
    an invoice "INV-1", due 10 days ago, unpaid
    an invoice "INV-2", due 10 days ago, paid today
    numbers = overdueList()
    expect numbers to contain "INV-1"
    expect numbers not to contain "INV-2"
```

## Sources

| Source | URL | Backs |
|---|---|---|
| Google Testing Blog: Test sizes (2010) | https://testing.googleblog.com/2010/12/test-sizes.html | Small/Medium/Large and what each may use |
| Google Testing Blog: The way of TDD (2026) | https://testing.googleblog.com/2026/03/the-way-of-tdd.html | Red → green → refactor |
| Testing on the Toilet: Tests too DRY? Make them DAMP (2019) | https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html | DAMP rules |
| Testing on the Toilet: Change-detector tests considered harmful (2015) | https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html | Behaviour, not implementation |
