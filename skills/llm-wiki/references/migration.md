# Migrating existing documentation

Use this only when the user chose *migrate*. The goal: every fact that is still true ends up in exactly one live wiki page; every superseded document survives verbatim in `wiki/archive/` so history and reasoning stay traceable.

## 1. Inventory

List every documentation file (exclude `node_modules/`, `vendor/`, `.venv*/`, build output, generated API docs, licence files and changelogs maintained by release tooling). For each, record path, line count, last commit date (`git log -1 --format=%cs -- <file>`) and a one-line summary.

## 2. Classify

| Class | Typical files | Action |
| --- | --- | --- |
| **Entry point** | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `CODE_OF_CONDUCT.md` | Keep at root (GitHub expects them). Archive the current version as `README-<date>.md` if you rewrite it substantially; slim to a pointer into `wiki/`. |
| **Agent instructions** | `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`, old `AGENTS.md` | Merge into the new `AGENTS.md` (see agent-files.md); archive the old text only if it carried real history. |
| **Living reference** | architecture notes, setup guides, API docs written by hand, glossaries | Distill into the owning live pages, then archive the original. |
| **Historical** | plans, proposals, briefs, audits, meeting notes, RFCs, ADRs | Archive verbatim. ADRs that are still in force also get a `decisions/` record that links back to the archived original (or move them directly into `decisions/` if they already have context/decision/consequence structure; add frontmatter, keep the body). |
| **Tool-managed** | files owned by a generator or design tool, changelogs written by release tooling | Leave in place; link from `wiki/index.md` under "Outside the wiki". |

## 3. Show the plan, get a yes

Present a table: file → class → destination → which live pages absorb its facts. Moving files is reversible but noisy; the user decides. Note anything you are unsure about.

## 4. Archive

For each archived file:

1. `git mv <file> wiki/archive/<NAME>.md` — keep the original name; add `-<YYYY-MM-DD>` only on collision (e.g. `README-2026-10-01.md`). Non-markdown evidence (JSON reports, CSVs) may also be archived if a page cites it.
2. Prepend the header — the only edit ever made to the file:

```markdown
---
type: Source Document
title: <original title> (<date it describes>)
description: <what it was>; historical reference only.
status: deprecated
archived: <YYYY-MM-DD>
superseded_by: <relative link(s) to live page(s)>
tags: [archive, source]
generated:
  by: <original author or "human:<id> (pre-wiki)">
  at: <archive timestamp, UTC>
---

> Archived under the [archive policy](../guides/archive-policy.md). Describes the project as of <date>; not current instructions.
```

3. Add it to `wiki/archive/index.md`, grouped by era, newest first, with what it was and what superseded it.

Never fix typos, links or errors inside an archived body. If the archived doc contains a known factual error, say so in the blockquote, not in the body.

## 5. Distill

For each live page that absorbs facts:

- List the archived source in `sources`.
- Carry over only facts that are still true; verify against code where cheap.
- When sources disagree with each other or with the code, resolve it rather than carrying both into a live page. Behavior: the code wins. A choice that changed over time: the live page states the current one, and a decision record (with a **Supersedes** line for the old choice) holds the why. Unclear which is current: list it for the user in the plan table and ask; do not pick silently.
- Choices with reasoning found in old docs become `decisions/` records dated when the choice was made (from git history or the doc), marked as recorded retroactively.
- Standing instructions found in old docs go into `product/user-directives.md` with their original date.

## 6. Fix links and entry points

- `grep -rn` the repo (code, configs, error messages, templates) for paths to moved files and update them.
- Rewrite `README.md` as an entry point: one paragraph on what the project is, where the docs live (`wiki/index.md`, `wiki/now.md`), agent entry (`AGENTS.md`), quickstart commands. Facts beyond that belong in the wiki.
- Restrict root markdown going forward: record the allowed list in `AGENTS.md` → Conventions.

## 7. Log it

Append to `log.md` under today's date: one `Deprecate` bullet per archived file (or one grouped bullet listing them), one `Ingest` bullet per absorbing page, and the `Create` bullet for the wiki itself.
