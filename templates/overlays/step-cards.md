# Overlay: step cards

**Source of truth:** {{SOURCE}}

<!-- guide: This overlay holds only what the source lacks. Never copy the source here, and never edit a partner document from a build session. In extend mode, these sections are meant to be pasted into the source once the partner agrees; until then this file is what the agent reads alongside it. Delete a section once the source covers it, and say where in the "Covered by the source" table. -->

The source holds the work items (tickets, milestones, a plan document). This overlay adds the fields every build session needs. One card per session; the session commands read the next card whose status is not done in `{{DOCS}}/progress.md`.

## Step cards

### S1. {{name}} (source item: {{ticket ID or section}})
- **Change type:** {{new / extend / replace / remove}}
- **Requirement IDs:** {{IDs from the doc map's Requirement IDs sources}}
- **Existing behaviour to keep:** {{…}}
- **Regression check:** {{baseline suite or named test}}
- **Partner sign-off needed:** {{no / yes: who, for which path}}
- **Done when:** {{observable checks, one per line}}

## Acceptance
| # | Check | How |
|---|---|---|
| A1 | {{…}} | {{…}} |
