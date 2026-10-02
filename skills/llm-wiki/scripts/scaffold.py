"""Scaffold an LLM wiki (Open Knowledge Format) into a repository.

Copies assets/wiki/ to <target>/wiki/ and scripts/lint_wiki.py to
<target>/scripts/lint_wiki.py, filling {{PROJECT}}, {{DATE}}, {{TIMESTAMP}}
and {{ACTOR}}. Optional directories (domain, reviews) are copied only when
requested; template lines tagged `<!-- if:<flag> -->` are kept only when
that flag is passed in --with (domain, reviews, cursor). Never
overwrites an existing file; prints what it created and what it skipped.
Agent files (AGENTS.md, CLAUDE.md, Cursor rule) are written by the agent from
assets/agents/, because they need project-specific content.
"""
import argparse
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
OPTIONAL = {'domain', 'reviews'}  # directories
FLAGS = OPTIONAL | {'cursor'}      # line-level conditions in templates


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--target', required=True, help='repository root')
    parser.add_argument('--project', required=True, help='project display name')
    parser.add_argument('--actor', default='claude-code', help='generated.by value, e.g. claude-code/<model-id>')
    parser.add_argument('--with', dest='optional', default='', help='comma list: domain,reviews (optional dirs), cursor (mention the Cursor rule)')
    parser.add_argument('--hook', action='store_true', help='install .githooks/pre-commit if absent')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    target = Path(args.target).resolve()
    enabled = {d.strip() for d in args.optional.split(',') if d.strip()}
    unknown = enabled - FLAGS
    if unknown:
        parser.error(f'unknown --with values: {sorted(unknown)}; choose from {sorted(FLAGS)}')
    now = datetime.now(timezone.utc)
    values = {
        '{{PROJECT}}': args.project,
        '{{DATE}}': now.strftime('%Y-%m-%d'),
        '{{TIMESTAMP}}': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        '{{ACTOR}}': args.actor,
    }

    def fill(text):
        for key, value in values.items():
            text = text.replace(key, value)
        lines = []
        for line in text.splitlines(keepends=True):
            match = re.search(r'\s*<!-- if:(\w+) -->', line)
            if match:
                if match[1] not in enabled:
                    continue
                line = line[:match.start()] + line[match.end():]
            lines.append(line)
        return ''.join(lines)

    plan = []  # (source, destination, is_template)
    wiki_src = SKILL / 'assets' / 'wiki'
    for src in sorted(wiki_src.rglob('*')):
        if not src.is_file():
            continue
        rel = src.relative_to(wiki_src)
        if rel.parts[0] in OPTIONAL and rel.parts[0] not in enabled:
            continue
        plan.append((src, target / 'wiki' / fill(str(rel)), True))
    plan.append((SKILL / 'scripts' / 'lint_wiki.py', target / 'scripts' / 'lint_wiki.py', False))
    if args.hook:
        plan.append((SKILL / 'assets' / 'agents' / 'pre-commit', target / '.githooks' / 'pre-commit', False))

    created, skipped = [], []
    for src, dest, is_template in plan:
        rel = dest.relative_to(target)
        if dest.exists():
            skipped.append(rel)
            continue
        created.append(rel)
        if args.dry_run:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if is_template:
            dest.write_text(fill(src.read_text(encoding='utf-8')), encoding='utf-8')
        else:
            shutil.copyfile(src, dest)
            if dest.name == 'pre-commit':
                os.chmod(dest, 0o755)

    prefix = 'would create' if args.dry_run else 'created'
    for rel in created:
        print(f'{prefix}: {rel}')
    for rel in skipped:
        print(f'skipped (exists): {rel}')
    print(f'{len(created)} {prefix}, {len(skipped)} skipped. Next: fill TODO(llm-wiki) markers, '
          f'write AGENTS.md/CLAUDE.md from {SKILL / "assets" / "agents"}, run python3 scripts/lint_wiki.py.')


if __name__ == '__main__':
    main()
