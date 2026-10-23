---
type: Decision
title: Move storage to Postgres
description: Postgres over SQLite, for concurrent writers.
status: accepted
tags: [decision, storage]
generated: {by: human:evan, at: 2026-06-15T12:00:00Z}
---

# Move storage to Postgres (2026-06-15)

## Context
Several API workers now write concurrently; SQLite write locks caused timeouts.

## Decision
Postgres, configured by `DATABASE_URL` (default `postgresql://localhost:5432/notes`).

## Status
Accepted 2026-06-15 by human:evan.
