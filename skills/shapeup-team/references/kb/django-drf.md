# KB: Django + DRF

Look things up here before guessing, and prefer the official docs for API details. Use `stable` URLs and
check the installed version in `shape/team.md`. Where a source conflicts with `roles/backend-drf.md`, the role file wins:
it is the house style.

## Official

| Source | URL | Use it for |
|---|---|---|
| Database access optimization | https://docs.djangoproject.com/en/stable/topics/db/optimization/ | The canonical ORM performance checklist |
| Performance and optimization | https://docs.djangoproject.com/en/stable/topics/performance/ | Profiling, caching, what to measure first |
| Query expressions / conditional expressions | https://docs.djangoproject.com/en/stable/ref/models/expressions/ | `F`, `Subquery`, `Exists`, `Case/When`: work in the DB |
| Constraints reference | https://docs.djangoproject.com/en/stable/ref/models/constraints/ | `CheckConstraint`, `UniqueConstraint` (conditions, `nulls_distinct`) |
| Transactions | https://docs.djangoproject.com/en/stable/topics/db/transactions/ | `atomic`, `on_commit`, savepoints |
| Writing migrations | https://docs.djangoproject.com/en/stable/howto/writing-migrations/ | Data migrations, non-atomic migrations, unique fields on existing rows |
| PostgreSQL-specific operations | https://docs.djangoproject.com/en/stable/ref/contrib/postgres/operations/ | `AddIndexConcurrently`, `RemoveIndexConcurrently` |
| Deployment checklist | https://docs.djangoproject.com/en/stable/howto/deployment/checklist/ | `manage.py check --deploy`, settings hardening |
| Release notes | https://docs.djangoproject.com/en/stable/releases/ | What changed in the installed version, deprecations |
| Supported versions | https://www.djangoproject.com/download/ | Support windows, Python/DB compatibility |
| DRF API guide | https://www.django-rest-framework.org/api-guide/ | Serializers, permissions, pagination, exceptions, testing |
| DRF testing | https://www.django-rest-framework.org/api-guide/testing/ | `APIClient`, force_authenticate |

## Patterns and style

| Source | URL | Use it for |
|---|---|---|
| HackSoft Django Styleguide | https://github.com/HackSoftware/Django-Styleguide | Service-function conventions, API/serializer layout, error handling. **Divergence:** our reads live in QuerySets (fat models), not in a selectors module. |
| Django Views — The Right Way (Luke Plant) | https://spookylukey.github.io/django-views-the-right-way/ | Thin views; the "thin views" chapter on where logic goes |
| Against service layers in Django (James Bennett) | https://www.b-list.org/weblog/2020/mar/16/no-service/ | The counter-argument. Use it to decide when a service is **not** needed (no pass-through services). |
| Classy DRF | https://www.cdrf.co/ | Every method and attribute of DRF generic views and viewsets, per version |
| Classy CBV | https://ccbv.co.uk/ | Same for Django class-based views |

## Performance, Postgres and the ORM

| Source | URL | Use it for |
|---|---|---|
| Haki Benita | https://hakibenita.com/ | Deep ORM + Postgres performance articles (bulk loads, indexes, concurrency) |
| Adam Johnson | https://adamj.eu/tech/ | Django tips, test speed, upgrades, security headers |
| Luke Plant — Django | https://lukeplant.me.uk/blog/categories/django/ | Pragmatic patterns, bulk properties, testing |
| django-zeal | https://github.com/taobojlen/django-zeal | Raise on N+1 in tests (Django-only, configurable threshold) |
| django-debug-toolbar | https://django-debug-toolbar.readthedocs.io/ | Seeing queries per request locally |

## Tooling (use only if installed, or propose through `HUMAN`)

| Source | URL | Use it for |
|---|---|---|
| drf-spectacular | https://drf-spectacular.readthedocs.io/ | OpenAPI 3 schema = the frontend-react contract |
| django-filter | https://django-filter.readthedocs.io/ | Declarative list filtering |
| pytest-django | https://pytest-django.readthedocs.io/ | Fixtures, `django_assert_num_queries` |
| factory_boy | https://factoryboy.readthedocs.io/ | Test data factories |
| django-upgrade | https://github.com/adamchainz/django-upgrade | Automated syntax upgrades between versions |
| Django Packages | https://djangopackages.org/ | Comparing packages before proposing one |
| awesome-django | https://github.com/wsvincent/awesome-django | Curated packages and resources |

## Security

| Source | URL | Use it for |
|---|---|---|
| OWASP DRF Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Django_REST_Framework_Cheat_Sheet.html | Default permissions, throttling, serializer field exposure, mass assignment |
| OWASP Django Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html | Settings, CSRF, cookies, headers |
| OWASP REST Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | Object-level authorisation (BOLA), input validation, rate limits |
| Django security releases | https://www.djangoproject.com/weblog/ | Patch-release announcements |
