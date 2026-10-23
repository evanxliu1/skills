# AGENTS.md — Notes API

Small HTTP API for shared notes. Read `wiki/now.md` and `wiki/index.md` first; update the wiki last.

## Project rules

- **Storage is SQLite, permanently.** Do not add a database server. See wiki/decisions/2026-02-01-sqlite-storage.md.
- **Never commit `.env`.**

## Commands

```sh
python3 -m notes            # run
python3 scripts/lint_wiki.py
```
