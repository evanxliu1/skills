---
type: System Component
title: Storage
description: Where notes are stored.
status: stable
tags: [storage]
generated: {by: human:evan, at: 2026-06-15T12:00:00Z}
---

# Storage

Until 2026-06-15 the app used SQLite; on 2026-06-15 the owner chose Postgres (see [decision](../decisions/2026-06-15-postgres-storage.md)). The SQLite choice is recorded in [the original decision](../decisions/2026-02-01-sqlite-storage.md).

Notes are stored in a single SQLite file at data/notes.db which the API process opens on startup and keeps open for the life of the process, so there is no separate database server to run.

`DATABASE_URL` in `src/store.py` selects the database.
