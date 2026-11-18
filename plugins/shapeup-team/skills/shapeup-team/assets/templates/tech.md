# Tech — {{title}}

| Pitch | Cycle | Branch |
|---|---|---|
| <docs>/pitches/{{slug}}/pitch.md | {{cycle}} | cycle/{{cycle}}-{{slug}} |

Keep only the sections that apply. Each diagram has a one-line caption saying what it answers.
Update a diagram in the same commit as the code it shows.

## Entities (DBA)
<Caption: which tables and relations change.>
```mermaid
erDiagram
```

## Classes (backend)
<Caption: how models, queries and services split the logic.>
```mermaid
classDiagram
```

## Flows (backend, frontend)
<One sequenceDiagram per use case that crosses 3+ participants. Caption: "How <use case> works".>
```mermaid
sequenceDiagram
```

## Processes (owner of the process)
<flowchart TD for jobs, backfills and imports; stateDiagram-v2 for lifecycles.>
```mermaid
flowchart TD
```

## Delivery (DevOps)
<Caption: what runs where after this release: services, jobs, schedules, queues, secrets by name, and what calls what. Only what changes.>
```mermaid
flowchart LR
```

## API contract (backend)

| Method | Path | Request | Response | Errors | Permission |
|---|---|---|---|---|---|
