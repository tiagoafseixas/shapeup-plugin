# Sources: DevOps on Google Cloud

Google Cloud's docs moved to `docs.cloud.google.com`; `cloud.google.com/...` links redirect there.

## Certification

| Source | URL | Use it for |
|---|---|---|
| Professional Cloud DevOps Engineer exam guide | https://services.google.com/fh/files/misc/professional_cloud_devops_engineer_exam_guide_english.pdf | The five sections this pack follows (`exam-guide.md`) |

## Delivery

| Source | URL | Use it for |
|---|---|---|
| Cloud Build: use secrets from Secret Manager | https://docs.cloud.google.com/build/docs/securing-builds/use-secrets | `availableSecrets`, `secretEnv`, `$$NAME` |
| Cloud Deploy: canary strategy | https://docs.cloud.google.com/deploy/docs/deployment-strategies/canary | Canary phases, supported targets, deploy analysis |
| Cloud Deploy: canary to Cloud Run | https://docs.cloud.google.com/deploy/docs/deployment-strategies/canary/cloud-run | Services and worker pools (not jobs) |
| Cloud Run: rollbacks, gradual rollouts, traffic migration | https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration | `--no-traffic`, `--tag`, `update-traffic`, rollback |
| Artifact Registry | https://docs.cloud.google.com/artifact-registry/docs | Repositories, cleanup policies, vulnerability scanning |
| Binary Authorization | https://docs.cloud.google.com/binary-authorization/docs | Admitting only attested images |
| SLSA | https://slsa.dev/ | Supply-chain levels and provenance |
| Workload Identity Federation with deployment pipelines | https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines | Keyless auth from GitHub Actions, GitLab and other CI |
| Cloud Deploy: roll back a target | https://docs.cloud.google.com/deploy/docs/roll-back | `targets rollback` (last successful release by default) |
| Cloud Deploy: manage rollouts | https://docs.cloud.google.com/deploy/docs/deployment-strategies/manage-rollout | Advancing canary phases, rollout states |

## Infrastructure as code

| Source | URL | Use it for |
|---|---|---|
| Terraform on Google Cloud: style and structure | https://docs.cloud.google.com/docs/terraform/best-practices/general-style-structure | Module structure, naming, variables |
| Terraform: root modules | https://docs.cloud.google.com/docs/terraform/best-practices/root-modules | One root per app and environment, under 100 resources |
| Terraform: security | https://docs.cloud.google.com/docs/terraform/best-practices/security | Remote state in Cloud Storage, state encryption |
| Terraform: version control | https://docs.cloud.google.com/docs/terraform/best-practices/version-control | Repository layout, branch per environment for root configs |

## Reliability and observability

| Source | URL | Use it for |
|---|---|---|
| SLO monitoring: alerting on burn rate | https://docs.cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate | `select_slo_burn_rate`, fast and slow burn |
| SLO monitoring: alert policy by API | https://docs.cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/create-policy-api | The alert policy body to put in Terraform |
| Google SRE book | https://sre.google/sre-book/table-of-contents/ | SLOs, error budgets, release engineering, postmortems |
| DORA metrics | https://dora.dev/guides/dora-metrics-four-keys | Lead time, deployment frequency, change fail rate, recovery time |
