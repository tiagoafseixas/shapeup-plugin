# Writing style

Every doc this team writes passes one test: **a reader opens any single block cold, understands it, and can act on it.**
A block is a table row, a log entry, a paragraph, a list item or a diagram. Read this before writing anything.

## Rules

| # | Rule | Bloated | Direct |
|---|---|---|---|
| 1 | State the fact. No preamble, no announcing what comes next. | "In this section we will describe how the backfill works." | "The backfill marks deals won in batches of 5,000." |
| 2 | One idea per sentence. One topic per block. Topic first. | "The index, which DBA reviewed and which is needed for S3, will be built concurrently because the table is big." | "Build the `(owner_id, closed_at)` index concurrently. `deals_deal` has 4.2M rows." |
| 3 | Name things in full in every block: file, model, endpoint, scope. Never "it", "the above", "as discussed". | "As mentioned, it should be fixed before that." | "Fix `DealSerializer.account` validation before S1 ships." |
| 4 | Numbers and names beat adjectives | "a large table", "quite slow", "several users" | "4.2M rows", "3.1 s p95", "12 reps" |
| 5 | Active voice, present tense, with a named actor | "The migration should be reviewed." | "DBA reviews migration 0007." |
| 6 | Cut hedges and filler | "basically", "it is worth noting that", "in order to", "we might want to consider" | delete them; "to"; say what to do |
| 7 | Every block works without its references. A link adds depth, never meaning. Max one link per block. | "See the runbook and decision #3 for details." | "Run the backfill after the deploy, off-peak. Source: runbook step 4." |
| 8 | Docs state decisions; log.md and DECIDE rows carry the reason, in one clause | Pitch: "Totals per currency, because FX needs rates, sources and rounding we haven't shaped." | Pitch: "Totals per currency." · log.md: "Totals per currency, no FX: FX needs its own pitch." |
| 9 | Lists for parallel items, tables for items with attributes, prose only for a story or an argument | a paragraph listing five endpoints and their methods | a table: method · path · purpose |
| 10 | Prefer a diagram to a paragraph that describes structure or order (`references/diagrams.md`) | 8 sentences on who calls whom | one `sequenceDiagram` |
| 11 | Don't restate. If a fact lives in one doc, other docs don't copy it, and don't point to it unless the reader needs it to act. | the pitch's no-gos copied into the board | QA's "Done when" checks a no-go in one line |
| 12 | Write only what the reader can't get from the code, the tests or git | a doc listing every model field | the one field whose meaning isn't obvious |
| 13 | One doc, one subject: a pitch never mentions another pitch | "Big batch: it ships the reminder engine that 'SMS reminders' reuses." | "Send payment reminders by email, starting with overdue invoices." |
| 14 | Explain only what the reader would get wrong without it | "…as in the mobile app", "(link to our website)", "so clients ask the accountant first" | cut it, unless removing it changes how the team builds |

## Direct and affirmative: the sentence edit

Run these six cuts on every sentence, in order. Example: the pitch appetite.

| # | Cut | Before → after |
|---|---|---|
| 1 | Put the verb first. Anything the team must do is an imperative. | "The plan is that we build the reminder engine" → "We build the reminder engine" |
| 2 | Drop the subject when it's us, the team or the product | "We build the reminder engine" → "Build the reminder engine" |
| 3 | Drop what the context already says: the product name in its own repo, values in the header table, the section heading | "Big batch, 20 rounds. Build the Acme reminder engine" (size is in the header table) → "Build the reminder engine" |
| 4 | Positive form: say what is. Keep "not" for real denials (no-gos, rejections). | "Reminders are not sent unless the accountant confirms" → "Reminders are sent only after the accountant confirms" |
| 5 | Definite form: imperative or "must" for requirements, "can" for options. Delete should, might, could, ideally, potentially. | "The job should ideally ask the accountant" → "The job asks the accountant" |
| 6 | Delete conversation residue: qualifiers that restate the default or answer a question raised while shaping, not one a reader will ask ("with or without X", "X is optional" when nothing implied it wasn't, "as on the web", "regardless of") | "lists the same overdue invoices as the dashboard, with or without a client filter" → "lists the same overdue invoices as the dashboard" |

Also turn hidden verbs back into verbs: "make a decision" → "decide", "perform a review of" → "review".
Descriptions of the world stay declarative, with the actor named ("Accountants already chase overdue invoices by hand…"). Only instructions and decisions go imperative.

Result: "Send payment reminders by email, starting with overdue invoices."

## Limits

| Block | Max |
|---|---|
| Sentence | 25 words |
| Paragraph | 4 sentences |
| Table cell | 2 sentences (lists inside a cell use ` · `) |
| Log row message | 3 sentences. A HUMAN row adds options as `A) … B) … Rec: A.` |
| Scope name | 5 words, domain language ("Win a deal") |
| Pitch | 1 page: within `team.md` › Pitch word limit (default 600) outside code blocks, plus wireframes |
| Turn report | 10 lines |

## Before → after

**Log row**
> Bloated: "Hi Shaper, while I was looking into S2 I noticed that the pitch mentions a fixed list of lost reasons but it doesn't actually specify what they are, so I was wondering whether you could let me know which reasons we should use, since frontend-react will need them for the picker and I also need them for the choices on the model."
>
> Direct: "S2: the pitch fixes a lost-reason list but names no values. I need the values for `Deal.lost_reason` choices; frontend-react needs the labels."

**Runbook step**
> Bloated: "Before proceeding, it's important to make sure that a backup has been taken, because the next steps modify a large amount of data and we want to be able to recover if anything goes wrong."
>
> Direct: `| 1 | Back up | gcloud sql backups create --instance=app-db | "Created backup" | Stop. Do not run step 2. |`

**Pitch problem** (baseline → workaround → cost)
> Bloated: "Sales managers often face significant challenges in keeping track of their team's pipeline, which can lead to inefficiencies and frustration across the organisation."
>
> Feature-first, still wrong: "An accountant clicks 'Remind' on an overdue invoice and the app emails the client."
>
> Direct: "Accountants already chase overdue invoices by hand: each Monday they export the list, then write every email in their mail app. That takes about two hours a week, and invoices slip when someone is away."

## Final check (run it before saving)

1. Cover everything except one block. Does that block still make sense? Repeat for each block.
2. Delete the first sentence of each paragraph. If nothing is lost, keep it deleted.
3. Does any "see X" carry meaning the block needs? Inline the one fact instead.
4. Does any adjective hide a number you know? Use the number.
5. Is anything here also in the code, the tests or another doc? Delete it here.
6. Did a qualifier get added because of a discussion ("with or without…", "…is optional", "as on the web")? If the general statement already covers it, delete it. Keep it only when it's a contract fact the builder needs (a tool's optional arguments).

## Sources

| Source | URL | Rule it backs |
|---|---|---|
| Strunk, *The Elements of Style* (1918, public domain) | https://www.gutenberg.org/ebooks/37134 | Active voice · positive form · definite, concrete language · omit needless words |
| Google developer documentation style guide: person | https://developers.google.com/style/person | Imperative for instructions; the "you" is implied |
| Google developer documentation style guide: highlights | https://developers.google.com/style/highlights | Active voice · present tense · conditions before instructions · no pre-announcing |
| Microsoft Writing Style Guide: brand voice | https://learn.microsoft.com/style-guide/brand-voice-above-all-simple-human | Get to the point fast · bigger ideas, fewer words · prune every excess word |
| Federal Plain Language Guidelines (PLAIN) | https://digital.gov/guides/plain-language/writing | Active voice · "must" for requirements · no hidden verbs · omit unnecessary words |
| National Archives: 10 plain-writing principles | https://www.archives.gov/open/plain-writing/10-principles.html | Main point first · one idea per paragraph · subject and verb close together |
