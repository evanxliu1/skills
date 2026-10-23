---
type: Decision
title: Rate limit API keys at 100/min
description: Per-key limit of 100 requests per minute.
status: accepted
tags: [decision, api]
generated: {by: human:evan, at: 2026-03-01T00:00:00Z}
---

# Rate limit API keys at 100/min (2026-03-01)

## Decision
100 requests per minute per API key, enforced in `src/limits.py`.

## Status
Accepted 2026-03-01 by human:evan.
