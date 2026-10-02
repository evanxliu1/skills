---
name: llm-wiki
description: Set up or migrate a repository's documentation into an agent-maintained LLM wiki in Open Knowledge Format (OKF) — a wiki/ bundle with now.md working memory, log.md history, index.md catalog, one-concept-per-file pages with YAML frontmatter, dated decision records, an immutable archive and four governing guides — plus a root AGENTS.md (Karpathy guidelines and a read-first/update-last session protocol) wired into CLAUDE.md, Cursor and Codex, and a dependency-free wiki linter in pre-commit and CI. Use this whenever the user wants to organize, restructure, bootstrap or standardize a project's docs for coding agents, asks for an AGENTS.md or CLAUDE.md setup, mentions an "LLM wiki", "Karpathy wiki", "OKF", "project memory for agents" or a "knowledge base in the repo", or wants a repo documented "like my other project" — even if they never say "wiki".
---

# LLM wiki setup

Turn a repository's documentation into a wiki that coding agents read first and update last, so knowledge accumulates across sessions instead of being re-derived from code and scattered prose every time.

The pattern combines three sources:
- **Karpathy's LLM wiki.** Raw sources stay immutable, an agent maintains the wiki, and a schema file governs it.
- **Google's Open Knowledge Format v0.2.** Each concept gets its own markdown file with YAML frontmatter; `index.md` is the catalog and `log.md` is the history.
- **Karpathy's behavioral guidelines** in a cross-tool `AGENTS.md`.

The result lives entirely in the repo: it is versioned with the code, renders on GitHub, and opens as an Obsidian vault.

## What you will produce

```
AGENTS.md                      schema + behavioral contract for every agent (Codex reads it natively)
CLAUDE.md                      `@AGENTS.md` import plus Claude-only notes
.cursor/rules/agents.mdc       alwaysApply pointer for Cursor
<subdir>/AGENTS.md + CLAUDE.md optional, for large subsystems with their own rules
scripts/lint_wiki.py           dependency-free linter
.githooks/pre-commit, CI step, PR-template checkbox   enforcement (where they fit)
wiki/
  index.md  log.md  now.md     catalog, history (newest first), working memory
  product/  system/  ops/  decisions/  guides/  archive/   always
  domain/  reviews/            when the project warrants them
```

The four pages in `wiki/guides/` are the full rulebook for writing in this wiki: page anatomy, frontmatter, types, linking, change tracking and archiving. They ship in `assets/wiki/guides/`. **Read `assets/wiki/guides/how-to-document.md` and `how-to-use-this-wiki.md` before writing any page.** That keeps your pages consistent with the rules the repo will hold future agents to.

## Workflow

### 1. Survey (read-only)

Build a picture before changing anything:
- **Shape:** languages, package manifests, top-level directories, entry points, how tests and builds run (manifests, Makefile, CI workflows).
- **Existing documentation:** every markdown/rst/txt doc outside dependency folders, with line counts. Include `docs/`, ADR folders, wiki-like folders, and any existing `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` or `.github/copilot-instructions.md`.
- **Enforcement points:** git or not; existing hooks (`.githooks/`, husky, `.pre-commit-config.yaml`, lefthook); `.github/workflows/`; PR template.
- **History:** `git log --oneline | head -30`, to date decisions and see who works here.

### 2. Interview (one batch, then proceed)

Ask only what you cannot infer, and give a recommended default for each question:
1. **Existing docs** (only if there are any): *migrate* or *greenfield*.
   - Migrate: archive old docs verbatim under `wiki/archive/`, distill their facts into live pages, and slim the README to an entry point.
   - Greenfield: scaffold the wiki beside the existing docs and move nothing.
   - Always let the user choose; never move files without a yes.
2. **Optional directories.**
   - `domain/` is for business or problem-domain semantics: rules, terminology and data meanings that are not about code. Recommend it for apps with real domain logic; skip it for pure libraries and tools.
   - `reviews/` holds audits and code reviews. Recommend it for anything multi-person or long-lived.
3. **Standing rules.** Things agents must never or always do here, such as no secrets, never editing applied migrations, or approval needed before deploys. These seed the project rules in `AGENTS.md` and `product/user-directives.md`.
4. **Tools in use** (Claude Code, Codex, Cursor, others), so you wire the right entry files. If unsure, wire all three; the cost is two tiny files.

If the user has already answered some of these, don't ask them again.

### 3. Scaffold

```bash
python3 <skill-dir>/scripts/scaffold.py --target <repo> --project "<Project Name>" \
    --actor "claude-code/<model-id>" [--with domain,reviews,cursor] [--hook] [--dry-run]
```

Pass `cursor` in `--with` only if the user uses Cursor. The script copies the wiki skeleton and the linter, fills in the date and actor placeholders, and **never overwrites an existing file**: it reports what it skipped. `--hook` installs `.githooks/pre-commit` when none exists. Run with `--dry-run` first if the repo already has a `wiki/` or `scripts/lint_wiki.py`.

Stub pages carry `TODO(llm-wiki)` markers, and the linter warns about each one. The scaffold is finished when no markers remain.

Until step 6 writes them, the linter will also report broken links to `AGENTS.md`, `CLAUDE.md` and `README.md`. Treat those as a checklist, not as a bug.

### 4. Write the seed content

The scaffold gives structure; the value is in content that is true. Read the code, and fill each stub from what you verified:

| Page | Must contain |
| --- | --- |
| `product/goal.md` | Why the project exists, who uses it, what success means, non-goals. One screen. |
| `product/user-directives.md` | The standing rules from the interview, dated, newest first. Setup choices (which tools, which optional folders, greenfield vs migrate) are configuration, not directives; leave them out. |
| `system/architecture.md` | Components, how they talk, where they run, data stores. A table or simple diagram beats prose. |
| `system/code-map.md` | Every top-level module or package: path, what it owns, key entry symbols, its tests. |
| `ops/local-setup.md` | Exact commands to install, run, test and build, copied from what actually works. Run the commands if it is safe and cheap. |
| `decisions/<date>-llm-wiki-documentation.md` | Why this wiki was adopted; context from the survey (how many docs, where facts were scattered). |
| `now.md` | Current branch and state, active work, open questions for the user, next steps. |
| `log.md` | A `Create` entry for the wiki, plus `Deprecate`/`Ingest` entries if you migrated. |

Add more pages where the code clearly has durable concepts (auth, data model, jobs, API, deploy). One concept per page; update an existing page rather than making a second one. Name code by `path/file.py:Symbol`.

Document what exists, not what was left out. If the user doesn't use Cursor or skipped `reviews/`, write nothing about Cursor or reviews. A note like "no Cursor rule" is noise to every future reader, and it goes stale the day someone adds one.

Mark what you verified and what you inferred. "Verified 2026-10-01 by running `npm test`" and "inferred from `config.ts`, not run" are different claims. That honesty is what lets future agents trust the wiki instead of re-reading the code.

Size it to the project. A 2,000-line CLI needs maybe eight pages; a multi-service app may need thirty. Don't invent pages to fill directories.

### 5. Migrate existing docs (only if the user chose it)

Follow `references/migration.md`. In brief:
1. Inventory and classify every doc.
2. Show the user the plan table.
3. `git mv` each superseded doc into `wiki/archive/` and add a frontmatter header; that header is the only edit ever made to it.
4. Distill the facts that are still true into live pages, recording contradictions with dates instead of silently picking one.
5. Slim the README to an entry point and fix inbound links.

### 6. Wire the agents

Follow `references/agent-files.md`, using the templates in `assets/agents/`.

`AGENTS.md` is the single source of agent instructions: the project summary, the wiki session protocol, Karpathy's guidelines, project rules, commands and conventions. `CLAUDE.md` imports it and keeps only Claude-specific additions; Cursor gets an `alwaysApply` rule; Codex reads `AGENTS.md` directly.

If any of these files already exist, merge rather than replace: move shared content into `AGENTS.md` and keep the tool-specific remainder.

### 7. Enforce

Add each item where it fits:
- **Hook.** The `--hook` flag, or append `python3 scripts/lint_wiki.py` to an existing hook (husky script, `.pre-commit-config.yaml` local hook, lefthook). Tell the user to run `git config core.hooksPath .githooks` if you created `.githooks/`; changing their git config is their call.
- **CI.** If `.github/workflows/` exists, add a `python3 scripts/lint_wiki.py` step to the main workflow (any runner has Python 3). Don't create a CI system the repo doesn't have.
- **PR template.** Add the checkbox from `assets/agents/pr-template-checkbox.md` to the existing template, or create `.github/pull_request_template.md` if the repo is on GitHub and has none.

### 8. Verify and hand off

1. Run `python3 scripts/lint_wiki.py`. Fix all errors; clear all `TODO(llm-wiki)` warnings, or list the ones left for the user.
2. Check that every command in `AGENTS.md` matches the repo.
3. Re-read `now.md` as if you were a new agent: could you start work from it?
4. Summarize for the user:
   - Pages created, with a one-line purpose each.
   - What was archived.
   - What was verified versus inferred.
   - Open questions you put in `now.md`.
   - The one-time setup commands for them (e.g. `git config core.hooksPath .githooks`).

Don't commit unless asked. If asked, use a branch, and commit the wiki in focused commits (scaffold, content, migration, wiring).

## Principles

These come from running this setup on a real project; each one prevents a specific failure.

- **The wiki owns *why* and *what was agreed*; the code owns *behavior*.** When they disagree, the code wins and the wiki gets fixed in the same change. Without this rule, docs rot into confident fiction.
- **One owner per fact.** A second copy of a fact will eventually disagree with the first. Other pages link to the owner.
- **Absolute UTC dates everywhere.** "Recently" and "last week" are meaningless to the next session.
- **Nothing is deleted; superseded material is archived.** Agents and humans can then trace why a choice was made, and old reasoning is never silently rewritten.
- **`now.md` is short and rewritten; `log.md` is long and append-only.** Mixing them buries the current state under history.
- **Mechanical checks belong to the linter; semantic checks belong to an agent's lint pass.** Don't try to make the script judge prose.
- **Match the repo's density and tone.** Terse codebase, terse pages.
