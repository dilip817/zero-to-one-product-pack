---
name: sync-docs
description: Use after an updated planning file has been dropped into the repo. Reports what changed and what it means for the build, without changing code.
disable-model-invocation: true
---

An updated planning file, a changed partner document, or a new Google Doc snapshot is in this repository.

1. `git status` and `git diff -- CLAUDE.md {{DOCS}}/ .claude/`, plus `git diff` on every local source in `{{DOCS}}/doc-map.md` (partner documents and `{{DOCS}}/external/` snapshots), to see what changed.
2. Summarise each change in one line: the decision or requirement ID (from any source in the doc map), and what is different now. Name requirement IDs that appeared or disappeared in a partner document or snapshot.
3. List what in the code, tests or traceability matrix no longer matches, with file names. Do not fix anything yet.
4. Say whether the change fits inside the current step or needs its own session.
5. Commit the dropped-in files on their own, exactly as they are, with the message `Docs: <what changed>`.
