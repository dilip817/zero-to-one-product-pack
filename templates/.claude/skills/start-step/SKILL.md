---
name: start-step
description: Start a build session. Reads the hand-off docs, names the one step for this session, and writes a plan to approve before any file is changed.
disable-model-invocation: true
argument-hint: "[step number, optional]"
---

Start a build session. Requested step, if any: $ARGUMENTS

1. **Read**, in this order: `CLAUDE.md`, `{{DOCS}}/doc-map.md` (or run `python3 tools/docmap.py show --docs-dir {{DOCS}}`), the `decisions` role, `{{DOCS}}/progress.md`, the `plan` role. Each role means what the doc map resolves it to: the source, its overlay, and for a Google Doc the local snapshot. In the `thesis` role read only the core (or the thesis overlay) plus any section the step card points to; read the requirement sources for the IDs the step names. In a brownfield repo also read `{{DOCS}}/existing-system-audit.md` and the rows of `{{DOCS}}/traceability.md` this step touches.
2. **Check the repo.** `git status` and `git log --oneline -5`. You should be on `{{WORK_BRANCH}}` with a clean tree. If not, stop and say so.
3. **Pick one step.** The requested number, or the first step in `progress.md` that is not done.
4. **Reply with a plan:**
   - **Step:** number, name, change type (`new`, `extend`, `replace`, `remove`), and its "Done when" quoted from §6.1.
   - **Constrained by:** decision IDs and requirement IDs.
   - **Existing behaviour to keep** (brownfield): what must not change, and the regression check that proves it.
   - **Plan:** files to create or change, tests to add, how each "Done when" item will be checked.
   - **Not doing:** nearby work that is out of scope.
   - **Questions for planning:** gaps or conflicts between files (including between a partner document and its overlay), snapshots older than the doc map's limit, and whether each blocks the step.
5. **Wait for approval.** Change no file until the plan is approved.

Do not invent a policy, price, capability or vendor feature to fill a gap: ask.
