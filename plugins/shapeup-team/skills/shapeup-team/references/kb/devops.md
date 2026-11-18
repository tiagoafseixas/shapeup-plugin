# Knowledge base: DevOps

The principles behind `roles/devops.md`, each with where it shows up in the role, and the sources they come from.

## Principles

| Principle | What it means | Where it shows up |
|---|---|---|
| Collaboration, shared ownership | Development and operations work as one team; whoever builds it also cares how it runs. Operations needs are as important as design and code. | DevOps is a role on the board, in tech checks, orient and scope mapping, not a team downstream |
| Automation | Builds, tests, packaging, infrastructure and releases are scripts and code, not manual steps | Pipeline and IaC are code on the cycle branch |
| Continuous integration | Merge small changes often; each is built and checked automatically and stays releasable | The cycle branch's pipeline stays green; red is a `BLOCK` |
| Continuous testing, shift left | Automated tests run with every change, early, inside the pipeline | Small and Medium checks before commit and in CI; Large in an environment |
| Continuous delivery vs deployment | Delivery keeps every change ready to release with a manual go; deployment releases every passing change automatically | Delivery: the user releases, from the runbook |
| Safe releases | Rolling, canary or blue/green deploys and feature flags limit the blast radius; every release has a rollback | Release plan › Strategy and Rollback |
| Infrastructure as code | Environments are declared, versioned and reproducible | Every new resource is code in the role's path |
| Monitoring and feedback | Logs, metrics, health data and alerts after release; what they show feeds the next plan | Observability for every new part; success metrics in the release plan |
| Security built in (DevSecOps) | Code, dependency and image scans and access controls inside the pipeline from the start | Scans in the pipeline; least-privilege identities; secrets by name only |
| Incremental improvement | Small releases, regular review of bottlenecks and tooling | One cycle, one shippable increment |
| Failure as learning | Incidents get a root cause, a fix that prevents recurrence, and shared lessons | Cool-down: incidents and toil to `ideas.md` |
| Standard environments | Containers make local, test and production behave alike | Local and test match production's engine and versions |

## Lifecycle

Plan → Code → Build → Test → Release → Deploy → Operate → Monitor, then back to Plan. The "7 Cs" name the continuous parts:
development, integration, testing, delivery/deployment, monitoring, feedback and operations. In this plugin, Plan is shaping,
Code to Release happen in the cycle, Deploy is the user's runbook, and Operate/Monitor feed cool-down and the next pitch.

## Trends worth knowing

| Trend | For this role |
|---|---|
| Cloud-native: microservices, containers, managed platforms | Prefer the platform's managed services over running your own |
| DevSecOps: security shifts left | Scans and policy checks are Small checks, not a later phase |
| Testing shifts further left | Infrastructure gets tests too (the sizes in the role file) |
| Platform engineering: internal developer platforms | Reuse the repo's existing pipeline and modules before adding new ones |

## Sources

| Source | URL | Use it for |
|---|---|---|
| Atlassian: What is DevOps | https://www.atlassian.com/devops/what-is-devops | Culture, the five principles, the engineer's profile |
| GeeksforGeeks: DevOps principles | https://www.geeksforgeeks.org/devops/devops-principles/ | The ten working principles |
| GeeksforGeeks: Introduction to DevOps | https://www.geeksforgeeks.org/devops/introduction-to-devops/ | Lifecycle stages with tools, adoption practices |
| GeeksforGeeks: DevOps lifecycle | https://www.geeksforgeeks.org/devops/devops-lifecycle/ | The eight phases and the 7 Cs |
| GeeksforGeeks: Evolution of DevOps | https://www.geeksforgeeks.org/devops/the-evolution-of-devops-major-trends-for-future/ | History and trends: cloud-native, DevSecOps, shift-left testing |
| Google SRE book | https://sre.google/sre-book/table-of-contents/ | SLOs, error budgets, release engineering, postmortems |
| DORA metrics | https://dora.dev/guides/dora-metrics-four-keys | Measuring delivery: frequency, lead time, change failure rate, recovery time |
