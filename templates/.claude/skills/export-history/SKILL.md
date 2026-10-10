---
name: export-history
description: Export, redact and scan the AI session transcripts for sharing, following the redaction policy. Never prints secret or personal values.
disable-model-invocation: true
---

1. Read `{{DOCS}}/ai-history/redaction-policy.md` and `tools/history/redaction-config.json` (create it from the example if missing; ask the owner for the personal values to redact and keep the file git-ignored).
2. `bash tools/history/save-history.sh` to copy this project's local transcripts into `ai-history/raw/` (git-ignored).
3. `python3 tools/history/scan.py ai-history/raw --config tools/history/redaction-config.json` and report categories with file and line counts only. Never print a matched value.
4. `python3 tools/history/redact.py ai-history/raw ai-history/redacted --config tools/history/redaction-config.json`.
5. Re-scan `ai-history/redacted`; every redacted category must show zero hits (`report_only` categories, such as names kept by policy, still show their counts by design). Check that every `.jsonl` line still parses.
6. Write `ai-history/redacted/REDACTIONS.md` with counts per file and category, what was kept on purpose, and what is not included.
7. Package for sharing (zip; split into parts under the share limit if needed) and update the export cells in `{{DOCS}}/ai-history/ai-history-index.md`. Do not upload anywhere without the owner's go.
