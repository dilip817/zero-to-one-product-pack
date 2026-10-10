# Playbook: running a zero-to-one build

The loop, the gates between phases, and the habits that kept the source project honest. Read once at the start of a project; come back to the gate list before each phase.

## Phases and gates

| Phase | Output | Gate to leave the phase |
|---|---|---|
| 0. Charter | `docs/project-charter.md` | Partner and you agree the problem, the endpoint, the deadline, ownership, data rules and what "done" means |
| 1. Thesis | `docs/product-thesis.md` "Core thesis", first lines of `docs/decisions.md` | One-sentence thesis; endpoint; two headline metrics; every claim tagged; the bet and what it is not |
| 2. Audit (brownfield) | `docs/existing-system-audit.md`, seeded `docs/traceability.md` | Baseline tests run and recorded; every requirement has a status; "do not touch" list agreed with the partner |
| 3. Plan | `docs/implementation-plan.md` | Every requirement has an ID and a way to verify it; step cards each fit one session and have a "Done when"; acceptance list written |
| 4. Build | Code, tests, `docs/progress.md` | Each step: tests green, "Done when" checked, progress and history updated, committed |
| 5. Prove | `docs/evals/eval-plan.md` then `docs/evals/RESULTS.md` | Thresholds written before results; held-out run once; limits written as plainly as the result |
| 6. Hand off | `docs/handoff/*`, redacted AI history | Launch checklist done; every mock labelled; sign-off list current; reviewer can follow the PR body alone |

The files above are the defaults. Each is a role in `docs/doc-map.md`; in a partner repo the role may resolve to their own document plus an overlay.

## The session loop (build agent)

1. `/start-step`: read the contract, decisions, progress, plan; name one step; write a plan; wait for approval.
2. Build only what the card asks.
3. Run the tests and the end-to-end check. Never finish red.
4. `/finish-step`: check "Done when", update progress and traceability, add the AI history row, commit with a message that names the step and why.
5. Stop. Do not start the next step.

## Habits worth keeping

**Evidence**
- Tag every claim: **[F]** sourced fact, **[O]** observed (one person, one path), **[I]** inference, **[H]** hypothesis, **[D]** decision, **[A]** assumption, **[?]** open question.
- Say the limits next to the number: sessions or people, sample size, who wrote the data, what the funnel cannot tell apart.
- Qualitative research is "recurrent in this sample", never prevalence.

**Decisions**
- One line per decision in `docs/decisions.md`, with an ID and a date. The latest line wins over every other file.
- When files disagree, the build agent stops and asks; it never picks.

**Scope**
- One step per session. Anything not on the card is out of scope, however small.
- A feature freeze date, after which only fixes the owner asks for go in.

**Truthfulness in the product**
- Never invent a policy, price, capability or vendor feature. User-facing copy states only what a named source says; keep the list of allowed facts in the plan.
- Every sentence a user sees has a source class (sourced, decided, fixed, fixture, interface). Keep the register in `docs/design/copy-sources.md`.
- Label every mock, on screen and in the README.
- Fail closed: an error never moves a user forward.

**AI in the loop**
- Fixed rules decide eligibility and safety; model output is never an input to them.
- The model returns keys from fixed tables; anything it writes that is shown to a user must be a verbatim quote of the user, or it is dropped.
- Compare against a non-AI baseline, on held-out data, with thresholds written first.

**Hand-off**
- The PR body is self-sufficient: start here, why, what it does, decisions and known gaps, real vs mocked, safety, evaluation, checks, files to read first.
- AI history is complete, redacted with labelled markers, and scanned before it leaves the machine.
- Don't merge or promote the deliverable unless the owner explicitly says to.

## Working with a partner founder

- Use their documents where they are. If they have a PRD, an ERD or schema, evals, ADRs or design docs, map them in `doc-map.md` as `adopt` and let the pack add only an overlay with what is missing. Never fork their document into a parallel copy; the two drift within a week.
- Google Docs stay theirs. The agent reads a dated snapshot (`/refresh-external`), and doccheck flags snapshots older than the doc map's limit, so a session never builds from a stale spec without saying so.
- Trace their requirement IDs, not renamed ones. Add their ID pattern to the doc map's "Requirement IDs" table; the pack's own IDs cover only what their documents lack (usually safety, quality and measurement).
- Agree in the charter which code, data, brand assets and docs are theirs, which are yours, and which are joint. Put "partner-owned" paths in the agent contract so the agent never edits them without sign-off.
- Use their names, terms and events in the docs. Map your metrics onto their funnel (`implementation-plan.md` §4 events table) rather than inventing a parallel one.
- Anything the product says about their business (prices, policies, capabilities, customer quotes, brand) goes into `docs/sign-off.md` with the role who must confirm it.
- Ask the partner the "Open questions for <partner>" list in `docs/design/step-audit.md` early; most late surprises are in there.
