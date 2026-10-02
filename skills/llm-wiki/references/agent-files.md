# Agent entry files

One instruction set, many tools. `AGENTS.md` is the shared source of truth; every other agent file is a thin pointer or importer so instructions cannot drift between tools.

| File | Read by | Content |
| --- | --- | --- |
| `AGENTS.md` (root) | Codex, Cursor, Copilot, Jules, Amp, Gemini CLI and others natively; Claude Code via import | Everything shared |
| `CLAUDE.md` (root) | Claude Code | `@AGENTS.md` on the first line, then Claude-only notes |
| `.cursor/rules/agents.mdc` | Cursor | `alwaysApply: true` rule restating the session protocol and pointing at `AGENTS.md` |
| `<subdir>/AGENTS.md` + `<subdir>/CLAUDE.md` | Tools that load nested files when working in that directory | Short directory-specific rules; the CLAUDE.md is just `@AGENTS.md` |

Templates are in `assets/agents/`. Fill every `<…>` placeholder from the survey and interview; delete sections that do not apply rather than leaving them empty.

## Writing `AGENTS.md`

Order and purpose of sections (template: `assets/agents/AGENTS.md`):

1. **Intro line** — what this file is and which tools read it.
2. **What this project is** — one paragraph: purpose, users, deployment(s). A table if there is more than one runtime or deployment. Agents need this to judge risk.
3. **The wiki is the memory** — the session protocol (start / work / finish) and links to the four guides. Keep the protocol wording close to the template; it is what makes the wiki self-maintaining.
4. **Behavioral guidelines** — Karpathy's four (think before coding, simplicity first, surgical changes, goal-driven execution) with attribution. Keep them; tune one or two sentences to the repo's style ("this codebase is dense and terse; keep it that way").
5. **Project rules** — the standing directives from the interview, each one line, bold lead-in. Link to `wiki/product/user-directives.md` as the dated record. Only rules that are true and enforced; an aspirational rule teaches agents that rules are optional.
6. **Commands** — copy-pasteable setup, run, test, build, lint (including `python3 scripts/lint_wiki.py`). Verify each exists in the repo. Annotate with counts or prerequisites when useful ("needs Postgres on 5432").
7. **Conventions** — language style, test layout, error-message tone, branch/PR naming, and the documentation rule (facts go in the owning wiki page; the allowed root markdown list).

Keep it under roughly 150 lines. Detail belongs in wiki pages it links to.

## Merging with existing files

- Existing `CLAUDE.md` with real content: move shared content into `AGENTS.md`, replace `CLAUDE.md` with the import plus whatever was genuinely Claude-specific (slash commands, skill notes, memory notes).
- Existing `.cursorrules` (legacy): fold into `AGENTS.md`, add the `.mdc` rule, and tell the user the legacy file can be removed (do not delete it yourself without a yes).
- Existing `AGENTS.md`: restructure into the template's sections, preserving every rule; add the session protocol.
- Existing `.github/copilot-instructions.md`: reduce to a pointer to `AGENTS.md` if the user agrees.

## Nested files

Add a directory `AGENTS.md` only when a subtree has rules the root does not (its own runtime, test command, security boundary, or contract). Format: one "Read first" line linking the wiki pages for that area, then 4–8 bullets. Pair each with a `CLAUDE.md` containing only `@AGENTS.md`. Mention the nested files in root `CLAUDE.md` so Claude knows they exist.

## Claude memory

Claude Code's private auto-memory is per-user and invisible to teammates and other tools. Root `CLAUDE.md` should say: the wiki is the long-term memory; private memory is for personal working notes only; anything another person or tool should know goes in the wiki.
