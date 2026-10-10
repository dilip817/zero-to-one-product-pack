# Overlay: design

**Source of truth:** {{SOURCE}}

<!-- guide: This overlay holds only what the source lacks. Never copy the source here, and never edit a partner document from a build session. In extend mode, these sections are meant to be pasted into the source once the partner agrees; until then this file is what the agent reads alongside it. Delete a section once the source covers it, and say where in the "Covered by the source" table. -->

## Covered by the source
| Design element | Where the source covers it | Or here |
|---|---|---|
| Screens and flow | {{…}} | n/a |
| Loading, empty and error states | {{…}} | §1 |
| States where the system is unsure | {{…}} | `{{DOCS}}/design/uncertain-paths.md` |
| Where each user-facing claim comes from | {{…}} | `{{DOCS}}/design/copy-sources.md` |
| Why each screen exists (taps, screens, typed fields) | {{…}} | `{{DOCS}}/design/step-audit.md` |
| Accessibility target and mobile widths | {{…}} | §2 |
| How mocks are labelled | {{…}} | §3 |

## 1. States the source does not specify
| Screen | State | What the user sees | Next action |
|---|---|---|---|
| {{…}} | {{loading / empty / error}} | {{…}} | {{…}} |

## 2. Accessibility and widths
{{Target (e.g. WCAG 2.2 AA), widths tested, keyboard and screen-reader checks.}}

## 3. Mock labels
{{Wording and placement for anything not real.}}
