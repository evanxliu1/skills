---
type: Product
title: User directives
description: Dated record of every explicit authorization, prohibition and preference the owner has given, with its scope and source.
status: stable
tags: [product, directives, memory]
generated:
  by: {{ACTOR}}
  at: {{TIMESTAMP}}
---

# User directives

Standing instructions from the owner that are in force, newest first. When a directive changes, replace its row; the change is in `log.md` and, for a real choice, a superseding decision record. Agents add a row whenever the user authorizes, forbids or prefers something; non-obvious choices also get a [decision record](../decisions/index.md). The one-line versions agents must always see live in [`AGENTS.md`](../../AGENTS.md) under Project rules.

| Date | Directive | Scope | Source |
| --- | --- | --- | --- |
| {{DATE}} | Keep project knowledge in `wiki/`; agents read `now.md` first and update the wiki last. | All agents, all tasks | [Decision](../decisions/{{DATE}}-llm-wiki-documentation.md) |

<!-- TODO(llm-wiki): add the standing rules gathered while setting up the wiki, one row each, including the retention choice (delete or archive retired pages and superseded decisions). -->
