# Diagrams and wireframes

Diagrams replace prose about structure and order. They are written in Mermaid (renders on GitHub) and live in
`tech.md` (technical diagrams) or `pitch.md` (flow, breadboards, sketches). Screen sketches are a few lines of text that
`scaffold.py wireframe` draws as hand-drawn SVGs inside the app's own shell. Draw one only when it answers a question
the code doesn't answer at a glance.

## Which diagram, when

| Diagram | Mermaid type | Draw it when | Owner | Lives in |
|---|---|---|---|---|
| Entity | `erDiagram` | A scope adds or changes tables, columns or relations | DBA | tech.md · Entities |
| Class | `classDiagram` | A scope adds models with domain methods, services or query objects that work together | backend | tech.md · Classes |
| Sequence | `sequenceDiagram` | A use case crosses 3+ participants (UI → API → service → DB → task/external) | backend (frontend for UI-only flows) | tech.md · Flows |
| Activity | `flowchart TD` (Mermaid has no activity type) | A process has branches, loops or retries: backfill, import, job | Owner of the process | tech.md · Processes |
| State | `stateDiagram-v2` | An entity has a lifecycle with rules about which transitions are allowed | backend | tech.md · Processes |
| Flow | `swimlane-beta TB`: one lane per actor, plus a touchpoint lane (Email, notifications) | Every pitch with a user-facing journey: **one** for the whole journey | Shaper + user | pitch.md · Solution › Flow |
| Breadboard | `flowchart LR`: places as subgraphs named `Step n · Place`, affordances inside, arrows to where each leads | **One per process** (one actor goal: Request, Fulfil, View), never several processes in one | Shaper + user (designer on a design check) | pitch.md · Solution › Breadboard |
| Sketch | `wireframes/<screen>.txt` → `scaffold.py wireframe` → `<screen>.svg`, embedded with `![…]()` | The pitch adds a screen or changes a screen's layout: ≤4 per pitch | Shaper + user (designer on a design check) | pitch.md · Wireframes |

## Rules

| # | Rule |
|---|---|
| 1 | Write one line above each diagram saying what question it answers ("How a deal is won"). |
| 2 | Draw only the changed parts plus their direct neighbours. Style nothing in Mermaid. |
| 3 | Use real names: model, field, endpoint, service, task. The diagram must match the code. |
| 4 | ≤15 nodes per diagram. Bigger means two questions, so draw two diagrams. |
| 5 | Show error paths that change behaviour (`alt` in sequence, a branch in flowchart). Skip trivial ones. |
| 6 | Update the diagram in the same commit that changes the code it shows. The Ship gate checks this. |
| 7 | Sketches stay fat-marker: places, affordances, rough position, real labels for actions. No colours, sizes or final copy; data is squiggles. The designer (or the frontend role) keeps the design room. |
| 8 | Sketches follow the app: they are drawn inside `<docs>/shell.txt`, and follow its conventions (lists, forms, page actions, per-area layouts). A screen that breaks a convention says why in a note. |
| 9 | In a pitch, the order is fixed: Flow, then the breadboards, then the sketches. A new diagram that repeats what another already shows replaces it; it is never added next to it. |

## Viewers

| Diagram | Renders in | Doesn't render in |
|---|---|---|
| Mermaid (`flowchart`, `erDiagram`, …) | GitHub, GitLab, Mermaid Live; VS Code with a Mermaid extension | The VS Code preview without an extension; any offline check by an agent |
| `swimlane-beta` | Mermaid ≥11.16 (beta; the syntax can still change) | Older Mermaid versions: they show nothing or a syntax error. The breadboards still carry the journey. |
| Sketch SVGs | Every Markdown viewer, as images | — |

An agent can't render Mermaid offline. After writing a flow or a breadboard, say so to the user and name the viewer limits above;
they look at it. Sketches are different: render and look at each one yourself (Sketches › Render and look).

## Skeletons

Entity: what the deal tables look like after this bet
```mermaid
erDiagram
    USER ||--o{ DEAL : owns
    ACCOUNT ||--o{ DEAL : has
    DEAL {
        bigint id PK
        varchar outcome "open|won|lost, null = open"
        timestamptz closed_at "set when won or lost"
        varchar lost_reason "only when lost"
    }
```

Class: how the model, the queries and the service split the win logic
```mermaid
classDiagram
    class Deal {
        +outcome
        +closed_at
        +mark_won(at)
        +mark_lost(at, reason)
    }
    class DealQueries {
        +open_for(user)
        +won_in_week(user, week)
    }
    class DealService {
        +win(deal, by) Deal
        +lose(deal, by, reason) Deal
    }
    DealService ..> Deal : calls mark_*
    DealService ..> DealQueries : reads
```

Sequence: how a deal is won
```mermaid
sequenceDiagram
    actor Rep
    participant UI as DealCard
    participant API as POST /api/deals/{id}/win/
    participant S as deal_win()
    participant DB as Database
    Rep->>UI: Mark won
    UI->>API: POST
    API->>S: deal_win(deal, by=user)
    S->>DB: SELECT … FOR UPDATE; UPDATE deal
    alt already closed
        S-->>API: DealError
        API-->>UI: 409 "Deal already closed"
    else ok
        S-->>API: deal
        API-->>UI: 200 DealOutput
    end
```

Activity: how the backfill runs
```mermaid
flowchart TD
    A[Start: backfill_won_deals] --> B{--apply?}
    B -- no --> C[Print match count] --> Z[End]
    B -- yes --> D[Next 5,000 ids with outcome IS NULL and notes ~* '^WON\y']
    D --> E{Rows found?}
    E -- no --> Z
    E -- yes --> F[UPDATE outcome=won, closed_at=updated_at] --> D
```

State: which outcome transitions are allowed
```mermaid
stateDiagram-v2
    [*] --> open
    open --> won: deal_win
    open --> lost: deal_lose
    won --> [*]
    lost --> [*]
```

Flow: the whole journey, from a win to the manager's review
```mermaid
swimlane-beta TB
  subgraph Rep
    win[Mark won]
    amount[Confirm amount]
  end
  subgraph Email
    digest[Monday digest]
    nudge[Reminder]
  end
  subgraph Manager
    open[Open the week]
    reviewed[Mark reviewed]
  end
  win --> amount --> digest --> open --> reviewed
  digest -->|Not opened by Wed| nudge --> open
```

Breadboard: Win a deal (the rep)
```mermaid
flowchart LR
  subgraph S1["Step 1 · Deals list"]
    win["Mark as won"]
  end
  subgraph S2["Step 2 · Confirm win dialog"]
    amount["Final amount"]
    ok["Confirm win"]
  end
  subgraph Done["Done · Deal shows Won"]
  end
  win --> S2
  ok --> Done
```

Breadboard: Review the week (the manager)
```mermaid
flowchart LR
  subgraph S1["Step 1 · Monday email"]
    link["Open Won this week"]
  end
  subgraph S1b["Or step 1 · Reports menu"]
    menu["Won this week"]
  end
  subgraph S2["Step 2 · Won this week"]
    export["Export CSV"]
    reviewed["Mark reviewed"]
  end
  subgraph Done["Done · Week marked reviewed"]
  end
  link --> S2
  menu --> S2
  reviewed --> Done
```

| Flow (swimlane) | Breadboard |
|---|---|
| One per pitch: the whole journey across actors | One per process: one actor reaching one goal |
| Lanes: the actors, plus a touchpoint lane (Email, notifications) | Places: subgraphs named `Step n · Place`; an alternative is `Or step n · Place` |
| Nodes: 1–3 words, ≤15 in all | Affordances inside each place: what the actor can do there |
| Side paths labelled on the edge (`-->|Late|`) | Reads left to right in the order the actor acts: the trigger (an email, a page visit) first, a `Done · <outcome>` place last |

## Sketches

A sketch is a text file per screen in `<docs>/pitches/<slug>/wireframes/<screen>.txt`. `scaffold.py wireframe <repo> <slug>`
draws each one as `<screen>.svg`: the app shell in grey with the current nav item highlighted, the pitch's parts in ink,
numbered markers, notes in the margin and extra states below the screen. Embed each SVG under the pitch's Wireframes
heading: `![Won this week](wireframes/won-this-week.svg)`. The `.txt` is the source: edit it, redraw, commit both.
`scaffold.py lint` flags a sketch whose SVG is stale or not embedded, and more than 4 sketches.

### Before you sketch: read the real screen

Sketch a changed screen from its code, never from a guessed layout. Read its layout files (offline): the action bar, where tabs
sit (a side card or a horizontal strip), panels, and the conventions of that area of the app (admin pages, company pages, settings).
Record each area's conventions in `<docs>/shell.txt` as `area <name>: <convention>`, so the next sketch starts from them.
When it matters where a new element sits for users to notice it ("next to the main call to action"), ask the user.

### Few and small

| Do | Don't |
|---|---|
| ≤4 sketches per pitch: the screens that carry the risk | A sketch per screen the journey passes through |
| One dialog for related actions (upload or cancel in one request dialog) | A dialog per action |
| Collapse what exists and doesn't change into one grey line: `. Company details, unchanged` | Redraw the existing screen around the change |
| Leave out search, pagination, counts and subtitles | Draw them, unless they are the problem |

### The app shell

`<docs>/shell.txt` holds the frame every sketch sits in, so sketches look like this app: side nav or top bar, the nav
items, brand, account menu, global search, how the nav collapses on a phone, and the app's screen conventions.
It is filled at `/bootstrap` by reading the layout code (the layout component, app shell or base template; files only,
offline) and confirmed with the user: `scaffold.py wireframe <repo>` draws `<docs>/shell.svg` to show them.
The designer, or the frontend role, updates it when the shell changes.

| Key | Values | Drawn as |
|---|---|---|
| `layout` | `side`, `top`, `side+top`, `none` | Side nav, top bar, both, or no app chrome |
| `brand` | text | Name at the top of the nav |
| `nav` | `Item \| Item \| Item` | Nav items; a sketch's `nav:` line highlights one |
| `account` | `top-right`, `bottom`, `none` | Avatar in the top bar, or at the foot of the side nav |
| `search` | `yes`, `no` | Search box in the top bar |
| `mobile` | `bottom-tabs`, `menu` | Phone: tab bar with the nav items, or a ☰ menu |
| `lists`, `forms`, `page actions` | `table`/`cards`, `page`/`dialog`/`drawer`, `top-right`/`bottom`/`inline` | Not drawn: conventions the sketch author follows |
| `area <name>` | one line per area of the app: `area company pages: action bar with Go back left, primary actions right; tabs as a side card` | Not drawn: read before sketching a screen in that area |

### Notation

Header lines (optional, first): `title:` (window title; default: the first heading), `screen: desktop | mobile`,
`frame: page | dialog | drawer | none` (`none` for an email or an embed, no shell), `nav:` (the nav item to highlight).
Then one row per line, top to bottom. Tokens in a row sit side by side; `>>` pushes the rest of the row to the right.

| Write | Draws |
|---|---|
| `# Title` / `## Subtitle` | Page heading / section heading |
| `[Label]` / `[*Label]` | Button / primary button |
| `{Label}` / `{{Label}}` | Text input / text area |
| `(Label ▾)` | Select |
| `[ ]` `[x]` / `( )` `(x)` then a label | Checkbox / radio |
| `<Label>` | Link |
| plain text, or `"text"` | A label |
| `\| Col \| Col \| x4` | Table with 4 rows of squiggle data |
| `cards: Title x3` | 3 cards (title optional) |
| `tabs: One \| *Two \| Three` | Tabs, `*` = active |
| `~~~ x2` | 2 lines of body text (squiggles) |
| `[# Chart]` | Image or chart placeholder |
| `? No deals won this week` | Empty or message box |
| `--` | Divider |
| `^1` after a token or at the end of a row | Numbered marker; explained under `notes:` |
| `. ` at the start of a row | Grey: exists today and doesn't change (use it on a changed screen) |
| `state: Empty` | Starts another state of the screen, drawn below it in a narrow box (≈290px): only the element that changes |
| `notes:` then `1 What it does → where it leads` | The margin notes: each marker's behaviour and destination |
| `// text` | A comment, not drawn |

Sketch: the Won this week page (`wireframes/won-this-week.txt`)
```text
title: Won this week
nav: Reports
# Won this week  >>  [Export CSV]^1
(Owner ▾)  (Region ▾)^2
| Deal | Owner | Amount | Won on | x3 ^3
>> [*Mark reviewed]^4

state: Empty
? No deals won this week^5

notes:
1 Downloads the rows shown, filters applied.
2 Filters the table. Default: everyone.
3 One row per deal won Mon–Sun. Click a row → Deal page.
4 → Deals list, with this week marked reviewed.
5 Replaces the table when the week has no wins.
```

Sketch: the confirm dialog (`wireframes/confirm-win.txt`)
```text
title: Deals
frame: dialog
nav: Deals
## Mark "Northwind renewal" as won
{Final amount}^1
{Won on}  (Reason ▾)
[x] Notify the account owner
>> [Cancel]  [*Confirm win]^2
notes:
1 Prefilled with the deal amount.
2 → Won this week, the deal highlighted.
```

| Do | Don't |
|---|---|
| A sketch for each place that is new or changes layout and carries risk; a dialog is its own sketch with `frame: dialog` | Sketch screens the pitch doesn't change |
| Real labels on actions and headings: they are the affordances | Final copy for body text, sample data, colours, icons |
| A note for every marker: what it does and where it leads (match the breadboard) | Notes that explain the layout; the picture does that |
| Extra states (empty, no permission, error) as `state:` blocks when they change what the user can do | A state per edge case: those go in Rabbit holes |

### State blocks are narrow

A `state:` block draws only the element that changes (the button, the message) and its note says what it replaces:
`5 Replaces Request Account 360 while a request is open.` Never redraw a full row with `>>` in a state: the box is too narrow,
and the renderer moves the right-hand part to its own line and prints a `check:` line.

### Render and look

Run `scaffold.py wireframe <repo> <slug> --png`. It prints a `check:` line for each layout problem (a row that doesn't fit, a label
wider than its box, a column too narrow) and writes a PNG per sketch with the first local converter it finds (`rsvg-convert`,
ImageMagick, Inkscape). Open each PNG and look for overlaps, clipped text and empty boxes; fix the `.txt` and redraw until it's clean.
Report a sketch to the user only after you've looked at it. No converter on the machine: say so and ask the user to check the SVGs.
