---
name: stack-postgres-cloudsql
description: Stack pack for the shapeup-team plugin — PostgreSQL on Google Cloud SQL, with zero-downtime migration patterns (Django operations included), read-only access and on-demand backups. Loaded by the dba agent when shape/team.md › Roles names stack-postgres-cloudsql. Also use it when reviewing migrations or query plans for Postgres in a repo with a shape/ folder.
---

# Stack pack: PostgreSQL on GCP Cloud SQL

| Layer | Covers | Agent |
|---|---|---|
| database | PostgreSQL 13–18 on Cloud SQL (Enterprise and Enterprise Plus) | dba |

The role file says what to do and when (review every migration, backups only, runbooks); this pack says how, in this stack.
House rules in the repo (`shape/stack/<role id>.md`) win over this pack. Where this pack and the role file disagree on process, the role file wins.

## Commands the role file refers to

| Action | Command |
|---|---|
| On-demand backup | `gcloud sql backups create --instance=<instance> --description="<slug>: before <step>"` |
| Confirm the backup | `gcloud sql backups list --instance=<instance> --limit=1` (status `SUCCESSFUL`, id, end time) |
| Read-only check | `SELECT current_user, current_setting('transaction_read_only');` returns the read-only user and `on` |

Read-only user setup, once per instance, as a runbook for the user. Cloud SQL's `cloudsqlsuperuser` runs the grants:

```sql
-- gcloud sql users create agent_ro --instance=<instance> --password=<secret>
GRANT CONNECT ON DATABASE <db> TO agent_ro;
GRANT USAGE ON SCHEMA public TO agent_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO agent_ro;
ALTER DEFAULT PRIVILEGES FOR ROLE <app_owner> IN SCHEMA public GRANT SELECT ON TABLES TO agent_ro;
GRANT pg_monitor TO agent_ro;                                 -- pg_stat_statements, pg_stat_activity
ALTER ROLE agent_ro SET default_transaction_read_only = on;   -- second belt; the grants are the real guard
ALTER ROLE agent_ro SET statement_timeout = '60s';
ALTER ROLE agent_ro CONNECTION LIMIT 2;
```

Point it at a read replica when one exists. The grants make it safe: a session can switch off `default_transaction_read_only`, but it can't gain write privileges.
In production, `EXPLAIN` only; never `EXPLAIN ANALYZE` on a statement that writes.

## Migration review

Read the SQL of each migration (`sqlmigrate` in Django) and lint it with `squawk` if available. Judge it against the size the table has in production, not in the test DB.

| Change | Risk on a big table | Safe pattern | In Django |
|---|---|---|---|
| Add a nullable column, or one with a constant default | none on PG ≥11 | Plain `ADD COLUMN` | `AddField` |
| Add a NOT NULL column with a default | Django drops the DB default right after adding it, so old app instances fail during a rolling deploy | Keep the default in the database | `db_default=` (Django ≥5.0), or nullable |
| Add a column with a computed default (`uuid4`, `now`) | Django computes it once: every existing row gets the same value; a unique column fails | Nullable → backfill in batches → constraint | Docs: "Migrations that add unique fields" |
| `SET NOT NULL` on an existing column | Full scan under ACCESS EXCLUSIVE | `CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE CONSTRAINT` → `SET NOT NULL` (PG ≥12 skips the scan) → drop the check | `RunSQL` + `SeparateDatabaseAndState` |
| Create an index | Blocks writes while it builds | `CREATE INDEX CONCURRENTLY` | `AddIndexConcurrently`, migration `atomic = False` |
| Add a unique constraint | Blocks writes while it builds | Unique index concurrently → `ADD CONSTRAINT … UNIQUE USING INDEX` | `RunSQL` + `SeparateDatabaseAndState` |
| Add a foreign key | Validates both tables under locks | `NOT VALID` → `VALIDATE CONSTRAINT` in a separate migration | Mind the auto-created FK index (not concurrent) |
| Change a column type | Table rewrite under ACCESS EXCLUSIVE (except varchar→text, widening varchar) | New column → dual write → backfill → switch reads → drop the old one later | Expand/contract across releases |
| Rename a column or table | Old code still running breaks during the deploy | Expand/contract across two releases | Or `db_column` to keep the physical name |
| Drop a column | Old code still selects it during the deploy | Release 1: stop using it (nullable). Release 2: drop it. | Two migrations, two releases |
| Data backfill | Long transaction, locks, bloat, WAL spike | Batches of 1–10k rows by PK, idempotent, outside the deploy when big (runbook) | Management command or `RunPython`, `atomic = False` |
| Any DDL on a busy table | Lock queue: one waiting ALTER blocks every read behind it | `SET lock_timeout = '5s'` before the DDL, retry on timeout | `RunSQL` |

## Rules

| Area | Rule |
|---|---|
| Types | `bigint` PKs, `timestamptz`, `text` + CHECK rather than `varchar(n)`, `numeric` for money (Postgres wiki "Don't Do This") |
| Indexes | Only for a named query, verified with `EXPLAIN (ANALYZE, BUFFERS)` on realistic volume. Composite: equality columns first, then range or sort. Partial indexes for hot subsets. |
| Queries | No unbounded `IN (…)` lists; keyset pagination, not `OFFSET`, on large tables |
| Regex | The word boundary is `\y`; `\b` is a backspace, so `notes ~* '^WON\b'` silently matches nothing |
| Connections | App instances × workers × persistent connections ≤ ~80% of `max_connections`. Managed Connection Pooling where the edition has it, PgBouncer otherwise. |
| Transaction pooling | `DISABLE_SERVER_SIDE_CURSORS = True` in Django. No session state (`SET` without `LOCAL`, session advisory locks, `LISTEN`). |
| Access | Private IP, Cloud SQL Python Connector or Auth Proxy, IAM database auth where possible. No public IP without authorised networks. |
| Safety | Automated backups and PITR on; deletion protection on; on-demand backup as step 1 of any risky runbook |
| Operations | Short transactions; know the maintenance window; ≥20% free storage if auto-increase is off; test major upgrades on a clone first |
| Compatibility | Check the backend framework supports the Postgres major (Django 6.1 dropped PostgreSQL 14) |

## Tests per size

| Size | Tool | How it enforces the size (testing.md) |
|---|---|---|
| Small | — | Database code has no Small tests |
| Medium | The backend's test database on the same Postgres major as production (Docker `postgres:<major>`) | Never SQLite for queries, constraints or regex: behaviour differs |
| Large | A staging copy, never production | Migrations rehearsed on production-sized data before a risky release |

## Performance

| Rule | How |
|---|---|
| Find slow queries first | `pg_stat_statements` and Query Insights, through the read-only user |
| Read plans | `EXPLAIN (ANALYZE, BUFFERS)` on staging-sized data; check row estimates against actuals |
| Keep tables healthy | Watch autovacuum on hot tables; bloat after large backfills |

## Review checklist

| Finding | Sev |
|---|---|
| A non-concurrent index, a type change or `SET NOT NULL` on a large table | `must` |
| A NOT NULL column added with `default=` instead of `db_default=` | `must` |
| A backfill inside a schema migration on a large table | `must` |
| An index with no named query or plan behind it | `should` |
| DDL on a busy table without `lock_timeout` | `should` |

## Sources

Indexed in `references/sources.md`: PostgreSQL docs for locks, ALTER TABLE, EXPLAIN and indexes; Cloud SQL docs for backups, connections and pooling; migration-safety guides.
