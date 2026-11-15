# Tech — {{title}}

| Pitch | Cycle | Branch |
|---|---|---|
| shape/pitches/{{slug}}/pitch.md | {{cycle}} | cycle/{{cycle}}-{{slug}} |

Keep only the sections that apply. Each diagram has a one-line caption saying what it answers.
Update a diagram in the same commit as the code it shows.

## Entities (DBA)
<Caption: which tables and relations change.>
```mermaid
erDiagram
```

## Classes (backend-drf)
<Caption: how models, QuerySets and services split the logic.>
```mermaid
classDiagram
```

## Flows (backend-drf, frontend-react)
<One sequenceDiagram per use case that crosses 3+ participants. Caption: "How <use case> works".>
```mermaid
sequenceDiagram
```

## Processes (owner of the process)
<flowchart TD for jobs, backfills and imports; stateDiagram-v2 for lifecycles.>
```mermaid
flowchart TD
```

## API contract (backend-drf)

| Method | Path | Request | Response | Errors | Permission |
|---|---|---|---|---|---|
