---
name: stack
description: >
  This skill should be used when the user types "/stack", or asks to "add a stack pack", "support MUI / Vue / Rails / MySQL",
  "write a pack for our stack", "add house rules for the frontend", or "which stack packs does this repo use".
  Lists, creates and lints stack packs for the shapeup-team plugin, and adds a repo's house rules.
metadata:
  version: "0.1.0"
---

# /stack [list | new <name> | house <role id> | lint <pack dir>]

Stack packs hold the how for one stack; the team's roles stay stack-agnostic. Load the `shapeup-team` skill first (Skill tool): its
"Roles and stack packs" section says how roles, packs and house rules fit. `scaffold.py` below is in that skill's `scripts/`.

| Command | Do |
|---|---|
| `list` (default) | Show `<docs>/team.md` › Roles. For each row, load the pack with the Skill tool and report installed or missing, and whether `<docs>/stack/<role id>.md` exists. |
| `new <name>` | Create a pack plugin (steps below) |
| `house <role id>` | `scaffold.py house <repo> <role id> --pack <the row's pack>`, then fill it with the user: only what differs from the pack |
| `lint <pack dir>` | `scaffold.py lint-pack <pack dir>` |

## new <name>

1. Ask once for anything the name doesn't settle: layer (backend, frontend, database), the technologies and majors (e.g. "React 19 + MUI v7"), and where to write it.
   Default location: `stack-<name>/` beside the repo, or `plugins/` when working inside the shapeup-plugin marketplace repo.
2. `scaffold.py pack <dir> <name> --layer <layer> --tech "<technologies>"`.
3. Index the official docs before writing any rule. Fetch the docs' index (`llms.txt` when the site has one) and read the main pages per area:
   setup, the component or data model, styling or theming, forms, data fetching, testing, performance, accessibility, migration guides between majors.
   Put each page in `references/sources.md` (Source · URL · Use it for), official docs first.
4. Fill the pack's SKILL.md section by section. Every rule names the API it uses and comes from an indexed page. Version notes cover what readers mix up between majors.
   Tests per size says how this stack makes a database or network access fail in a Small test, and how to list slow tests.
5. Follow `references/writing-style.md`. Run `scaffold.py lint-pack <dir>/stack-<name>` until it's clean.
6. Package it (`cd <dir>/stack-<name> && zip -r ../stack-<name>.plugin . -x '*.DS_Store'`) and send the `.plugin` file to the user, or add it to their marketplace's `marketplace.json`.
7. Add or update the role's row in `team.md` › Roles with the new pack.
