# KB: Testing and review

The team's rules (sizes, test first, DAMP, change detectors) are in `references/testing.md`. These sources back the tools.

| Source | URL | Use it for |
|---|---|---|
| Ponytail (review and audit) | https://github.com/DietrichGebert/ponytail | `/ponytail-review` (a change, reading the connected code) and `/ponytail-audit` (whole repo), ranked must / should / nice |
| Testing Library: guiding principles | https://testing-library.com/docs/guiding-principles | Test what the user sees, not implementation |
| Testing Library: query priority | https://testing-library.com/docs/queries/about/#priority | `getByRole` > `getByLabelText` > … > test id |
| Cypress best practices | https://docs.cypress.io/app/core-concepts/best-practices | Selectors, isolation, no arbitrary waits |
| Playwright best practices | https://playwright.dev/docs/best-practices | Isolation, locators, web-first assertions |
| Playwright locators | https://playwright.dev/docs/locators | Role and label locators that survive UI changes |
| Vitest | https://vitest.dev/guide/ | Unit/component runner (if the repo uses it) |
| MSW | https://mswjs.io/docs/ | Mocking the API at the network level in frontend-react tests |
| pytest-django | https://pytest-django.readthedocs.io/ | DB access, `django_assert_num_queries`, client fixtures |
| DRF testing | https://www.django-rest-framework.org/api-guide/testing/ | `APIClient`, authentication in tests |
| OWASP Web Security Testing Guide | https://owasp.org/www-project-web-security-testing-guide/ | Exploratory security checks (authz, input handling) |
| Martin Fowler: Test Pyramid | https://martinfowler.com/articles/practical-test-pyramid.html | Why so few e2e tests: where each kind of test belongs |
