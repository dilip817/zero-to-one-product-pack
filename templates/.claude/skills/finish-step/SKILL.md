---
name: finish-step
description: End a build session. Runs the tests, checks the step's "Done when", updates progress, traceability and the AI history index, commits, and prints the hand-back.
disable-model-invocation: true
---

Close out this session's step.

1. **Test.** {{BUILD_COMMAND}}; {{UNIT_TEST_COMMAND}}; {{END_TO_END_COMMAND}}. In a brownfield repo also run the baseline suite recorded in the audit and compare counts. Never finish on failing tests.
2. **Check "Done when."** For each item on the card, say whether it passes and what shows it.
3. **Check the diff.** `git status`, `git diff --stat`. Confirm: no secrets; no planning-only file changed (`CLAUDE.md`, `.claude/`, `{{DOCS}}/overlays/`, and every role file the doc map lists); no partner document mapped `adopt` or `extend` changed; no snapshot in `{{DOCS}}/external/` edited by hand; no partner-owned path changed without sign-off on the card.
4. **Update `{{DOCS}}/progress.md`:** step status, what exists, what is next, questions for planning, a session-log row.
5. **Update `{{DOCS}}/traceability.md`:** every requirement this step touched, whichever source its ID comes from (the doc map's "Requirement IDs" table), with its new status, code location and test.
6. **Add a row to `{{DOCS}}/ai-history/ai-history-index.md`.**
7. **Run** `python3 tools/doccheck.py --docs-dir {{DOCS}}` and fix what it flags in files you own.
8. **Commit** on `{{WORK_BRANCH}}`. The message names the step and says what changed and why. Ask before pushing unless the contract says otherwise.
9. **Print the hand-back** (short enough to paste into the planning chat): what was built, test results, "Done when" status, questions for planning word for word, what the next session will do.

Do not start the next step.
