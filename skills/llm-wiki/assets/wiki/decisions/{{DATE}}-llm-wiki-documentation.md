---
type: Decision
title: Adopt an LLM wiki (Open Knowledge Format) plus AGENTS.md as the documentation and memory system
description: Keep project knowledge in a wiki/ bundle that agents read first and update last, governed by AGENTS.md and four guides, with a linter in the hook and CI.
status: accepted
tags: [decision, documentation, agents, wiki]
generated:
  by: {{ACTOR}}
  at: {{TIMESTAMP}}
sources:
  - resource: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    title: Karpathy, LLM wiki pattern
  - resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
    title: Open Knowledge Format v0.2
  - resource: https://github.com/multica-ai/andrej-karpathy-skills
    title: Karpathy behavioral guidelines for coding agents
---

# Adopt an LLM wiki plus AGENTS.md ({{DATE}})

## Context

<!-- TODO(llm-wiki): what the documentation looked like before (files, line counts, where facts were scattered), which agents are used, and who asked for this. -->

## Options considered

| Option | Fit | Why not / why |
| --- | --- | --- |
| Keep existing docs, add `AGENTS.md` only | Cheapest | Agents keep re-deriving facts each session; no change tracking or memory loop |
| Conventional `docs/` folder | Familiar | No governing schema, no index/log discipline, no ingest/query/lint operations; drifts |
| **LLM wiki in OKF under `wiki/`, governed by `AGENTS.md`** (chosen) | Agent-maintained, git-native, renders on GitHub and in Obsidian | More files; needs the linter and the session protocol to stay healthy |
| External knowledge tool (Notion, vector store) | Nice UI | Not versioned with the code; needs accounts or SDKs |

## Decision

- `wiki/` holds `index.md` (catalog), `log.md` (newest-first history), `now.md` (working memory) and category directories. One concept per file, YAML frontmatter with `type` required and OKF provenance fields, relative links.
- `AGENTS.md` is the schema and behavioral contract for every tool; `CLAUDE.md` imports it.
- Cursor has an `alwaysApply` rule in `.cursor/rules/agents.mdc` pointing at `AGENTS.md`. <!-- if:cursor -->
- Agents follow the session protocol: read `now.md` and `index.md` first; finish by updating `now.md`, `log.md`, affected pages and decision records.
- Live pages state only the current truth. Retired pages and superseded decisions are <deleted | archived under `wiki/archive/`> per the retention directive; pre-wiki documents are archived verbatim. Code and pages cite decisions by link instead of restating them. <!-- TODO(llm-wiki): fill in the retention choice. -->
- `scripts/lint_wiki.py` enforces structure in the pre-commit hook and CI where available.

## Consequences

- Every behavior, setup or contract change includes a wiki change in the same diff.
- New sessions start from `now.md` instead of re-reading the codebase.

## Status

Accepted {{DATE}}.
