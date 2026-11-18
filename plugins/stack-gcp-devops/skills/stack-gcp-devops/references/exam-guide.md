# Professional Cloud DevOps Engineer: the exam guide, for this role

The exam guide's five sections and what each one means for a DevOps turn in a Shape Up cycle. Weights are the guide's
approximate share of the exam. Source: https://services.google.com/fh/files/misc/professional_cloud_devops_engineer_exam_guide_english.pdf

| # | Section | Weight | In this pack |
|---|---|---|---|
| 1 | Bootstrapping and maintaining a Google Cloud organization | ~20% | Rules |
| 2 | Building and implementing CI/CD pipelines for applications, infrastructure and ML | ~25% | Delivery, Commands |
| 3 | Applying site reliability engineering practices | ~18% | Observability (SLOs), release plan |
| 4 | Implementing observability practices and troubleshooting | ~25% | Observability |
| 5 | Optimizing performance and cost | ~12% | Cost and performance |

## 1. Bootstrapping and maintaining an organization

| Topic | What to know | In a cycle |
|---|---|---|
| Resource hierarchy | Folders and projects organised around applications and environments; Shared VPC, VPC peering and Private Service Connect for shared networking; one scope for monitoring and logging across projects | A new workload gets its own project or reuses the environment's; never a new pattern in a pitch without a `DECIDE` |
| IAM and org policies | Least-privilege roles, service accounts created and managed per workload; org policies for constraints such as data residency | Every IAM change is Terraform and a release-plan line the user reads |
| Infrastructure management | IaC with Terraform, Infrastructure Manager, Cloud Foundation Toolkit blueprints, Config Connector, Helm, GitOps; scripting in Python or Go | Use the repo's tool; adopt a blueprint before writing a module |
| CI/CD architecture | Cloud Build for CI, Cloud Deploy for CD (Skaffold, Kustomize), Artifact Registry; third-party tools (Jenkins, Argo CD, Packer, kpt); securing the CI/CD tooling itself | Keep the pipeline the repo has; secure its identity (Workload Identity Federation) |
| Multiple environments | Staging and production separated; ephemeral environments; configuration and policy management; GKE fleets; safe patching and upgrades | Ephemeral per PR where the platform allows; upgrades are their own pitch, not a side effect |
| Development environments | Cloud Workstations and Cloud Shell with custom images and the Cloud SDK; AI assistants (Gemini Code Assist, Gemini Cloud Assist, Gemini CLI) | Local and test environments match production's versions |

## 2. CI/CD pipelines and continuous testing

| Topic | What to know | In a cycle |
|---|---|---|
| Pipeline design | CI/CD for applications and infrastructure; artifacts in Artifact Registry; hybrid and multi-cloud deployment (e.g. GKE); triggers; approval flows | Build once, promote the digest; production needs the user's approval |
| Implementation | Auditing and tracking deployments (Artifact Registry, Cloud Build, Cloud Deploy, Audit Logs); rollout strategies (canary, blue/green, rolling, traffic splitting, feature flags) with success metrics; troubleshooting failed deploys | The release plan names the strategy, the success metrics and the rollback |
| Configuration and secrets | Cloud KMS; Secret Manager, Certificate Manager, Parameter Manager; Workload Identity Federation; injecting secrets at build time or at runtime | Runtime injection by default; names in the repo, values with the user |
| Pipeline security | Artifact Analysis vulnerability scanning; supply chain security with Binary Authorization and SLSA; IAM policies per environment | Scans in the pipeline; Binary Authorization on the production target |

## 3. Site reliability engineering

| Topic | What to know | In a cycle |
|---|---|---|
| Change vs reliability | SLIs, SLOs and SLAs; error budgets; the cost of each extra "nine" | A pitch that touches a journey with an SLO checks the error budget before the release; a spent budget favours a canary or a later release |
| Service lifecycle | Planning, deployment, maintenance, retirement; capacity planning with quotas, limits and reservations (Dynamic Workload Scheduler for scarce accelerators); autoscaling for managed instance groups, Cloud Run and GKE | Tech check: will the pitch hit a quota or need capacity? Max instances is both a cost and a safety ceiling |
| Incident mitigation | Drain or redirect traffic; add capacity; roll back | Every release plan has a tested rollback; mitigation first, root cause after |

## 4. Observability and troubleshooting

| Topic | What to know | In a cycle |
|---|---|---|
| Telemetry | Collecting logs with the Ops Agent, OpenTelemetry, Audit Logs, VPC Flow Logs and Cloud Service Mesh; trimming log cost with filters, sampling and exclusions; metrics from apps, platforms, networks, Managed Prometheus; synthetic monitors; custom and log-based metrics | Every new endpoint or job ships with its logs, metrics and an alert |
| Logs | Logs Explorer and the Logging query language; export and retention to BigQuery, Pub/Sub or Cloud Storage; redacting personal or health data with log processors; Gemini Cloud Assist for analysis | No personal data in logs; retention by need |
| Metrics and alerts | Metrics Explorer; dashboards (creation, filters, sharing, playbooks, PromQL); alerting on SLIs, SLOs and cost; integrations (webhooks, PagerDuty, Rootly) | Alerts in Terraform with documentation; dashboards linked from the release plan |
| Tracing | OpenTelemetry; trace waterfalls and spans; joining trace ids to structured logs | The trace field in every log line |
| Troubleshooting | Infrastructure, pipeline, application and observability problems; performance and latency | A red pipeline is triaged first: config (yours) or code (its author's) |

## 5. Performance and cost

| Topic | What to know | In a cycle |
|---|---|---|
| Performance data | Application performance monitoring; Active Assist insights and recommendations | Read recommendations as a production read; apply them through Terraform |
| FinOps | The cost of observability; Spot VMs; right-sizing; committed and sustained use discounts and network tiers; recommenders for cost, security, performance, manageability and reliability; per-workload optimisation on GKE, Cloud Run and Compute Engine | The release plan states the monthly cost change; cost work found in the cycle goes to `ideas.md` |
