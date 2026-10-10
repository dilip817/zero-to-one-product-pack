# Zero-to-one product pack

[![test](https://github.com/dilip817/zero-to-one-product-pack/actions/workflows/test.yml/badge.svg)](https://github.com/dilip817/zero-to-one-product-pack/actions/workflows/test.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Templates and tools for running a zero-to-one product build with a partner founder, in a new repo or inside an existing one. It packages the operating system from one finished project: a product thesis, a decision log, an execution plan with step cards, a design and copy discipline, pre-registered evals, and an AI history that can be handed over.

There is no project content in here. Every file is a skeleton with `{{PLACEHOLDERS}}` and `<!-- guide: ... -->` notes that say what goes where and why. Delete the guide notes as you fill them in.

## Quick start

```bash
git clone https://github.com/dilip817/zero-to-one-product-pack.git
cd zero-to-one-product-pack

# a new project
bash install.sh ~/code/my-new-product --mode greenfield

# an existing codebase that already has a PRD, a schema, evals, ADRs or Google Docs
bash install.sh ~/code/partner-app --mode brownfield --docs-dir docs/z21 --dry-run
```

Needs Python 3.10 or later and nothing else. The session commands (`/start-step`, `/kickoff`, ...) are [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills; the documents and tools work without it.

**Who it is for:** founders, product engineers and studios who build new products with an AI coding agent, often inside someone else's codebase, and want the thinking, the build and the evidence to stay in step.

## The five pillars

| # | Pillar | Files | What it answers |
|---|---|---|---|
| 1 | Product thesis and roadmap | `docs/product-thesis.md`, `docs/decisions.md` | Why this, for whom, what we bet, how we will know, what comes next |
| 2 | Execution plan and ERD | `docs/implementation-plan.md`, `docs/data-model.md`, `docs/traceability.md`, `docs/existing-system-audit.md` | What to build, in which order, how each step is proven done, and what already exists |
| 3 | Design | `docs/design/*` | What it looks like, why each screen exists, where every word comes from, what happens when the system is unsure |
| 4 | Evals | `docs/evals/*` | Does the AI part beat a simple baseline, by a rule written down before the results were seen |
| 5 | AI history | `docs/ai-history/*`, `tools/history/*` | A complete, redacted record of every AI session, ready to share |

Around them: `docs/doc-map.md` (where each document lives; see below), `CLAUDE.md` (the agent's operating contract), `docs/progress.md` (where the build is), `docs/handoff/*` (PR description, walkthrough cues, stakeholder message, launch checklist), `docs/evidence/research-note.md`, `docs/sign-off.md`, and the session skills in `.claude/skills/`.

## Install

```bash
# New project: every document is the pack's own
bash install.sh /path/to/repo --mode greenfield

# Existing project: core files, plus a doc map proposed from the documents already there
bash install.sh /path/to/repo --mode brownfield --docs-dir docs/z21
#   ...run /kickoff, then confirm each row in docs/z21/doc-map.md...
bash install.sh /path/to/repo --apply-map --docs-dir docs/z21

# Any of them with --dry-run first to see what would happen
```

The installer never overwrites a file and is safe to re-run. When a partner file is in the way (their `CLAUDE.md`, `README.md`), it writes the pack's version next to it as `<name>.starter.<ext>` for you to merge. Pack files you have edited since installing are left alone. Each run is appended to `<docs>/.starter-manifest`. It needs Python 3.10 or later and nothing else (tested on 3.10 to 3.13).

Then, at any time:

```bash
python3 tools/docmap.py show --docs-dir docs/z21     # where every role resolves
python3 tools/doccheck.py --docs-dir docs/z21        # gaps: unconfirmed roles, stale snapshots, untraced requirements, placeholders
```

## The doc map: using the documents a project already has

Every pack document is a **role**: charter, thesis, roadmap, requirements, plan, data-model (ERD), design, evals, decisions, research. `docs/doc-map.md` says, per role, where it lives:

| Mode | Meaning | What the installer puts in place |
|---|---|---|
| `new` | No existing document; use the pack's | The full template |
| `adopt` | The partner's document is the source of truth | An overlay in `docs/overlays/<role>.md` with only what it lacks (e.g. on a PRD: endpoint, headline metric and guardrail, evidence tags, the bet) |
| `extend` | As `adopt`, and the overlay's sections should be pasted into their document once they agree | The same overlay, marked `[extend]` |
| `skip` | Not used in this project | Nothing |

A role can have several sources, for example a PRD in the repo and a strategy Google Doc. What each kind of existing document becomes:

| You already have | Role and mode | What the pack adds |
|---|---|---|
| PRD (`docs/PRD.md`, `REQ-12`, user stories) | `thesis` and `requirements`, adopt | Thesis overlay; its IDs traced as they are (`REQ-\d+` in the doc map's "Requirement IDs"); the pack's plan §3 holds only what the PRD lacks (safety, quality, measurement) |
| ERD or schema (`schema.prisma`, `.dbml`, SQL, a mermaid `erDiagram`) | `data-model`, adopt | Entities touched, field classification, migrations and rollback, ERD of what is added |
| Evals (promptfoo, pytest, a notebook, an `evals/` folder) | `evals`, adopt | Pre-registration (baseline, pass rule, held-out hash, run once) and a results table that links the harness's output |
| ADRs or a decision log | `decisions`, adopt | A one-line-per-decision index; new decisions are written in their ADR format |
| Design doc or Figma/Slides deck | `design`, adopt | Missing states, accessibility, mock labels; links to step audit, copy sources and uncertain paths |
| Research notes, interviews | `research`, adopt | Evidence tags on the claims the thesis relies on |
| Execution plan or tickets | `plan`, adopt | Step-card fields (change type, behaviour to keep, regression check, sign-off, Done when) |
| Google Docs, Slides, Sheets | any role, with a URL source | A dated local snapshot the agent reads (`python3 tools/docmap.py snapshot <url> <download>` or `/refresh-external`); doccheck flags it when older than 14 days |

**Detection.** In brownfield mode the installer proposes rows by looking for these files by name and folder, for requirement IDs defined in tables, headings and bullets, and for Google Doc links in any Markdown file. Nothing is applied until planning sets `Confirmed` to `yes`. `/kickoff` checks every proposal against the file's content and looks for what the names missed.

**Who edits what.** Partner documents are never edited from a session. Overlays and the doc map are planning-owned. Snapshots are refreshed, never hand-edited. The session commands (`/start-step`, `/finish-step`, `/trace`, `/sync-docs`) read every role through the map, so nothing in them changes per project.

## How a project runs (summary; the full loop is in PLAYBOOK.md)

1. **Charter** (`docs/project-charter.md`): partner, problem, constraints, who owns what, what "done" means, data and IP rules. One page, agreed before anything else.
2. **Thesis** (`docs/product-thesis.md`): the one-sentence thesis, the endpoint, two headline metrics, evidence with tags, the bet, the roadmap. Decisions go to `docs/decisions.md`, one line each.
3. **Audit, if the code exists** (`/kickoff`): fills `docs/existing-system-audit.md` and seeds `docs/traceability.md` from the real code and tests.
4. **Plan** (`docs/implementation-plan.md`): requirements with IDs, design, step cards with "Done when", acceptance.
5. **Build, one step per session** (`/start-step`, `/finish-step`): plan, approval, build, tests, progress, history row, commit.
6. **Prove** (`docs/evals/`): pre-register thresholds, run the baseline and the model on held-out data once, write the limits as plainly as the result.
7. **Hand off** (`docs/handoff/`): launch checklist, PR description, walkthrough cues, stakeholder message, redacted AI history (`/export-history`).

## Two kinds of chat, one source of truth

The pack assumes two roles, which can be two tools or two sessions:

- **Planning chat** (thinking, deciding): owns `CLAUDE.md`, `docs/decisions.md`, `docs/implementation-plan.md`, `docs/product-thesis.md`, `.claude/`.
- **Build agent** (Claude Code): owns code, tests, `README.md`, `docs/progress.md`, `docs/traceability.md`, `docs/ai-history/ai-history-index.md`, and the design and eval working files.

The only things carried between them are the files. When a chat-owned file is wrong, the build agent writes the question under "Questions for planning" in `docs/progress.md` instead of editing it. When a chat-owned file is replaced, run `/sync-docs`.

## Brownfield: adopting the pack in an existing codebase

The pack must fit the partner's system, not the other way round.

1. **Install into a separate docs folder** (`--mode brownfield --docs-dir docs/z21`). The partner's docs are not moved, renamed or copied. The installer proposes a doc map from what it finds.
2. **Merge the agent contract.** Keep the partner's `CLAUDE.md` (or equivalent) and add three sections from `CLAUDE.starter.md`: the file-ownership table with the doc-map paragraph, the session loop, and the non-negotiable rules. Add their conventions to "Repo conventions".
3. **Run `/kickoff`.** It reads the repo (stack, services, data, auth, CI, tests, analytics, design system, vendors, deploy), records baseline test counts so later steps can prove they broke nothing, checks every doc-map proposal against the file's content, and lists Google Docs that need snapshots.
4. **Confirm the doc map** (planning), snapshot the Google Docs (`/refresh-external`), then `install.sh --apply-map`. Partner documents get overlays; only the missing roles get templates.
5. **Seed the traceability matrix from the code.** Every requirement ID, from every source in the doc map, gets a status (`exists`, `partial`, `missing`, `conflicts`) with the file and test that show it. Step cards are then written to close `partial` and `missing` rows: nothing is rebuilt that already works, and nothing is assumed to work that has no test.
6. **Step cards name the change type.** Each card says `new`, `extend`, `replace` or `remove`, lists "existing behaviour to keep", and names the regression check. A step that touches partner-owned code needs the partner's sign-off in the card.
7. **Work behind seams.** New vendor or model calls go behind an adapter with a fixture, a stub and a mock label, so the partner can swap in their real service without touching the flow.

## Adoption levels

| Level | Use when | Roles to keep (set the rest to `skip` in the doc map) |
|---|---|---|
| Lite | A one-week spike or a single feature | charter, thesis (core only), decisions, plan (§3 and §6 only), plus progress and the AI history index |
| Standard | A zero-to-one MVP | Lite plus requirements tracing, data-model, design, evals, and the sign-off and handoff files |
| Full | A partner build that will ship to real users | Standard plus research, the existing-system audit, uncertain paths, redaction tooling, and the launch checklist with owner steps |

A partner with mature documents can run Standard with most roles on `adopt`: the work is then mostly overlays and tracing.

## Files in this pack

```
install.sh, install.py           non-destructive installer: greenfield, brownfield (with detection), --apply-map
PLAYBOOK.md                      the operating loop, gates and habits
templates/CLAUDE.md              agent operating contract
templates/README.project.md      project README skeleton (real vs mocked, known gaps)
templates/.claude/skills/        start-step, finish-step, sync-docs, kickoff, trace, refresh-external, export-history
templates/docs/                  the documents, by pillar (doc-map.md is generated by the installer)
templates/overlays/              what each role adds on top of a partner's own document
tools/docmap.py                  show, detect, snapshot: the doc map's reader and helpers
tools/doccheck.py                doc map, placeholder, structure, traceability and decision checks
tools/history/                   save, scan and redact AI-session transcripts
tests/test_pack.py               end-to-end tests on a synthetic partner repo (tests/fixtures/brownfield)
```

## Limits

- Detection proposes, it does not decide: it matches file names, folder names and ID formats. `/kickoff` and a person confirm every row.
- Google Docs are read through dated snapshots, not live.
- Redaction is pattern-based and best-effort. Read an export before you share it (see `SECURITY.md`).

## License

[MIT](LICENSE). Use it, change it, ship it; keep the notice. Contributions welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

