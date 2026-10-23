---
okf_version: "0.2"
---

# {{PROJECT}} wiki

The project's long-term memory. Start with [`now.md`](now.md), then the directory you need. Schema: [`AGENTS.md`](../AGENTS.md) and [guides](guides/index.md). History: [`log.md`](log.md).

## Start here

* [now.md](now.md) — current state, active work, open questions, next steps (working memory).
* [Goal](product/goal.md) — why the project exists and who it serves.
* [Architecture](system/architecture.md) — components, runtimes and how they connect.
* [Code map](system/code-map.md) — every module and what it owns.
* [User directives](product/user-directives.md) — dated record of what the owner authorized, forbade or prefers.

## Directories

* [product/](product/index.md) — goal, users, workflow, user directives, roadmap.
* [domain/](domain/index.md) — problem-domain rules, terminology and data semantics. <!-- if:domain -->
* [system/](system/index.md) — architecture, code map and component pages.
* [ops/](ops/index.md) — runbooks: setup, deploy, maintenance.
* [decisions/](decisions/index.md) — dated decision records with context, options, decision, consequences, status.
* [reviews/](reviews/index.md) — audits and code reviews. <!-- if:reviews -->
* [guides/](guides/index.md) — how to use, document, track changes, retire material.
* [archive/](archive/index.md) — immutable archived documents.

## Outside the wiki

* [`README.md`](../README.md) — human entry point and quickstart.
* [`AGENTS.md`](../AGENTS.md), [`CLAUDE.md`](../CLAUDE.md) — agent instructions.
* `.cursor/rules/agents.mdc` — Cursor rule pointing at `AGENTS.md`. <!-- if:cursor -->
