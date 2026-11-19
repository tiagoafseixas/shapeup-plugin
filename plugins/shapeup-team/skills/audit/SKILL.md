---
name: audit
description: This skill should be used when the user types "/audit", or asks to "audit the release process", "review the readiness of the api service", "check our pipeline", "is the billing job production-ready" or "run a readiness review". DevOps reviews something that runs (a service, a job, the pipeline, a process) read-only, by the Well-Architected pillars and DORA, and files the findings as ideas.
---

# /audit: readiness review

A read-only review run by the DevOps role, outside any cycle. Findings go to an audit file and to `ideas.md`; nothing is fixed.

1. Load the `shapeup-team` skill with the Skill tool. You are the Conductor.
2. No `<docs>/team.md`: run `/bootstrap` first. Without a `devops` row in `team.md` › Roles, say the review runs without a stack pack's platform checks and ask whether to continue.
3. Ask the user one question if the request doesn't say both: what is reviewed, and what prompted it.
4. Spawn the `devops` agent (model Opus for a tier 0–1 target, Sonnet otherwise) with `Mode: readiness review`, the target, the reason, and `references/readiness-review.md`.
5. Pass its `HUMAN` question to the user as it comes (production facts, with the three options); send the answer back to the same agent.
6. When it reports: show the user its ≤5-line summary and the audit file's path. Don't commit; the user commits the audit and `ideas.md`.
