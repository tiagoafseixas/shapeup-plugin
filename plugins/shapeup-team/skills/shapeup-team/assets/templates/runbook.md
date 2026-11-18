# Runbook — {{title}}

| Release | Owner | Downtime | Duration | Prod instance |
|---|---|---|---|---|
| PR <#> | user runs · DBA and DevOps wrote | <none or n min> | <~n min> | <project:region:instance> |

Every step: one command, what you should see, what to do if not. Step 1 is a backup when data changes.

## Release (DevOps; delete when infrastructure, config and secrets don't change)

| Strategy | Success metrics: what, where, how long | Roll back when | Cost change |
|---|---|---|---|
| <rolling · canary n% · blue/green · flag> | <error rate, p95 latency, SLO burn on <dashboard>, for <n> min> | <threshold> | <€/month, or none> |

## Before

| # | Check | Command | You should see |
|---|---|---|---|

## Steps

| # | Step | Command / action | You should see | If not |
|---|---|---|---|---|

## Rollback

| # | Step | Command / action | You should see | If not |
|---|---|---|---|---|
