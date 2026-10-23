# AGENTS.md — <Project Name>

Operating instructions for coding agents (<Claude Code, Codex, Cursor>) in this repository. Claude Code loads this file through `CLAUDE.md`; Codex and Cursor read it directly.<If nested: `<dir>/` carries short directory-specific additions in its own `AGENTS.md`.>

## What this project is

<One paragraph: what it does, for whom, where it runs, what it must never do. Add a table if there are several deployments or runtimes:>

| Deployment | Code | Runtime | Storage | Status |
| --- | --- | --- | --- | --- |
| <name> | <paths> | <runtime> | <store> | <live / dev / retiring> |

## The wiki is the memory

`wiki/` is the project's long-term memory: an LLM wiki in Open Knowledge Format (markdown + YAML frontmatter). It holds intent, decisions, domain rules, system understanding, runbooks and history. Code is the source of truth for **behavior**; the wiki is the source of truth for **why** and **what was agreed**. When they disagree, fix the wiki in the same change and say so.

**Session protocol, every task:**

1. **Start.** Read `wiki/now.md` (current state, active work, open questions), then `wiki/index.md`. Read the `wiki/system/` and `wiki/domain/` pages for the area you will touch. Do not re-derive what those pages already state.
2. **Work.** Follow the rules below. Prefer reading a wiki page over grepping the whole tree; prefer the code over the wiki when they conflict, then fix the wiki.
3. **Finish.** Update `wiki/now.md`, append to `wiki/log.md`, update any page whose facts changed, and add a `wiki/decisions/` record for any non-obvious choice you or the user made. If that choice reverses an earlier one, [supersede it](wiki/guides/how-to-track-changes.md#superseding-a-decision) so no page or code comment still states the old one. Run `python3 scripts/lint_wiki.py`. A change that alters behavior, setup or contracts without a wiki update is unfinished.

Guides: [how to use the wiki](wiki/guides/how-to-use-this-wiki.md) · [how to document](wiki/guides/how-to-document.md) · [how to track changes](wiki/guides/how-to-track-changes.md) · [retention policy](wiki/guides/archive-policy.md).

## Behavioral guidelines

Adapted from [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills) (MIT). They bias toward caution over speed; for trivial tasks, use judgment.

**1. Think before coding.** Don't assume, don't hide confusion, surface tradeoffs. State assumptions explicitly. If several interpretations exist, present them instead of picking silently. If a simpler approach exists, say so and push back when warranted. If something is unclear, stop, name what is confusing, and ask.

**2. Simplicity first.** Minimum code that solves the problem, nothing speculative. No features beyond what was asked. No abstractions for single-use code. No configurability that wasn't requested. No error handling for impossible scenarios. If 200 lines could be 50, rewrite. Ask: "Would a senior engineer call this overcomplicated?"

**3. Surgical changes.** Touch only what you must; clean up only your own mess. Don't "improve" adjacent code, comments or formatting. Don't refactor what isn't broken. Match existing style even if you'd do it differently. Mention unrelated dead code, don't delete it. Remove only the imports/variables your change orphaned. Every changed line should trace to the request.

**4. Goal-driven execution.** Define success criteria, loop until verified. "Add validation" becomes "write tests for invalid inputs, make them pass". "Fix the bug" becomes "write a reproducing test, make it pass". For multi-step work state a short plan of `step → verify` pairs. Report outcomes faithfully: failed tests are reported with output, skipped steps are named.

## Project rules

These are standing user directives; the dated record is in [wiki/product/user-directives.md](wiki/product/user-directives.md).

- **<Rule name>.** <One or two sentences: what is forbidden or required, and its scope.>
- **Never commit secrets or personal data.** <List the ignored paths: `.env*`, data dirs, credentials.>
- **Retired material is <deleted | archived under `wiki/archive/`>.** Retired pages and superseded decisions leave the live wiki this way; see the retention policy.
- **Dates are absolute.** Write `YYYY-MM-DD`, never "today" or "last week", in code comments, docs and the wiki. Wiki timestamps are UTC.

## Commands

```sh
<install>
<run locally>
<test>                       # <what it covers / prerequisites>
<build>
python3 scripts/lint_wiki.py # wiki conformance and links
```

## Conventions

- **<Language>:** <style, structure, dependency policy, where tests live>.
- **Errors and copy:** <tone of user-facing messages>.
- **Branches and PRs:** <naming, review expectations, CI>. Commits do not deploy unless the repo says otherwise.
- **Documentation:** facts go into the wiki page that owns the concept, not into a new top-level markdown file. Root markdown is limited to <`README.md`, `AGENTS.md`, `CLAUDE.md`, …>. Code comments that encode a decision cite its record (`# Decision: wiki/decisions/<file>.md`) instead of calling it permanent.
