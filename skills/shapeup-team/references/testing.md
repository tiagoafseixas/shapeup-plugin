# Testing standard

Applies to backend-drf, frontend-react and QA. Developers write Small and Medium tests before the code. QA owns Large tests.
Every test checks behaviour a user, an API client or a caller can observe.

## Sizes

| Size | Covers | May use | Never uses | Time per test | Data | Written by |
|---|---|---|---|---|---|---|
| Small | One function, class or component | Memory only | Database, files, network, threads, sleep, real clock, env vars | ≤0.5 s | 100% built in the test: fakes, stubs, value objects | backend-drf, frontend-react |
| Medium | Several functions or classes working together: service + model + serializer, view + permission, component + hook + API mock | The local test database, localhost | External systems: they are mocked at the boundary | ≤300 s | Mostly built in the test; rows created in the test database | backend-drf, frontend-react |
| Large | A whole journey of a user or an external API client through the running system: browser → web → API → DB | Everything real | Only external systems we must not touch (payments, email delivery, Google, NewsAPI, AI APIs): stubbed at the network edge | ≤900 s | Set up by the test through the API or fixtures | QA (developers may add one) |

Run each size with its own command from `team.md`. Put each test in the size's place in the repo (e.g. `<app>/tests/small/`).
A Django Small test subclasses `SimpleTestCase` (or has no `django_db` mark in pytest), so a database query fails the test.
A Small test over 0.5 s is moved to Medium or made faster. Find them with `python manage.py test --durations 20` or `pytest --durations=20`.

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
| The test fails and its expectation matches the source (Done when, Works when, tech.md API contract, a PO `ANSWER`) | Fix the code |
| The source says something else than the test | Fix the test. Add a `NOTE` row: test name, old expectation, new expectation, the source. Commit `S<n> <role>: fix test — <test>`. |
| No source covers the behaviour | `ASK` the PO. Leave the test failing and work on something else. |
| The test is a change detector (below) | Rewrite it to check behaviour, or delete it. Add a `NOTE` row naming it. |
| QA changes a developer's test | Same rules, and the `NOTE` row goes to the owner of the scope |

Deleting, skipping or loosening an assertion (`skip`, `xfail`, `.only`, a wider tolerance) counts as changing the test.

## Behaviour, not implementation

A test fails when behaviour breaks and passes through any refactor that keeps the behaviour.

| Check | Never check |
|---|---|
| Return values, raised errors, HTTP status and body | How many times an internal function ran, or with which arguments |
| Rows written to the test database, state of the object | The order in which collaborators were called |
| What the user sees and can do: text, roles, labels, enabled/disabled | Private methods, CSS classes, Chakra internals, component props |
| What reached an external boundary: the email in `mail.outbox`, the request a fake gateway received | Snapshots of logic or of whole components |
| Query count stays flat as rows grow (N+1 guard) | An exact number of queries that changes with any refactor |

Count calls only when the count is the behaviour a user would notice: "charged once", "one email sent".

```python
# Change detector: breaks on any refactor, catches no bug
def test_win_deal(self):
    with patch("deals.services.Deal.save") as save, patch("deals.services.notify") as notify:
        win_deal(deal, by=owner)
    save.assert_called_once()
    notify.assert_called_once_with(deal.id, "won")

# Behaviour
def test_owner_wins_open_deal(self):
    deal = DealFactory(owner=owner, outcome=None)
    win_deal(deal, by=owner)
    deal.refresh_from_db()
    self.assertEqual(deal.outcome, "won")
    self.assertEqual(len(mail.outbox), 1)
```

## DAMP: descriptive and meaningful phrases

Each test reads alone, top to bottom. Readability beats removing repetition.

| Rule | Do |
|---|---|
| Name | The behaviour and its condition: `test_other_user_gets_404_when_winning_a_deal`, `it("shows the empty state when there are no reviews")` |
| Data in the body | Create the values this test depends on inside the test. Factories and builders fill everything else with defaults. |
| Shared setup | Only plumbing the behaviour doesn't depend on: the API client, a logged-in user. Never the data under test. |
| One behaviour | One action, then the assertions about its outcome |
| No logic | No loops, conditionals or computed expected values. Write each assertion on its own line with a literal value. |
| Helpers | Build values (`DealFactory`, `make_review(...)`). Never hide the action or the assertion inside a helper. |

```python
# Too DRY: the data and the check live elsewhere
def test_ranking(self):
    for company in self.companies:
        self.assertIn(company.name, self.result_names())

# DAMP
def test_ranking_hides_companies_below_minimum_reviews(self):
    CompanyFactory(name="Acme", reviews=6)
    CompanyFactory(name="Tiny", reviews=5)
    names = rank_companies(goal="pay")
    self.assertIn("Acme", names)
    self.assertNotIn("Tiny", names)
```

## Sources

| Source | URL | Backs |
|---|---|---|
| Google Testing Blog: Test sizes (2010) | https://testing.googleblog.com/2010/12/test-sizes.html | Small/Medium/Large and what each may use |
| Google Testing Blog: The way of TDD (2026) | https://testing.googleblog.com/2026/03/the-way-of-tdd.html | Red → green → refactor |
| Testing on the Toilet: Tests too DRY? Make them DAMP (2019) | https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html | DAMP rules |
| Testing on the Toilet: Change-detector tests considered harmful (2015) | https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html | Behaviour, not implementation |
