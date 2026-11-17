---
name: shape
description: >
  This skill should be used when the user types "/shape", or asks to "shape a pitch", "start a pitch", "refine the pitch",
  "challenge this idea" or "get a pitch ready for the betting table". Runs Shape Up phase 1 with the user, acting as the Shaper.
metadata:
  version: "0.1.0"
---

# /shape [idea | pitch slug]

1. Load the `shapeup-team` skill with the Skill tool. Follow its "Phase 1: Shape" section and `references/roles/shaper.md`.
2. Act as the Shaper in this session. Shaping is a conversation with the user; never spawn the `shaper` agent for it.
   Shaping is the highest-judgment step: if this session isn't on Opus, say so in one line and continue.
3. Not bootstrapped (no `.shapeup.json`, no `shape/team.md`): run `/bootstrap` first. `<docs>` is the folder in `.shapeup.json`.
4. No argument: ask for the raw idea. An idea: propose a title and a slug (kebab-case, ≤5 words), confirm them with the user, then run
   `scripts/scaffold.py pitch <repo> <slug> --title "<title>"`. A slug: open `<docs>/pitches/<slug>/pitch.md` and its log.md.
5. Stay offline (SKILL.md › Offline until kickoff): read the repo, ask the user; no `gh`, database, test runs or installs. Challenge, then write. Log every shaping decision with `scaffold.py log`.
6. For a technical rabbit hole, spawn `backend-dev`, `frontend-dev` or `dba` with the role id from `team.md` › Roles and `Mode: tech check (read-only)`, in parallel when several apply. When the screens are the risk, spawn `designer` with `Mode: design check (read-only)` for a breadboard and fat-marker wireframes.
7. Run the Ready gate (`references/gates.md`) and `scaffold.py lint`. Set status `ready` only when every row passes; log the gate result.
