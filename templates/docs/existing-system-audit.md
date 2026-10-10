# Existing-system audit: {{REPO}}

**Audited:** {{DATE}} at commit `{{SHA}}` · **By:** {{build agent via /kickoff}} · **Reviewed by:** {{partner engineer}}

<!-- guide: Brownfield only. Facts from the code, not from memory. Never paste secret values; record env var NAMES only. -->

## 1. Stack
| Layer | Technology and version | Where |
|---|---|---|

## 2. Services and boundaries
| Service | Responsibility | Owner | Talks to |
|---|---|---|---|

## 3. Data
| Store | Main entities | Who writes | PII? |
|---|---|---|---|

## 4. Auth, roles and access

## 5. Integrations and vendors
| Vendor | Used for | Where in code | Test double exists? |
|---|---|---|---|

## 6. Analytics and events
| Event | Fired where | Used in which funnel |
|---|---|---|

## 7. Test baseline (before any change)
| Suite | Command | Passed | Failed | Skipped |
|---|---|---|---|---|
Pre-existing failures: {{list; not ours to fix unless a card says so}}

## 8. Conventions
Language versions, lint/format, branching and review, commit style, deploy process.

## 9. Docs that already exist
<!-- guide: The decisions live in doc-map.md (one row per role and source, with mode and notes). Record here only what the kickoff found that the doc map cannot hold. -->
- Documents found that play no pack role, and where they are: {{…}}
- Google Docs that need a snapshot, and who can export them: {{…}}
- Partner documents that contradict each other or the code: {{…}}

## 10. Seams for new work
{{Interfaces, adapters, feature flags, routes where new work can attach without editing partner code.}}

## 11. Risks and fragile areas

## 12. Do not touch
{{Paths and services the agent must not change without partner sign-off.}}

## 13. Summary
Counts by traceability status: exists {{n}} · partial {{n}} · missing {{n}} · conflicts {{n}}. Top gaps: {{…}}. Questions for the partner: {{…}}.
