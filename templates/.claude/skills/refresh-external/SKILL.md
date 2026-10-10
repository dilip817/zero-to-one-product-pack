---
name: refresh-external
description: Refresh the local snapshots of Google Docs listed in the doc map, so sessions read current partner documents. Never edits the Google Doc.
disable-model-invocation: true
---

1. Run `python3 tools/doccheck.py --docs-dir {{DOCS}}` and list the doc-map rows whose snapshot is missing or older than the limit.
2. For each one, get the current content:
   - If this session has a Google Drive connector, read the document with it and save the text as Markdown to a scratch file outside the repo.
   - Otherwise ask the owner to download it (Docs: File > Download > Markdown; Slides: File > Download > Plain text; Sheets: CSV per tab) and give you the path.
3. `python3 tools/docmap.py snapshot <url> <file> --docs-dir {{DOCS}}` for each. It writes the snapshot, sets the date in the doc map, and suggests a "Requirement IDs" row if the document defines IDs.
4. `git diff -- {{DOCS}}/external/` and summarise what changed in one line per change, naming requirement and decision IDs. Then follow `/sync-docs` from step 3.
5. Commit with `Docs: refresh <document names> snapshots`. Snapshots of partner documents may be confidential: follow the charter's data rules on where they may live.
