# Launch / submission checklist

**Deliverable due:** {{DATE}} · **Freeze:** {{DATE}} · Last automated pass: {{DATE}} on `{{SHA}}`.

## A. Automated checks (build agent)
| # | Check | Result | How |
|---|---|---|---|
| A1 | Unit tests | | `{{cmd}}` |
| A2 | End-to-end, every path, phone and desktop | | `{{cmd}}` |
| A3 | Accessibility audit | | `{{cmd}}` |
| A4 | Copy register: 0 open, 0 under review | | `{{cmd}}` |
| A5 | Sign-off list current | | `{{cmd}}` |
| A6 | Every mock labelled (screen and README) | | |
| A7 | No secrets in the repo; `.env*` and `ai-history/` ignored | | `git grep …` |
| A8 | Traceability: every requirement verified | | `python3 tools/doccheck.py --docs-dir {{DOCS}} --strict` |
| A9 | Base branch untouched; PR open, not merged | | |
| A10 | CI green on the final head | | |

## B. Owner steps
| # | Step | When | Notes |
|---|---|---|---|
| B1 | Decide who can open the deployment, and until when | | |
| B2 | Record the walkthrough | | `walkthrough-cues.md` |
| B3 | Final check on a phone at the real URL | | |
| B4 | Export the AI histories | | `/export-history` |
| B5 | Send the stakeholder message | | `stakeholder-message.md` |
| B6 | Restore access protection after the review window | {{DATE}} | |

## C. Shared items
| # | Item | Owner | State |
|---|---|---|---|
| C1 | Personal data in screenshots and docs reviewed and redacted | | |
| C2 | Partner-supplied files contain no real customer data | | |
| C3 | AI history scanned, redacted, indexed | | |

## D. Acceptance (from the `plan` role: implementation-plan.md §7, or the step-cards overlay)
| # | Requirement | Covered by |
|---|---|---|
