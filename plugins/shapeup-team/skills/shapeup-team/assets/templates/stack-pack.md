---
name: stack-{{slug}}
description: Stack pack for the shapeup-team plugin — {{summary}}. Loaded by the {{agent}} agent when shape/team.md › Roles names stack-{{slug}}. Also use it when writing or reviewing {{tech}} code in a repo with a shape/ folder.
---

# Stack pack: {{tech}}

| Layer | Covers | Agent |
|---|---|---|
| {{layer}} | <versions this pack is written for, e.g. "Library 2.x–3.x"> | {{agent}} |

The role file says what to do and when (tests first, handoffs, gates); this pack says how, in this stack.
House rules in the repo (`shape/stack/<role id>.md`) win over this pack. Where this pack and the role file disagree on process, the role file wins.

## Version notes

<What changed between the majors a reader is likely to mix up. Check the installed versions first. Delete the section if nothing applies.>

## Layering

<Backend and frontend packs. A database pack replaces this section with `## Commands the role file refers to` (backup, confirm backup,
read-only check, read-only user setup) and `## Migration review` (each change, its risk on a big table, the safe pattern).>

| Logic | Goes in | Never in |
|---|---|---|
| <one row per kind of logic> | <the concrete construct in this stack> | <where it tends to leak> |

## Rules

| Area | Rule |
|---|---|
| <area> | <one imperative rule, with the API name> |

## Tests per size

| Size | Tool | How it enforces the size (testing.md) |
|---|---|---|
| Small | <runner, base class> | <how a DB, network or file access fails the test; how to list slow tests> |
| Medium | <runner, fixtures> | <test DB, what gets mocked at the boundary> |
| Large | <e2e tool> | <how the system runs; what gets stubbed at the network edge> |

## Performance

| Rule | How |
|---|---|
| <rule> | <API or tool> |

## Review checklist

| Finding | Sev |
|---|---|
| <stack-specific mistake QA or review should catch> | `must` / `should` / `nice` |

## Sources

Indexed in `references/sources.md`: one table per area, columns Source · URL · Use it for. Official docs first.
