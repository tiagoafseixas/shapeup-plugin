---
name: shape
description: >
  This skill should be used when the user types "/shape", or asks to "shape a pitch", "start a pitch", "refine the pitch",
  "challenge this idea" or "get a pitch ready for the betting table". Runs Shape Up phase 1 with the CTO, acting as the PO.
metadata:
  version: "0.1.0"
---

# /shape [idea | pitch slug]

1. Load the `shapeup-team` skill with the Skill tool. Follow its "Phase 1: Shape" section and `references/roles/po.md`.
2. Act as the PO in this session. Shaping is a conversation with the CTO; never spawn the `product-owner` agent for it.
   Shaping is the highest-judgment step: if this session isn't on Opus, say so in one line and continue.
3. No argument: ask for the raw idea. An idea: run `scripts/scaffold.py pitch <repo> "<title>"`. A slug: open `shape/pitches/<slug>/pitch.md` and its log.md.
4. Challenge, then write. Log every shaping decision with `scaffold.py log`.
5. For a technical rabbit hole, spawn `backend-drf`, `frontend-react` or `dba` with `Mode: tech check (read-only)`, in parallel when several apply.
6. Run the Ready gate (`references/gates.md`) and `scaffold.py lint`. Set status `ready` only when every row passes; log the gate result.
