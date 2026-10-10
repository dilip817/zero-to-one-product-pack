# CLAUDE.md

Instructions for Claude Code working in this repository.

<!-- guide: This is the build agent's operating contract. Keep it short. In a brownfield repo, merge these sections into the partner's existing CLAUDE.md (or equivalent) instead of replacing it. -->

## What this is

{{ONE_PARAGRAPH: what is being built, for whom, with which partner, and what it is not (concept, MVP, production).}}

{{DATA_RULE: e.g. "All data is synthetic. Never add real customer information."}}

## The files are the hand-off

Thinking and decisions happen in {{PLANNING_TOOL}}. You build. The only things carried between the two are the files below. Do not rely on anything from an earlier session. If it isn't in these files, you don't know it.

**Start with `{{DOCS}}/doc-map.md`.** It says where each kind of document lives: the pack's file (mode `new`), a partner document that stays the source of truth plus an overlay with what it lacks (`adopt`, `extend`), or nothing (`skip`). When this file names a role, read what the doc map resolves it to: the source, its overlay, and for a Google Doc the local snapshot. `python3 tools/docmap.py show --docs-dir {{DOCS}}` prints the resolved list.

| Role or file | What it is | Who edits it |
|---|---|---|
| `{{DOCS}}/doc-map.md` | Where each role lives, which requirement IDs are traced, snapshot dates | Planning confirms; you propose rows in `/kickoff` and update snapshot dates |
| `decisions` role (default `{{DOCS}}/decisions.md`) | One line per decision. The latest line wins over everything else | Planning only |
| `plan` role (default `{{DOCS}}/implementation-plan.md`) | Requirements (§3), design (§4), step cards (§6.1), checklist (§6.2), acceptance (§7) | Planning only |
| `requirements` role | Requirement IDs from every source in the doc map's "Requirement IDs" table | Planning only |
| `thesis` role (default `{{DOCS}}/product-thesis.md`) | The why. Read the "Core thesis" and any section the plan points to | Planning only |
| `charter`, `data-model`, `design`, `evals`, `research` roles | As named; each resolves through the doc map | Planning only |
| Partner documents mapped `adopt` or `extend` | The partner's own PRD, schema, ADRs, evals, design docs | **The partner.** Never edit them from a session |
| `{{DOCS}}/overlays/*` | What a partner document lacks, beside it | Planning only |
| `{{DOCS}}/external/*` | Read-only snapshots of Google Docs | Refreshed with `/refresh-external`; never edited by hand |
| `CLAUDE.md`, `.claude/` | This contract and the session skills | Planning only |
| `{{DOCS}}/existing-system-audit.md` | What already exists (brownfield) | **You**, after `/kickoff`; planning reviews |
| `{{DOCS}}/traceability.md` | Requirement → code → test → status | **You** |
| `{{DOCS}}/progress.md` | Where the build is, last session, questions for planning | **You** |
| `{{DOCS}}/ai-history/ai-history-index.md` | One row per AI session | **You** add a row per session |
| `README.md`, code, tests, design and eval working files | The product | **You** |

**Never edit a file marked "Planning only" or a partner document.** If one is wrong, incomplete or conflicts with another, stop and write the question in `{{DOCS}}/progress.md` under "Questions for planning."

## Every session, in this order

1. **Read** `CLAUDE.md`, `{{DOCS}}/doc-map.md`, the `decisions` role, `{{DOCS}}/progress.md`, then the `plan` role. If a snapshot you rely on is older than the doc map's limit, say so in the plan.
2. **Name the step.** One step from §6.1 per session: the next one `progress.md` shows as not done.
3. **Plan before coding.** Files to touch, tests to add, how you will check "Done when". Wait for approval.
4. **Build** only what the step card asks for.
5. **Test.** {{TEST_COMMANDS_SUMMARY}}. Do not finish with failing tests.
6. **Update** `progress.md`, `traceability.md`, and add a row to the AI history index.
7. **Commit** to `{{WORK_BRANCH}}` with a message that names the step and says why.
8. **Stop.** Do not start the next step.

## Rules that are not negotiable

<!-- guide: Keep the ones that apply, delete the rest, add the project's own. These came from a regulated-domain build; most generalise. -->

- **Fixed rules decide eligibility and safety.** No model output is ever an input to them.
- **The model returns keys from fixed tables only.** Nothing the model writes is shown to a user, except a verbatim quote of the user's own words.
- **Screen before the model** for {{SAFETY_CLASS}} on every free-text entry. A message that trips it is never used for suggestions.
- **Fail closed.** An error never moves a user forward. The fallback is {{FALLBACK}}.
- **Never invent a policy, price, capability or vendor feature.** User-facing copy states only what the `plan` role §{{ALLOWED_FACTS_SECTION}} lists. If you need a fact that isn't in the docs, ask.
- **Fixed wording stays fixed:** {{FIXED_WORDING_CLASSES e.g. legal, crisis, policy}}.
- **Label every mock** on screen and in the README.
- **No secrets in the repo.** Keys are read on the server only.
- **Partner-owned areas:** {{PATHS_OR_SERVICES}}. Do not change them without a step card that names the partner's sign-off.
- {{PROJECT_RULE}}

## Repo conventions

<!-- guide: Brownfield: copy from the existing-system audit. Greenfield: decide once here. -->

- Language and runtime: {{...}}
- Formatting and lint: {{...}}
- Tests: {{framework, location, how to run}}
- Branching and review: work on `{{WORK_BRANCH}}`. Never commit to `{{BASE_BRANCH}}`. {{merge/PR rules}}
- Small commits. Each message says what changed and why.

## Commands

```bash
{{BUILD_COMMAND}}
{{UNIT_TEST_COMMAND}}
{{END_TO_END_COMMAND}}
python3 tools/doccheck.py --docs-dir {{DOCS}}
python3 tools/docmap.py show --docs-dir {{DOCS}}
bash tools/history/save-history.sh
```

## Environment variables

| Name | Values | Meaning |
|---|---|---|
| {{NAME}} | {{values}} | {{meaning; "server only" for secrets}} |

## History

The complete user-visible transcript of every AI session is a deliverable. Preserve prompts, responses, retries, corrections, tool output and decisions. Do not request or reconstruct hidden reasoning. Exports go in `ai-history/` (git-ignored) until redacted under `{{DOCS}}/ai-history/redaction-policy.md`.
