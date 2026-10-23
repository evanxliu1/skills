"""Shortlist candidates for an llm-wiki audit. It finds; the agent judges.

Sections:
  decisions   every decision record with status, supersedes/superseded_by, tags
  retired     superseded/reversed/archived decisions still cited by live pages or code
  competing   accepted decisions sharing a topic tag with no supersedes link between them
  markers     "permanent" / "do not change" style lines, and whether they cite a decision
  history     inline history in live pages ("until 2026-…", "previously", "no longer")
  duplicates  near-identical paragraphs on different live pages
  size        line count of live pages (compare before and after the audit)

Dependency-free. Repository files come from `git ls-files`; outside git only
the wiki is scanned.

Usage: python3 find_stale.py [--repo .] [--wiki wiki] [--since <git-rev>]
  --since limits markers, history and duplicates to files changed since <git-rev>.
"""
import argparse
import re
import subprocess
from itertools import combinations
from pathlib import Path

RETIRED = {'deprecated', 'superseded', 'reversed'}
GENERIC_TAGS = {'decision', 'wiki', 'product', 'system', 'ops', 'domain'}
MARKER = re.compile(r"\b(permanent(ly)?|do not (change|remove|touch|modify)|don'?t (change|remove|touch)"
                    r"|never (change|remove|switch)|must always|forever|by design|intentional(ly)?)\b", re.I)
HISTORY = re.compile(r'\b(until \d{4}-\d{2}-\d{2}|previously|used to|no longer|formerly|originally'
                     r'|was (changed|replaced|switched|moved)|we switched|instead of the old)\b', re.I)
SKIP_LIVE = ('archive', 'guides', 'log.md')


def frontmatter(text):
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---', 4)
    fields = {}
    for line in text[4:end if end > 0 else 0].splitlines():
        match = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if match:
            fields[match[1]] = re.sub(r'\s+#.*$', '', match[2]).strip().strip('"\'')
    return fields


def body(text):
    if text.startswith('---\n'):
        end = text.find('\n---', 4)
        if end > 0:
            return text[end + 4:]
    return text


def git(repo, *args):
    try:
        return subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True).stdout.decode()
    except (OSError, subprocess.CalledProcessError):
        return None


def repo_files(repo, wiki):
    listed = git(repo, 'ls-files', '-z', '--cached', '--others', '--exclude-standard')
    if listed is None:
        return []
    files = []
    for name in filter(None, listed.split('\0')):
        path = (repo / name).resolve()
        if wiki in path.parents or not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            files.append((name, path.read_text(encoding='utf-8')))
        except (UnicodeDecodeError, OSError):
            pass
    return files


def tags(fm):
    return {t.strip().strip('"\'') for t in fm.get('tags', '').strip('[]').split(',') if t.strip()} - GENERIC_TAGS


def paragraphs(text):
    for para in re.split(r'\n\s*\n', re.sub(r'```.*?```', '', text, flags=re.S)):
        words = re.findall(r'[a-z0-9_]+', para.lower())
        if len(words) >= 12 and not para.lstrip().startswith(('#', '|', '* [')):
            yield para.strip(), {' '.join(words[i:i + 3]) for i in range(len(words) - 2)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--wiki', default='wiki')
    ap.add_argument('--since')
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    wiki = (repo / args.wiki).resolve()
    pages = {p: p.read_text(encoding='utf-8') for p in sorted(wiki.rglob('*.md'))}
    rel = {p: p.relative_to(wiki).as_posix() for p in pages}
    live = {p: t for p, t in pages.items() if p.relative_to(wiki).parts[0] not in SKIP_LIVE}
    files = repo_files(repo, wiki)
    changed = None
    if args.since:
        diff = git(repo, 'diff', '--name-only', args.since, '--')
        changed = {(repo / n).resolve() for n in (diff or '').split()}

    def in_scope(path):
        return changed is None or path in changed

    decisions = {p: frontmatter(t) for p, t in pages.items() if frontmatter(t).get('type') == 'Decision'}
    print('## decisions')
    for p, fm in decisions.items():
        links = ' '.join(f'{k}={fm[k]}' for k in ('supersedes', 'superseded_by') if fm.get(k))
        print(f'{rel[p]}  status={fm.get("status", "accepted")}  tags={sorted(tags(fm))}  {links}'.rstrip())

    print('\n## retired')
    for p, fm in decisions.items():
        if fm.get('status') not in RETIRED and p.parent.name != 'archive':
            continue
        hits = [rel[q] for q, t in live.items()
                if p.name in body(t) and frontmatter(t).get('type') != 'Decision']
        hits += [f'{name}:{n}' for name, text in files
                 for n, line in enumerate(text.splitlines(), 1) if p.name in line]
        for hit in hits:
            print(f'{rel[p]} cited by {hit}')

    print('\n## competing')
    accepted = [(p, fm) for p, fm in decisions.items()
                if fm.get('status', 'accepted') == 'accepted' and p.parent.name == 'decisions']
    for (a, fa), (b, fb) in combinations(accepted, 2):
        shared = tags(fa) & tags(fb)
        linked = a.name in pages[b] or b.name in pages[a]
        if shared and not linked:
            print(f'{rel[a]} <> {rel[b]}  shared tags {sorted(shared)}')

    print('\n## markers')
    sources = [(rel[p], t, p) for p, t in live.items()] + [(n, t, (repo / n).resolve()) for n, t in files]
    for name, text, path in sources:
        if not in_scope(path):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if MARKER.search(line):
                cited = 'cites decision' if 'decisions/' in line else 'NO decision cited'
                print(f'{name}:{n}  [{cited}]  {line.strip()[:140]}')

    print('\n## history')
    for p, text in live.items():
        if not in_scope(p) or frontmatter(text).get('type') == 'Decision':
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if HISTORY.search(line):
                print(f'{rel[p]}:{n}  {line.strip()[:140]}')

    print('\n## duplicates')
    paras = [(p, para, shingles) for p, t in live.items() if p.name != 'log.md'
             for para, shingles in paragraphs(body(t))]
    for (pa, ta, sa), (pb, tb, sb) in combinations(paras, 2):
        if pa == pb or not (in_scope(pa) or in_scope(pb)):
            continue
        score = len(sa & sb) / len(sa | sb)
        if score >= 0.5:
            print(f'{rel[pa]} ~ {rel[pb]}  ({score:.2f})  "{ta[:90]}"')

    print('\n## size')
    print(f'{len(live)} live pages, {sum(t.count(chr(10)) for t in live.values())} lines')


if __name__ == '__main__':
    main()
