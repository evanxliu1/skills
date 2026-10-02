@AGENTS.md

# Claude Code notes

- `AGENTS.md` above is the shared instruction set for every agent; keep this file to Claude-specific additions.
- <If nested: `<dir>/CLAUDE.md` imports its directory's `AGENTS.md` and loads automatically when you work there.>
- Long-term memory lives in `wiki/` (start with `wiki/now.md`). Claude's private auto-memory is for personal working notes only; anything a teammate or another tool should know goes in the wiki.
- Run `python3 scripts/lint_wiki.py` before finishing any task that touched `wiki/`.
