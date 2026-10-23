---
type: System Component
title: Architecture
description: Components and data flow.
status: stable
tags: [architecture]
generated: {by: human:evan, at: 2026-02-01T00:00:00Z}
---

# Architecture

One Python process serves the HTTP API (`src/`) and talks to the store in `src/store.py`.

Notes are stored in a single SQLite file at data/notes.db which the API process opens on startup and keeps open for the life of the process, so there is no separate database server to run.

Rate limiting is 100 requests per minute per API key, decided in [rate limits](../decisions/2026-03-01-rate-limit.md).

See [storage](storage.md).
