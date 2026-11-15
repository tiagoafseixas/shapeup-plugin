# KB: PostgreSQL + GCP Cloud SQL

Use the docs for the Postgres major in `shape/team.md` (replace `current` in the URL with the version number when they differ).

## PostgreSQL

| Source | URL | Use it for |
|---|---|---|
| Explicit locking | https://www.postgresql.org/docs/current/explicit-locking.html | Which DDL takes which lock, and what each lock blocks |
| ALTER TABLE notes | https://www.postgresql.org/docs/current/sql-altertable.html | Which forms rewrite the table, `NOT VALID` / `VALIDATE` |
| Using EXPLAIN | https://www.postgresql.org/docs/current/using-explain.html | Reading plans, `ANALYZE`, `BUFFERS` |
| Indexes | https://www.postgresql.org/docs/current/indexes.html | Types, partial, expression, multicolumn, index-only scans |
| Routine vacuuming | https://www.postgresql.org/docs/current/routine-vacuuming.html | Bloat, autovacuum tuning, wraparound |
| Versioning policy | https://www.postgresql.org/support/versioning/ | EOL dates for the instance's major |
| Don't Do This (wiki) | https://wiki.postgresql.org/wiki/Don%27t_Do_This | Type and feature anti-patterns |
| Use The Index, Luke | https://use-the-index-luke.com/ | Index design from first principles, keyset pagination |

## Zero-downtime migrations

| Source | URL | Use it for |
|---|---|---|
| Squawk | https://squawkhq.com/ | Linting the SQL from `sqlmigrate` for lock and rewrite risks |
| django-pg-zero-downtime-migrations | https://github.com/tbicr/django-pg-zero-downtime-migrations | Safe-by-default schema editor (lock timeouts, NOT VALID patterns) |
| django-migration-linter | https://github.com/3YOURMIND/django-migration-linter | Flags backward-incompatible migrations |
| GoCardless: zero-downtime migrations, the hard parts | https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/ | Lock queues, why `lock_timeout` matters |
| Citus: tips for Postgres locks | https://www.citusdata.com/blog/2018/02/22/seven-tips-for-dealing-with-postgres-locks/ | Practical lock-safe DDL patterns |

## Cloud SQL for PostgreSQL

| Source | URL | Use it for |
|---|---|---|
| General best practices | https://cloud.google.com/sql/docs/postgres/best-practices | Instance, data, app and backup practices from Google |
| Manage database connections | https://cloud.google.com/sql/docs/postgres/manage-connections | Pooling, limits, backoff |
| Managed Connection Pooling | https://cloud.google.com/sql/docs/postgres/managed-connection-pooling | Built-in pooler: modes, ports, prepared statements, edition limits |
| Database flags | https://cloud.google.com/sql/docs/postgres/flags | Supported flags (`pg_stat_statements`, timeouts, logging) |
| Query Insights | https://cloud.google.com/sql/docs/postgres/using-query-insights | Finding slow queries in prod |
| Backups / PITR | https://cloud.google.com/sql/docs/postgres/backup-recovery/backups | Automated and on-demand backups, point-in-time recovery |
| Cloud SQL Auth Proxy | https://cloud.google.com/sql/docs/postgres/sql-proxy | Secure connections without IP allowlists |
| Cloud SQL Python Connector | https://github.com/GoogleCloudPlatform/cloud-sql-python-connector | In-process connector, IAM auth |
| IAM database authentication | https://cloud.google.com/sql/docs/postgres/iam-authentication | Passwordless DB users |
| In-place major upgrade | https://cloud.google.com/sql/docs/postgres/upgrade-major-db-version-inplace | Upgrading the Postgres major |

## Blogs worth searching

| Source | URL | Use it for |
|---|---|---|
| Crunchy Data blog | https://www.crunchydata.com/blog | Postgres operations, performance, new features |
| pganalyze blog | https://pganalyze.com/blog | Query plans, indexing, "5mins of Postgres" deep dives |
| Haki Benita | https://hakibenita.com/ | Postgres from a Django developer's angle |
