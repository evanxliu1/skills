---
type: Decision
title: Use SQLite as the only store
description: SQLite over Postgres.
status: accepted
tags: [decision, storage]
generated: {by: human:evan, at: 2026-02-01T00:00:00Z}
---

# Use SQLite as the only store (2026-02-01)

## Context
Single-user prototype; no ops budget.

## Decision
SQLite file at `data/notes.db`. This is permanent: no database server, ever.

## Status
Accepted 2026-02-01 by human:evan.
