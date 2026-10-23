# skills

Agent Skills I use or have written, for Claude Code and other coding agents that read `SKILL.md` folders.

| Skill | What it does |
| --- | --- |
| [llm-wiki](skills/llm-wiki/SKILL.md) | Sets up or migrates a repo's docs into an agent-maintained LLM wiki in Open Knowledge Format, with `AGENTS.md`/`CLAUDE.md`/Cursor wiring and a dependency-free linter in pre-commit and CI. |
| [llm-wiki-audit](skills/llm-wiki-audit/SKILL.md) | Audits an existing LLM wiki: finds reversed decisions still stated as current (pages, `AGENTS.md`, "permanent" code comments), retires superseded records, merges duplicated facts, and asks you to settle conflicts. |

## Install

**Claude Code plugin marketplace** (any machine):

```sh
/plugin marketplace add evanxliu1/skills
/plugin install evan-skills@evanxliu1-skills
```

**Symlinks** (a local clone; edits take effect immediately):

```sh
git clone https://github.com/evanxliu1/skills.git ~/Projects/SKILLS
~/Projects/SKILLS/install.sh   # links skills/* into ~/.claude/skills (and ~/.codex/skills if Codex is installed)
```

Use one method per machine, not both, or the skill is listed twice.

## Layout

```
skills/<name>/SKILL.md        instructions + frontmatter (name, description)
skills/<name>/scripts/        executable helpers
skills/<name>/references/     docs loaded on demand
skills/<name>/assets/         templates copied into target projects
.claude-plugin/marketplace.json
install.sh
```

## Adding a skill

1. Create `skills/<name>/SKILL.md`.
2. Add `"./skills/<name>"` to the `skills` array in `.claude-plugin/marketplace.json`.
3. Re-run `./install.sh`.

## License

MIT. Skill content adapted from third parties keeps its attribution inline.
