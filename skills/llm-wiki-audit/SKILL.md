---
name: llm-wiki-audit
description: Audit and clean up an existing LLM wiki (the wiki/ + AGENTS.md setup made by the llm-wiki skill) so agents read only the current truth — find decisions that were reversed but are still stated as current in wiki pages, AGENTS.md, user directives or code comments marked "permanent", retire superseded decision records (deleted or archived, as the user chooses), collapse inline history, merge duplicated facts into one owner page, and ask the user to settle conflicts the agent cannot. Use this whenever the user wants to audit, lint, prune, dedupe, tidy, slim down or "clean up" their wiki or agent docs, says the wiki is bloated, stale or contradicts itself, says "we switched from X to Y but the docs still say X", or asks for the periodic semantic lint pass the wiki guides describe.
---

# LLM wiki audit

A wiki that agents can't trust is worse than no wiki, because agents act on what they read. The main source of distrust is a decision that was reversed but is still stated as current somewhere: a page, `now.md`, a directive, an `AGENTS.md` rule, or a code comment that says `# permanent, do not change`. The second source is bloat: inline history, repeated facts and dead records that make reading slower and hide the current truth.

This skill is the safety net. The llm-wiki guides tell agents to supersede decisions properly at write time ([how-to-track-changes](../llm-wiki/assets/wiki/guides/how-to-track-changes.md), "Superseding a decision"); this pass catches what slipped through. A good audit leaves the wiki the same size or smaller, and leaves exactly one current statement of every choice.

## Before you start

Read, in the target repo:
- `AGENTS.md`, `wiki/now.md`, `wiki/index.md`.
- `wiki/guides/how-to-track-changes.md` (the **Superseding a decision** steps) and `wiki/guides/archive-policy.md` (retention). If the guides are missing or predate those sections, follow the steps in this file; they are the same.
- `wiki/product/user-directives.md`: find the **retention directive** (delete or archive retired material). If there is none and the user's request doesn't answer it, you'll ask for it in the question batch (step 5). Either way, record the answer as a directive row so later audits don't ask again.

If there is no `wiki/` with this layout, stop and suggest the `llm-wiki` skill instead.

Note the starting size from the `size` section in step 2. You'll report before and after.

## Workflow

### 1. Mechanical baseline

Run `python3 scripts/lint_wiki.py`. Fix mechanical errors that have one obvious fix (missing index entry, broken link to a renamed page). Note any warnings about superseded or missing decisions; they are leads for step 3.

### 2. Shortlist

```bash
python3 <skill-dir>/scripts/find_stale.py --repo <repo> [--since <git-rev>]
```

The default is the whole wiki. For a scoped or incremental audit ("only system/", "since the last audit"), pass `--since` with the commit from the date of the last `Lint` entry in `log.md` (`git rev-list -1 --before=<date> HEAD`), or just read the scoped pages.

The script only finds candidates: decision records and their chain, retired decisions that are still cited, accepted decisions that share a topic, "permanent"-style markers, inline history and near-duplicate paragraphs. Its keyword lists will miss things and flag false positives. Use it to know where to look, then read the pages.

### 3. Build the decision timeline

For each topic that has a decision (storage, auth, deploy target, API style…), work out which choice is **current**. Check these sources against each other:
- decision records and their `supersedes` / `superseded_by` links
- `user-directives.md` rows and `AGENTS.md` project rules
- `now.md` and `log.md` (`Decision` / `Directive` entries)
- **the code.** It shows what is actually running, so read it whenever a decision is about behavior.

Then grep every live statement of the old choices. That means the old record's filename, plus the old choice in words: the option name, config key, value or library. Search across `wiki/` (excluding `archive/` and `log.md`), `AGENTS.md`, `README.md` and code comments.

### 4. Classify each finding

| Finding | Example | Who resolves |
| --- | --- | --- |
| Reversed decision still stated as current | `system/storage.md` says SQLite; a 2026-06 record chose Postgres | Agent rewrites the text; code comments need approval |
| Superseded record not retired, or retired with no **Supersedes** line | old record still `accepted`, still listed in `decisions/index.md` | Agent, per retention (in the approval list) |
| Competing decisions | two `accepted` records on one topic, and neither the records, the code nor the user's request says which is current | **User** |
| Code contradicts an accepted decision, no newer record | decision says 100 req/min, code says 300 | **User**: was the decision changed, or is the code wrong? |
| "Permanent" marker | `# do not change: always X` | If a record covers it, agent rewrites the comment to cite the record (approval). If no record covers it, **user**: record a decision, or drop the comment? |
| Citation of a retired record | `# Decision: wiki/decisions/<old>.md` | Agent rewrites it to cite the replacement (approval). If no current record covers what the comment protects, reduce it to a plain description and put the question in `now.md` |
| Inline history in a live page | "Until 2026-06-15 we used SQLite; now…" | Agent: state the current truth; history stays in the decision chain, log and git |
| Duplicated fact | the same storage paragraph on two pages | Agent: keep it on the owning page, link from the other |
| Redundant page | a page whose facts all live elsewhere | Agent, per retention (in the approval list) |

When the newer choice is clear, the agent applies the fix. It is clear when a newer record or directive picks a different option on the same topic and the code or the user's request agrees, even if the newer record lacks a `supersedes` field (add it). When it's unclear which side is current, the user decides. Never pick silently, and don't treat "the code wins" as settling a question of intent: the code may be the bug.

### 5. One batch of questions

Ask everything at once, with a recommended answer for each. Skip any question the user's request already answers ("delete old stuff", "you can edit comments"), but still list the resulting actions so they can see them. Use the question tool if you have one and a numbered list otherwise:

1. **Retention**, only if no directive exists. Ask whether retired material should be deleted (git history and the superseding record are the trace) or archived in `wiki/archive/`. Recommend delete.
2. **Conflicts**, one per competing-decision, code-vs-decision or uncovered-marker finding. Show both claims with file:line, their dates and sources, and what you'd recommend.
3. **Approval list.** Every record or page to retire, each with the retention default pre-selected so the user can flip any single item to the other action. Also list every code comment edit, with the current text and the proposed rewrite (or removal).

Rewrites of wiki prose that follow a clear newer decision don't need approval; list them in the final summary instead. If the user can't answer something now, leave it alone and put it in `now.md` as an open question.

### 6. Apply

For each decision that changed, follow the superseding steps:
1. The current record gets a **Supersedes** section and `supersedes:` frontmatter, naming the old record and one line on why it was dropped. Name a deleted record by filename in backticks, not a link. This is the one place the rejected option survives, so agents don't propose it again.
2. Retire the old record as approved. Archive means `status: superseded`, `superseded_by`, `git mv` it to `archive/`, and add it to `archive/index.md`. Delete means `git rm`.
3. Rewrite every live mention to the current choice and cite the current record (`# Decision: wiki/decisions/<file>.md` in code). Remove inline history.
4. Replace stale rows in `user-directives.md` and rules in `AGENTS.md` with the current choice. If the current choice has no directive of its own, remove the row; the decision record owns it. Update `decisions/index.md` so it lists only decisions in force.

For each conflict the user settled, write the answer down. A new or superseding decision record if it was a real choice, a directive row if it is a standing rule, a wiki fix if it was a factual error. If the user said the code is wrong, don't fix the code here; record it as a task in `now.md`.

For duplicates, keep the fact on the page that owns the concept and replace the other copies with a link. Merge redundant pages into their owner before retiring them.

Bump `generated` (actor and UTC time) on every page you rewrite. Never edit archived bodies. Touch code only where it was approved, and only comments.

### 7. Verify

- `python3 scripts/lint_wiki.py` passes, and no "superseded decision" or "missing decision" warnings remain.
- Re-run `find_stale.py`. Every remaining hit should be a known false positive or an open question you recorded.
- Grep each old choice one last time. The only hits should be the current record's rationale (Context, description, Supersedes), the log, the archive and open questions in `now.md`.

### 8. Record and report

- Append one `Lint` bullet to `log.md` under today's **UTC** date (it may differ from the local date), summarizing the audit. Name deleted files in backticks, not as links. Leave older log entries alone, even links to records you deleted; the linter ignores dead links in the log.
- Update `now.md` with any open questions left unanswered.
- If `wiki/reviews/` exists, save the audit as a dated `Review` page.
- Tell the user:
  - which decisions were found reversed and where they were still stated
  - what was deleted or archived
  - which wiki rewrites were made without asking
  - their answers and where each one was recorded
  - what is still open
  - the live-page size before and after

Don't commit unless asked.

## Principles

- **One current statement per choice.** Everything else either cites it or is history in the decision chain, the log or git.
- **Keep why it was rejected, drop the rest.** Delete old text freely. Keep one line on why each replaced option was dropped, in the record that replaced it.
- **Ask about intent, fix mechanics.** Which choice is current, and whether to touch code, are the user's calls. Making the wiki agree with a clear decision is not.
- **Leave it smaller.** If the audit made the wiki bigger, something was duplicated instead of replaced.
