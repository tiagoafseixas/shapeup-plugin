---
name: stack-gcp-devops
description: Stack pack for the shapeup-team plugin — DevOps on Google Cloud. Cloud Build or GitHub Actions with Workload Identity Federation, Artifact Registry, Cloud Deploy, Cloud Run and GKE, Terraform, Secret Manager, Cloud Observability (Logging, Monitoring, Trace), SLOs and error budgets, FinOps, following the Professional Cloud DevOps Engineer exam guide. Loaded by the devops agent when the team config (team.md) › Roles names stack-gcp-devops. Also use it when writing or reviewing pipelines, Dockerfiles, Terraform or monitoring for Google Cloud in a repo set up by the shapeup-team plugin.
---

# Stack pack: DevOps on Google Cloud

| Layer | Covers | Agent |
|---|---|---|
| infra | Cloud Build, Artifact Registry, Cloud Deploy, Cloud Run, GKE (Standard and Autopilot), Terraform ≥1.7 with the `google` provider, Secret Manager, Cloud Logging, Monitoring and Trace | devops |

The role file says what to do and when (delivery as code, never deploy, release plan); this pack says how, on Google Cloud.
House rules in the repo (`<docs>/stack/<role id>.md`) win over this pack. Where this pack and the role file disagree on process, the role file wins.
The exam guide's five sections, summarised for this role: `references/exam-guide.md`.

## Commands the role file refers to

| Action | Command | Who runs it |
|---|---|---|
| IaC check (Small) | `terraform fmt -check -recursive && terraform init -backend=false && terraform validate && tflint` | DevOps, any time |
| Policy and misconfig scan (Small) | `checkov -d <infra>` or `trivy config <infra>` | DevOps |
| Pipeline and image lint (Small) | `actionlint` (GitHub Actions), `yamllint cloudbuild.yaml`, `hadolint Dockerfile` | DevOps |
| Image build and structure test (Medium) | `docker build -t <name>:<sha> .` then `container-structure-test test --image <name>:<sha> --config <test.yaml>` | DevOps, after kickoff |
| IaC unit test (Medium) | `terraform test` with `mock_provider "google" {}` in every test file | DevOps; without mocks it creates real resources, so the hook asks |
| Plan against real state (production read) | `terraform plan -lock=false -out=tfplan` | DevOps after the user picks option (c); otherwise the user runs it and pastes the summary |
| Read config, logs, metrics (production read) | `gcloud run services describe <svc> --region=<r>`, `gcloud logging read '<filter>' --limit=50 --freshness=1h` | DevOps after option (c), one question |
| Apply infrastructure | `terraform apply tfplan` | the user (runbook) |
| Release to staging | `gcloud deploy releases create <rel> --delivery-pipeline=<p> --region=<r> --images=<name>=<image>@<digest> --to-target=<staging>` · `gcloud deploy releases promote --release=<rel> --delivery-pipeline=<p> --region=<r> --to-target=<staging>` | DevOps (`team.md` › Staging target; one command, no chaining) |
| Staging on Cloud Run without Cloud Deploy | `gcloud run deploy <svc> --image=<image>@<digest> --region=<r> --project=<staging project>` | DevOps (`team.md` › Staging project) |
| Release to production | `gcloud deploy releases promote --release=<rel> --delivery-pipeline=<p> --region=<r> --to-target=<prod>` | the user, or the pipeline on merge with the user's approval |
| Canary step | `gcloud deploy rollouts advance <rollout> --delivery-pipeline=<p> --release=<rel> --region=<r>` | DevOps for a `-to-<staging>-` rollout; the user in production |
| Cloud Run gradual rollout | `gcloud run deploy <svc> --image=<image> --no-traffic --tag=<tag>` then `gcloud run services update-traffic <svc> --to-revisions=<rev>=5` | the user |
| Roll back | Cloud Run: `gcloud run services update-traffic <svc> --to-revisions=<previous-rev>=100` · Cloud Deploy: `gcloud deploy targets rollback <target> --delivery-pipeline=<p> --region=<r>` (the last successful release by default) | DevOps in staging; the user in production |

## Delivery

| Stage | On Google Cloud | Rule |
|---|---|---|
| Trigger | Cloud Build trigger or GitHub Actions on push and PR | External CI authenticates with Workload Identity Federation, never a service-account key |
| Check | Small and Medium tests, lint, IaC check, scans | Fail fast: the cheapest checks first |
| Build | One image per commit, tagged with the commit SHA, pushed to Artifact Registry | Build once, promote the same digest everywhere; never rebuild per environment, never deploy `latest` |
| Verify | Artifact Analysis vulnerability scan; SLSA provenance from Cloud Build; Binary Authorization on the production target | A critical finding blocks the release |
| Test | Large tests against an ephemeral or test environment: a Cloud Run revision with `--no-traffic --tag=pr-<n>` has its own URL | Ephemeral environments are deleted by the pipeline when the PR closes |
| Deliver | Cloud Deploy pipeline dev → staging → prod, Skaffold renders the manifests; approval required on prod | DevOps promotes to staging before each review; the user approves and promotes to prod |
| Migrate | Schema changes as a Cloud Run job or pipeline step before traffic moves, expand/contract with the DBA | The DBA's runbook order wins |

| Strategy | Use when | On Google Cloud |
|---|---|---|
| Rolling (standard) | Low-risk change, backward compatible | Cloud Deploy standard strategy; Cloud Run sends 100% to the new revision |
| Canary | A change that can fail under real traffic | Cloud Deploy canary with percentages (Cloud Run services and worker pools, not jobs; GKE via service networking or Gateway API), or Cloud Run traffic splitting by hand |
| Blue/green | Instant switch and instant rollback | Cloud Run tags (`blue`, `green`) and `update-traffic --to-tags` |
| Feature flag | Ship dark, release later or to some users | The app's flag; the flag flip is a runbook step |

Each strategy names its success metrics and its rollback in the release plan.

## Rules

| Area | Rule |
|---|---|
| Hierarchy | One project per environment and workload, grouped in folders; org policies set at the folder (allowed regions for data residency, no public IPs, no SA keys) |
| Identity | A dedicated service account per workload with only the roles it uses; no basic roles (`owner`, `editor`); IAM bindings in Terraform; no service-account keys |
| Secrets | Secret Manager, referenced by name and version: runtime injection (`--set-secrets` on Cloud Run, the Secret Manager CSI driver on GKE) over build time. In Cloud Build: `availableSecrets.secretManager` with `secretEnv` on the step that needs it, referenced as `$$NAME` |
| Keys and certs | Cloud KMS for application encryption keys; Certificate Manager for TLS |
| Terraform | Standard module structure; `main.tf`, `variables.tf`, `outputs.tf`; singular resource names that don't repeat the type; units in variable names (`ram_size_gb`); pin provider versions |
| State | Remote state in a Cloud Storage bucket with versioning; one root module per environment and application; under 100 resources per state |
| Networking | Shared VPC for shared networks; Private Service Connect or private IP to managed services; no `0.0.0.0/0` ingress without a load balancer and Cloud Armor |
| Labels | `app`, `env`, `team`, `pitch` labels on every resource that costs money |
| Change | Every change goes through the pipeline; a console change is drift, and the next plan reverts it |

## Tests per size

| Size | Tool | How it enforces the size (testing.md) |
|---|---|---|
| Small | `terraform fmt`/`validate` with `init -backend=false`, `tflint`, `checkov` or `trivy config`, `hadolint`, `actionlint` | No credentials in the environment: anything that reaches Google Cloud fails. Each runs in seconds. |
| Medium | `terraform test` with `mock_provider "google"`; `docker build` + `container-structure-test`; `kubectl kustomize` or `helm template` piped to `kubeconform` | Mocked providers and local builds only; no project id is set, so a real call fails |
| Large | The pipeline deploys a tagged no-traffic revision or an ephemeral environment; QA's Large tests and a smoke check run against its URL | Runs in the pipeline with its own identity, never from the agent's shell |

## Observability

| Signal | How | Rule |
|---|---|---|
| Logs | JSON to stdout (Cloud Run and GKE ship it to Cloud Logging); `severity` and `message` fields; `logging.googleapis.com/trace` to join the trace | No personal data; exclusion filters and sampling for noisy logs; sinks to BigQuery or Cloud Storage for retention beyond the default |
| Metrics | Built-in Cloud Run and GKE metrics; log-based metrics for business events; Managed Service for Prometheus on GKE | A metric per new endpoint or job: rate, errors, latency (or runs and failures for jobs) |
| Traces | OpenTelemetry SDK exporting to Cloud Trace | Propagate the trace context across services and Pub/Sub |
| Synthetic | Uptime checks or synthetic monitors on public endpoints and key journeys | One per journey the pitch adds |
| SLOs | Cloud Monitoring services with request-based SLIs (availability, latency) and an error budget | Burn-rate alerts with `select_slo_burn_rate`: fast burn pages, slow burn opens a ticket |
| Alerts | `google_monitoring_alert_policy` in Terraform, with documentation and a notification channel | Every alert says what to do; one that nobody acts on is deleted |

Incident mitigation, in the release plan's rollback: shift traffic back (`update-traffic`), add capacity (max instances, node pool),
drain a bad zone or region at the load balancer. Blameless postmortem notes go to `<docs>/ideas.md` at cool-down.

## Cost and performance

| Rule | How |
|---|---|
| Right-size from data | Recommender and Active Assist (`gcloud recommender recommendations list --recommender=<id>`) as a production read; apply through Terraform |
| Cloud Run | Set `concurrency`, `max-instances` (a cost and quota ceiling) and `min-instances` only where cold starts hurt the SLO |
| GKE | Autopilot by default; Standard with cluster autoscaler and node auto-provisioning when you need node control; Spot VMs for interruptible batch |
| Commitments | Committed use discounts for the steady baseline, after a month of usage data; sustained use discounts apply by themselves on Compute Engine |
| Observability cost | Log exclusions and sampling, metric cardinality limits, retention by need |
| Artifacts | Artifact Registry cleanup policies: keep the deployed and recent digests |
| Budgets | A budget with alerts per project; the release plan states the monthly change |

## Review checklist

| Finding | Sev |
|---|---|
| A service-account key, secret value or credential in the repo, a build log or a Terraform variable default | `must` |
| A basic role (`owner`, `editor`) or a project-wide binding where a resource-level one would do | `must` |
| An image deployed by tag (`latest`) instead of digest, or rebuilt per environment | `must` |
| A new resource clicked in the console instead of declared in Terraform | `must` |
| A release without a rollback command or success metrics | `must` |
| A new endpoint or job without a metric and an alert on its errors | `must` |
| Public ingress without authentication, Cloud Armor or a reason in log.md | `must` |
| Terraform state stored locally or in the repo | `must` |
| Missing labels on a costly resource | `~` |
| `min-instances` set without an SLO reason | `~` |
| Logs that aren't JSON, or lack the trace field | `~` |

## Sources

Indexed in `references/sources.md`: one table per area, columns Source · URL · Use it for. Official docs first.
