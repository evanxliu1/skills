---
type: Runbook
title: Local setup
description: Run the API locally.
status: stable
tags: [setup]
generated: {by: human:evan, at: 2026-02-01T00:00:00Z}
---

# Local setup

1. `python3 -m venv .venv && . .venv/bin/activate`
2. Create the SQLite database: `python3 -m notes init` (writes `data/notes.db`).
3. `python3 -m notes`

Architecture: [overview](../system/architecture.md).
