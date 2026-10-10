---
name: kickoff
description: Brownfield kickoff. Reads an existing codebase and fills the existing-system audit and the first pass of the traceability matrix. Read-only on code.
disable-model-invocation: true
---

Audit this repository before any build step. Change no code.

1. **Inventory.** Read the README, build files, CI config, infra and deploy config, env samples (names only, never values), and the top-level source tree. Fill `{{DOCS}}/existing-system-audit.md` §1 to §6: stack, services and boundaries, data stores and schemas, auth and roles, integrations and vendors, analytics and events, design system, deploy and environments.
2. **Baseline.** Run the existing test suites and record exact counts (passed, failed, skipped) and the commands in §7. If something fails before you change anything, record it as pre-existing. Do not fix it.
3. **Conventions.** Record language versions, lint and format rules, branch and review rules, commit style in §8, and copy them into the "Repo conventions" section of `CLAUDE.md` as a proposed change under "Questions for planning" (you do not edit `CLAUDE.md`).
4. **Docs that already exist.** `{{DOCS}}/doc-map.md` holds the installer's proposals (re-run `python3 tools/docmap.py detect --docs-dir {{DOCS}}` for fresh ones). Open every proposed source and check it really plays that role. Search for documents the detector missed (other names, other folders, Google Doc links). For each row, write in Notes what the source covers and what it lacks, and propose the mode (`adopt`, `extend`, `new`, `skip`). Check the "Requirement IDs" table: one row per source of IDs, with a pattern that matches them all and nothing else. Leave `Confirmed` for planning to set. List every Google Doc that needs a snapshot (§9).
5. **Seams.** Name the places where new work can attach without editing partner code: interfaces, adapters, feature flags, routes (§10).
6. **Traceability.** For each requirement ID from every source in the doc map's "Requirement IDs" table (or, before any exists, each capability in the `thesis` role), add a row to `{{DOCS}}/traceability.md` with status `exists`, `partial`, `missing` or `conflicts`, the file and line that show it, and the test that covers it (or "none").
7. **Risks and do-not-touch** (§11, §12): fragile areas, missing tests, compliance-sensitive code, partner-owned paths.
8. **Report**: a one-screen summary, the counts per status, the top five gaps, and questions for the partner. Commit the audit, the doc map and the matrix with `Docs: kickoff audit`. Do not apply the map: planning confirms rows, then runs the installer with `--apply-map`.
