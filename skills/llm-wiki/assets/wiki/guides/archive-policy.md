---
type: Guide
title: Retention and archive policy
description: How retired pages and superseded decisions leave the live wiki (deleted or archived), and the immutability rule for archived sources.
status: stable
tags: [guide, wiki, archive]
generated:
  by: {{ACTOR}}
  at: {{TIMESTAMP}}
---

# Retention and archive policy

Live pages state the current truth only. Retired material (a page another page fully replaces, a superseded decision record) leaves the live wiki in one of two ways, chosen once per repo and recorded in [user directives](../product/user-directives.md):

- **Delete.** `git rm` it. Git history and the superseding page or record are the trace.
- **Archive.** Move it to `wiki/archive/`, the immutable raw-source layer.

Pre-wiki documents moved in during a migration are always archived, because the user chose to keep them.

## What belongs here

- Pre-wiki documents (plans, briefs, audits, proposals, setup logs) moved verbatim when the wiki was adopted.
- When the repo archives: wiki pages that a newer page fully replaces, and superseded decision records (`status: superseded`, `superseded_by` the new record).
- Data artifacts and local state are never in the wiki; if they are gitignored, pages reference them by path and say so.

## How to archive

1. `git mv` the file into `wiki/archive/`, keeping its name; add a date suffix only if the name would collide (`README-2026-01-31.md`).
2. Prepend a frontmatter block (this is the only edit ever made to the file): `type: Source Document` (or the page's original type), `status: deprecated`, `archived: <UTC date>`, `superseded_by: <link(s)>`, plus a one-line blockquote pointing to this policy. The body below the header is never edited again, not even to fix a typo or a broken link.
3. Make sure the superseding page lists the archived file in `sources` and carries every fact from it that is still true.
4. Add the file to `archive/index.md` with what it was and what replaced it. Append a `Deprecate` entry to `log.md`.
5. Fix inbound links in live pages and code (error messages, rendered reports) to point at the archived path or the new page.

## How to delete

1. Make sure the superseding page carries every fact from the retired one that is still true; a superseding decision names the old record in its **Supersedes** section.
2. `git rm` the file and remove its index entry.
3. Fix inbound links in live pages and code; the linter reports each one as broken.
4. Append a `Deprecate` entry to `log.md` naming the deleted path in backticks (not a link) and what replaced it.

## Linting

`scripts/lint_wiki.py` still requires frontmatter with `type` and `superseded_by` on archived pages and lists them in `archive/index.md`, but it does not report broken links inside archived bodies or `log.md`: those links describe where things were on their date.

## Reading the archive

Archived documents describe the world as it was on their date. Quote them for history and evidence; do not treat them as current instructions. If an archived fact is still true and missing from a live page, that is an ingest task for the live page, not a reason to edit the archive.
