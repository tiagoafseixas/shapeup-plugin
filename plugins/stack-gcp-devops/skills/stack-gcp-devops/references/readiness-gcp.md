# Readiness review on Google Cloud

The platform checks for `/audit` (core: `references/readiness-review.md` in the shapeup-team plugin), by the same pillars.
Each check names the evidence to read. Commands marked *production read* run only after the user picks option (c); otherwise hand
them to the user to run.

| Pillar | Check | Evidence |
|---|---|---|
| Operational excellence | Releases go through Cloud Build or GitHub Actions and Cloud Deploy, never `gcloud run deploy` by hand | Delivery files; Cloud Audit Logs for deploys outside the pipeline (*production read*) |
| Operational excellence | Each alert policy has documentation and a notification channel | `google_monitoring_alert_policy` in Terraform |
| Security | No user-managed service-account keys | `gcloud iam service-accounts keys list --iam-account=<sa> --managed-by=user` (*production read*) |
| Security | No basic roles (`owner`, `editor`, `viewer`) on service accounts | IAM bindings in Terraform; IAM Recommender (*production read*) |
| Security | Pipelines authenticate with Workload Identity Federation | CI config: no `GOOGLE_CREDENTIALS` key secret |
| Security | Secrets in Secret Manager, injected at runtime | `--set-secrets` or `secretKeyRef`; no secret-looking env values in Terraform |
| Security | Artifact Analysis scanning on, Binary Authorization on the production target | Artifact Registry and Cloud Deploy config |
| Security | Org policies for allowed regions and no SA keys | Org or folder policy code; `gcloud resource-manager org-policies list` (*production read*) |
| Reliability | An SLO per tier 0–1 service with a burn-rate alert | `google_monitoring_slo` and an alert using `select_slo_burn_rate` |
| Reliability | `max-instances` set and below the project quota | Cloud Run config; quotas (*production read*) |
| Reliability | Cloud SQL backups and point-in-time recovery on; a restore tested | Ask the DBA |
| Cost | A budget with alerts per project; labels on costly resources | Billing budget code; resource labels |
| Cost | Log exclusions or sampling for high-volume logs; Artifact Registry cleanup policies | Logging sinks and exclusions; repository config |
| Performance | `min-instances` only where cold starts break the SLO; concurrency set | Cloud Run config |
| Sustainability | Region chosen for a reason; no idle resources | Recommender idle-resource insights (*production read*) |

Google publishes official agent skills that evaluate a workload against each Well-Architected pillar. If the user has installed
them (`npx skills add google/skills --skill google-cloud-waf-<pillar>`, pillars: `operational-excellence`, `security`,
`reliability`, `cost-optimization`, `performance-optimization`, `sustainability`), load the ones that match the review's scope with
the Skill tool and fold their findings into the audit file. Source: https://docs.cloud.google.com/architecture/framework
