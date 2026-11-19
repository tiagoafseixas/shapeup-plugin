# Readiness review (`/audit`)

A read-only review of something that runs, or is about to: a service, a job, the pipeline, a process such as "how we release".
It follows Google SRE's Production Readiness Review, which identifies a service's reliability needs from its specifics and can
start at any point of its life. Findings are organised by the six pillars of Google Cloud's Well-Architected Framework, plus
DORA's delivery capabilities for the pipeline itself. Platform checks come from the stack pack. Run by DevOps.

Outside Shape Up's scope, and kept compatible with it: a review files ideas, never work. A finding becomes a pitch, or a cool-down
fix, only when the user shapes and bets on it.

## Steps

| # | Step | Done when |
|---|---|---|
| 1 | Agree the scope with the user in one question: what is reviewed, and what prompted it (an incident, a launch, a new team member, a check-up) | Target and reason known |
| 2 | `scaffold.py audit <repo> <slug> --title "<target>"` creates `<docs>/audits/<date>-<slug>.md` | File exists |
| 3 | Read the evidence from files: `team.md` › Services (tier, SLO), delivery files, IaC, monitoring and alert definitions, runbooks and release plans of past pitches, `ideas.md`, the git history | Evidence table filled |
| 4 | Production facts the files can't give (quotas, alert history, real error rates, costs): one `HUMAN` question listing them all, with the three options (SKILL.md › Production access). Don't wait for it to review the rest; mark those checks "pending the user". | Asked once, or nothing needed |
| 5 | Check each pillar below, then the stack pack's audit checks | Every row checked, or listed under "Not checked" with the reason |
| 6 | Write each finding: what, evidence, severity, a one-line fix. `must` when it breaks the tier's target, or a security or data-safety rule; `~` otherwise | Findings table filled |
| 7 | One line per `must` in `<docs>/ideas.md`: `<date> audit <slug>: <finding> → <fix>`. `~` findings stay in the audit file | Ideas filed |
| 8 | Report to the user in ≤5 lines: the target, the count of `must` and `~`, the top three, the audit file | Reported |

The care scales with the tier: a tier 0–1 service gets every row; a tier 3 job gets security and cost, and the rest only where it's cheap to check.

## What to check

| Pillar | Questions |
|---|---|
| Operational excellence | Does every change reach production through the pipeline? Is there a rollback, and was it ever exercised? Does each alert route to someone and say what to do? Is there a runbook for the manual steps that remain? What toil repeats every release? |
| Security, privacy and compliance | Does each workload run as its own least-privilege identity? Any long-lived keys or secrets outside the secret manager? Are dependencies and images scanned in the pipeline? Personal data in logs? Data kept in the regions it must stay in? |
| Reliability | Does the service have an SLO for its tier, and an alert on burning it? Are backups taken and was a restore ever tested (ask the DBA)? What happens when each dependency fails? Quotas and capacity for the expected peak? A single point of failure in a tier 0–1 path? |
| Cost optimization | A budget with alerts? Labels to see who spends what? Idle or oversized resources? Log and metric volume that nobody reads? |
| Performance optimization | Is latency measured where users feel it? Autoscaling limits set, with a ceiling? Cold starts within the SLO? |
| Sustainability | Resources running with nothing to do; regions chosen without reason. Only for tier 0–1, and only where it's cheap to check. |
| Delivery (DORA) | Do builds and tests run on every change? Are deploys automated and small? Are approvals peer review plus automation, not a manual gate? The four keys from git and the user: deployment frequency, lead time for changes, change fail rate, time to restore. |

## Rules

- Read-only: no file outside `<docs>/audits/` and `<docs>/ideas.md` changes; no production read without the user's option (c).
- Evidence for every finding: a file and line, a command's output, or the user's answer. No finding from memory or habit.
- Don't fix what you find, however small: the user decides what gets shaped.
