# {{PROJECT_NAME}}: implementation plan (engineering requirements)

**Version:** {{v1}} · **Last updated:** {{DATE}} · **Owner:** {{planning}} · Planning-only

<!-- guide: This is the build agent's spec. Every requirement has an ID and a "Verified by". Every step card fits one session. Brownfield: requirements cite the traceability status, and step cards name the change type. -->

## 1. Purpose and scope
{{What this plan covers; link the thesis core; what is out.}}

## 2. How the work is split [D]
| Who | Does |
|---|---|
| Planning chat | Thesis, decisions, this plan, the contract |
| Build agent | Code, tests, progress, traceability, AI history rows |
| {{Partner}} | {{reviews, sign-offs, partner-owned code}} |

## 3. Requirements
<!-- guide: If the partner's PRD or a Google Doc already defines requirements, do not copy them here: they are listed in doc-map.md under "Requirement IDs" and traced with their own IDs. This section then holds only what those sources lack, usually safety (SR), quality (QR) and measurement (MR). -->
<!-- guide: FR = functional, SR = safety/security, QR = quality/operations, MR = measurement. "Verified by" names an automated test or a named manual check. Brownfield: add a "Status at kickoff" column from traceability.md. -->

### 3.1 Functional
| ID | Requirement | Verified by |
|---|---|---|
| FR1 | {{…}} | {{unit / end-to-end / manual: name}} |

### 3.2 Safety and security
| ID | Requirement | Verified by |
|---|---|---|
| SR1 | {{Fixed rules decide <x>; no model output is an input}} | {{…}} |
| SR2 | {{Fail closed: an error never moves a user forward}} | {{…}} |

### 3.3 Quality and operations
| ID | Requirement | Verified by |
|---|---|---|
| QR1 | {{accessibility target, performance budget, mobile widths}} | {{…}} |

### 3.4 Measurement
| ID | Requirement | Verified by |
|---|---|---|
| MR1 | {{events emitted for every step and exit}} | {{…}} |

## 4. System design
### 4.1 Architecture
{{Diagram or list: client, server functions, model call, adapters, data.}} Brownfield: show where new parts attach to the seams in the audit. Entities, the ERD and field classification live in the `data-model` role (doc-map.md), not here.

### 4.2 Journey
| # | Screen / state | Decides | Events |
|---|---|---|---|
| 0 | {{…}} | {{…}} | {{…}} |

### 4.3 AI route
{{Input limits → screen → model call → validator → fallback. Output schema (keys from fixed tables). Timeouts, rate limits, modes (live/mock).}}

### 4.4 Fixed tables
{{The closed sets the model may return keys from, and who owns their wording.}}

### 4.5 Integrations and adapters
| Vendor / partner service | What it does in production | In the prototype | Adapter file | Mock label |
|---|---|---|---|---|
| {{…}} | {{…}} | {{fixture/stub/live}} | {{…}} | {{…}} |

### 4.6 Events, and how they map to the partner's funnel
| Event | Properties | Partner's event it maps to |
|---|---|---|
| {{…}} | {{…}} | {{…}} |

### 4.7 Privacy and compliance
### 4.8 Failure modes
| Failure | What the user sees | Event |
|---|---|---|

## 5. Tools, and why these over the alternatives

## 6. Build plan
### 6.1 Step cards
<!-- guide: One card = one session. Anything not on the card or in §3–§4 is out of scope for that session. -->

**Step {{N}} — {{name}}**
- **Change type:** {{new | extend | replace | remove}}
- **Starts from:** {{state of the repo}}
- **Do:** {{…}}
- **Keep (existing behaviour):** {{…}} · **Regression check:** {{…}}
- **Constraints:** {{decision and requirement IDs}}
- **Partner sign-off needed:** {{no | yes: who, for what}}
- **Not in this step:** {{…}}
- **Done when:** {{observable, testable conditions}}

### 6.2 Submission / launch checklist
See `handoff/launch-checklist.md`.

## 7. Acceptance
| # | Requirement | Covered by |
|---|---|---|
| 1 | {{The endpoint is reachable on a phone at the real URL}} | {{…}} |
| 2 | {{With the model off, the same path completes through the fallback}} | {{…}} |
| 3 | {{Every §3 requirement has a passing test or a named manual check}} | {{traceability.md}} |

## 8. Risks
## 9. Open items
## Sources
