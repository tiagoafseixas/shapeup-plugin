---
name: bootstrap
description: >
  This skill should be used when the user types "/bootstrap", or asks to "set up the team in this repo", "bootstrap Shape Up here",
  "start using shapeup-team" or "prepare this repo for pitches". Runs once per repo: picks the docs folder with the user,
  writes .shapeup.json and the team config, offline.
metadata:
  version: "0.1.0"
---

# /bootstrap

Once per repo, before the first pitch. Offline: read files and ask the user; no network, no database, no test runs, no installs.

1. Load the `shapeup-team` skill with the Skill tool. You are the Conductor. `scaffold.py` is in its `scripts/`.
2. Already bootstrapped (`.shapeup.json` at the repo root, or a `shape/team.md`): say where the docs folder is and stop. Moving it is a manual edit.
3. Ask the user where the team's docs live. Offer `shape/` (default), `docs/shape/` and their own folder; one question, in plain words.
   Never pick the folder without asking.
4. Ask for the product name, then run `scaffold.py init <repo> --product "<name>" --docs <folder>`.
   It writes `.shapeup.json` and creates `<docs>/team.md`, `shell.txt`, `ideas.md`, `decisions.md`, `pitches/` and `betting/`.
5. Fill `<docs>/team.md` from the repo's files: `package.json`, `pyproject.toml` / `requirements*.txt`, `pom.xml` / `build.gradle`, `go.mod`, `Gemfile`, `composer.json`, `*.csproj`, framework settings, CI config, `AGENTS.md` / `CLAUDE.md`.
   - Roles: one row per developer role (role id `<layer>-<stack>`), its agent, its stack pack and its path; one row for the database.
     Delivery files in the repo (CI workflows, `cloudbuild*.yaml`, Dockerfiles, `*.tf`, Kubernetes or Helm manifests): propose a `devops-<platform>` row
     with agent `devops`, its pack (`stack-gcp-devops` when they target Google Cloud) and the infrastructure folder as its path. Ask the user: with the row,
     delivery files become DevOps's; without it, they stay with the developers.
   - Commands: the Small, Medium and Large test commands, lint, build and migration checks per role, and DevOps's IaC, pipeline and image checks, as the repo runs them. Write them down; don't run them.
   - Services: list what the repo deploys (services, jobs, schedules, from the delivery files and the code) and propose a tier for each with the reason; the user confirms or corrects every tier.
   - Ask the user, in one message, what files can't tell: the base branch, the production database instance name, the largest tables and their size (or "ask per pitch"), PR reviewers, and with a DevOps row the cloud projects per environment (names only) and the staging target DevOps may promote to (`team.md` › Staging target, Staging project, Production project).
6. Fill `<docs>/shell.txt` from the UI code: the layout component, app shell or base template, its nav items, and 2–3 screens
   for the conventions (tables or cards, forms on a page or in a dialog, where page actions sit). Draw the preview with
   `scaffold.py wireframe <repo>` and show `<docs>/shell.svg` to the user: "Is this your app's frame?". Fix what they correct.
   No UI in the repo: `layout: none`.
7. Load each role's stack pack with the Skill tool. List the missing ones with their install command, or offer `/stack new <name>`.
8. Grep the repo's files for connection strings; report file paths, never values.
9. Run the Bootstrap gate (`references/gates.md`) and report in ≤5 lines: the docs folder, the roles and their packs, what's missing, and the next step (`/shape <idea>`).
   Don't commit: the user commits the docs folder and `.shapeup.json`.
