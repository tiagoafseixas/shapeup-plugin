---
name: stack-django-drf
description: Stack pack for the shapeup-team plugin — Django + Django REST Framework backends with thin views, fat models and a service layer. Loaded by the backend-dev agent when the team config (team.md) › Roles names stack-django-drf. Also use it when writing or reviewing Django or DRF code in a repo set up by the shapeup-team plugin.
---

# Stack pack: Django + DRF

| Layer | Covers | Agent |
|---|---|---|
| backend | Django 5.x–6.x, DRF 3.15+, pytest-django or the Django test runner | backend-dev |

The role file says what to do and when (tests first, handoffs, gates); this pack says how, in this stack.
House rules in the repo (`<docs>/stack/<role id>.md`) win over this pack. Where this pack and the role file disagree on process, the role file wins.

## Version notes

| Version | Watch for |
|---|---|
| Django ≥5.0 | `db_default=` keeps a default in the database; use it for NOT NULL columns added to live tables |
| Django ≥5.1 | `CheckConstraint(condition=...)`; `check=` is deprecated |
| Django 6.x | Check the supported PostgreSQL majors in the release notes before upgrading either side |

## Layering: thin views, fat models, service layer

| Logic | Goes in | Never in |
|---|---|---|
| Shape and format of the input (types, required fields, lengths) | Input serializer | Model, view |
| Invariant of one row (amount ≥ 0, unique per owner) | DB constraint in `Meta.constraints`, plus `clean()` for messages | Serializer only |
| State change of one aggregate (`deal.mark_won()`) | Model method: pure, no I/O, raises a domain error | Service, view |
| Derived value from its own fields, no query | Model property | Serializer method |
| Reusable filter, annotation or read query | Custom `QuerySet` method (`objects = XQuerySet.as_manager()`) | View, service |
| Use case touching >1 model, a transaction, or a side effect (email, task, external API) | Service function in `<app>/services.py` | View, serializer `create()`, signal, `save()` |
| "Can this user do X to this object?" | DRF permission class (object-level), reusing QuerySet helpers | Service |
| HTTP: authenticate, authorise, parse, call one service or QuerySet, serialize | View / ViewSet | — |
| Background or scheduled work | Task that only calls a service | Task body |

Service rules:

- Plain functions named `<noun>_<verb>` (`deal_win`), keyword-only arguments, type hints, return model instances. Never take `request`.
- A service exists only for a real use case. No pass-through services (`deal_get`, `deal_list`): reads live on the QuerySet. Plain single-model CRUD with no rules may stay `ModelViewSet` + `ModelSerializer`.
- Open transactions in services (`transaction.atomic`). Put side effects in `transaction.on_commit`. Use `select_for_update()` when two requests can race on the same row.
- Raise domain exceptions (one `<App>Error` family). Map them to HTTP once, in the DRF exception handler, not in every view.
- No business logic in signals, `save()` overrides (except trivial normalisation), or serializer `create`/`update`.

```python
# models.py: fat, the invariants and state of one aggregate
class DealQuerySet(models.QuerySet):
    def open_for(self, user):
        return self.filter(owner=user, stage__in=Stage.OPEN)

class Deal(models.Model):
    objects = DealQuerySet.as_manager()
    class Meta:
        constraints = [models.CheckConstraint(condition=Q(amount__gte=0), name="deal_amount_gte_0")]
    def mark_won(self, *, at):
        if self.stage == Stage.WON:
            raise DealError("Deal already won")
        self.stage, self.closed_at = Stage.WON, at

# services.py: the use case
def deal_win(*, deal: Deal, by: User) -> Deal:
    with transaction.atomic():
        deal = Deal.objects.select_for_update().get(pk=deal.pk)
        deal.mark_won(at=timezone.now())
        deal.save(update_fields=["stage", "closed_at"])
        Activity.objects.create(deal=deal, kind=Activity.WON, by=by)
        transaction.on_commit(lambda: notify_deal_won.delay(deal.pk))
    return deal

# views.py: thin
class DealWinApi(APIView):
    permission_classes = [IsAuthenticated, CanEditDeal]
    def post(self, request, pk):
        deal = get_object_or_404(Deal.objects.open_for(request.user), pk=pk)
        self.check_object_permissions(request, deal)
        return Response(DealOutput(deal_win(deal=deal, by=request.user)).data)
```

## Rules

| Area | Rule |
|---|---|
| Serializers | Separate input and output serializers when the shapes differ (`DealWinInput`, `DealOutput`). Nested writes only if a service handles them. Explicit `fields`; never `__all__` on writes. |
| Ownership | Set ownership fields from `request.user` in `perform_create` or the service; never read them from the body |
| Permissions | Default `IsAuthenticated` in settings. Scope every queryset to the user or tenant in `get_queryset`, then add object-level permission classes. |
| Lists | Paginate every list (`DEFAULT_PAGINATION_CLASS`) and filter through django-filter if installed |
| Errors | Keep DRF's field-error format so the frontend can map errors to fields. Map domain errors in one exception handler. |
| Contract | Keep the OpenAPI schema (drf-spectacular, if installed) accurate; the tech.md API table is the contract |
| Migrations | `makemigrations`, then `sqlmigrate <app> <n>` for the DBA handoff. One schema concern per migration; data migrations separate and batched (`RunPython` with `atomic = False`, or a management command). Never edit a migration on the base branch; never squash during a cycle. |
| Postgres regex | `__regex` / `__iregex` run as Postgres regex: `\b` is a backspace there, the word boundary is `\y`. Test regex filters against Postgres, never SQLite. |

## Tests per size

| Size | Tool | How it enforces the size (testing.md) |
|---|---|---|
| Small | `SimpleTestCase`, or pytest without the `django_db` mark | Any database query raises, so a DB touch fails the test. List slow tests with `manage.py test --durations 20` or `pytest --durations=20`. |
| Medium | `TestCase` / `APITestCase`, or pytest with `django_db`; `APIClient`, factory_boy | Runs against the test database. `mail.outbox` captures email; mock HTTP clients (`responses`, `respx`) at the boundary. |
| Large | `LiveServerTestCase`, or the frontend pack's e2e tool against `runserver` | The whole API runs; stub only external systems at the network edge |

| Behaviour | Size |
|---|---|
| Model methods, validators, pure domain rules | Small |
| Services: happy path, each domain error, the side effect (row written, email in `mail.outbox`, task enqueued) | Medium |
| Constraints and custom querysets | Medium |
| API: permissions (owner, other user, anonymous), contract shape, errors, query count flat from 1 to N rows | Medium |

The testing standard's examples, in Django:

```python
# Change detector: breaks on any refactor, catches no bug
def test_win_deal(self):
    with patch("deals.services.Deal.save") as save, patch("deals.services.notify") as notify:
        deal_win(deal=deal, by=owner)
    save.assert_called_once()
    notify.assert_called_once_with(deal.id, "won")

# Behaviour, DAMP: the data this test depends on is in its body
def test_owner_wins_open_deal(self):
    deal = DealFactory(owner=owner, stage=Stage.OPEN)
    deal_win(deal=deal, by=owner)
    deal.refresh_from_db()
    self.assertEqual(deal.stage, Stage.WON)
    self.assertEqual(len(mail.outbox), 1)
```

## Performance

| Rule | How |
|---|---|
| No N+1 | `select_related` (FK/1:1), `prefetch_related` / `Prefetch` (M2M, reverse). Test that the query count stays the same for 1 and N rows (`assertNumQueries`, `django_assert_num_queries`), or django-zeal if installed. |
| Push work to the DB | `annotate`, `aggregate`, `Exists`, `Subquery`, `F()`. No Python loops over querysets to compute totals. |
| Write efficiently | `bulk_create`, `bulk_update`, `update()`, `save(update_fields=...)` |
| Read only what you need | `values()` / `only()` on hot paths, carefully: deferred fields trigger N+1 |
| Indexes | Propose them in `Meta.indexes` with the query they serve; the DBA approves them |
| Check the plan | `queryset.explain()` for any new query on a large table, pasted into the DBA handoff |

## Review checklist

| Finding | Sev |
|---|---|
| A queryset in a view or viewset not scoped to the user or tenant (BOLA) | `must` |
| Ownership field read from the request body, or `fields = "__all__"` on a write serializer | `must` |
| Business logic in a view, serializer `create`/`update`, signal or `save()` | `~` |
| A side effect outside `transaction.on_commit` inside a transaction | `~` |
| A list endpoint without pagination, or without a flat query-count test | `~` |
| A pass-through service (`deal_get`) | `~` |

## Sources

Indexed in `references/sources.md`: Django and DRF official docs first, then the community guides the rules above come from.
