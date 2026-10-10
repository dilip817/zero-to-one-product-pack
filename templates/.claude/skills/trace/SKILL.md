---
name: trace
description: Refresh the traceability matrix against the current code and tests, and report requirements without a passing test or a named manual check.
disable-model-invocation: true
---

1. Read `{{DOCS}}/doc-map.md` ("Requirement IDs": every source and its ID pattern; a URL source is read through its snapshot), each of those sources, and `{{DOCS}}/traceability.md`.
2. For every requirement ID: confirm the code location still exists, find the test that covers it, run that test, and set the status (`exists`, `partial`, `missing`, `conflicts`) and the "Verified by" cell.
3. Add rows for requirement IDs that are missing from the matrix; flag rows whose ID no longer exists in any source.
4. Run `python3 tools/doccheck.py --docs-dir {{DOCS}}`.
5. Report: counts per status, requirements with no test and no named manual check, and any conflict between a requirement source and the code. Change no code.
