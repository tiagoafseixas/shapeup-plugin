# Changelog

Versions of the `shapeup-team` plugin. Stack packs keep their own versions in `marketplace.json`.

| Version | Date | Change |
|---|---|---|
| 0.8.0 | 2026-11-18 | DevOps role (optional `devops` agent): pipeline, images, infrastructure as code, config and secret names, observability and the release plan; promotes builds to the staging target in `team.md` before each review, never to production, never applies infrastructure. Delivery files become DevOps's when the team has the row; `Infra?` on the board, Delivery in tech.md, a Release section in the runbook. The guard blocks cloud writes and secret reads and asks before cloud reads. New `infra` layer for stack packs; new pack `stack-gcp-devops` 0.1.0, following the Professional Cloud DevOps Engineer guide. |
| 0.7.0 | 2026-11-18 | Shaping tells the journey first: processes as numbered steps confirmed with the user, then one swimlane Flow, one breadboard per process (`Step n · Place` → `Done`), then ≤4 sketches read from the real screens. Sketches are rendered and looked at (`wireframe --png`, `check:` lines; the renderer no longer overlaps a row that doesn't fit). Evidence, branded names and colliding terms in step 1; manual work is always a rabbit hole. New Ready gate rows and lint checks. |
| 0.6.0 | 2026-11-18 | Sketches drawn from text in the app's own shell (`scaffold.py wireframe`), replacing ASCII wireframes; Mermaid breadboard. |
| 0.5.0 | 2026-11-17 | Review rounds: work until there's something to review with the user; budget of 2 (Small) or 6 (Big) reviews; final review before ship. |
