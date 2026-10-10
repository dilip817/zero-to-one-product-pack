# Project charter: {{PROJECT_NAME}}

<!-- guide: One page, agreed with the partner before any other document. Planning-only. -->

**Partner:** {{COMPANY}} · {{PARTNER_NAMES_AND_ROLES}}
**Owner on our side:** {{NAME}}
**Start / freeze / deliver:** {{DATE}} / {{DATE}} / {{DATE}}
**Mode:** {{greenfield | brownfield (repo, branch)}}
**Adoption level:** {{Lite | Standard | Full}}

## Problem in one sentence
{{Who struggles with what, measured how.}}

## Endpoint
{{The single event that means "done" for the user, e.g. first_order.delivered, not "signed up".}}

## Definition of done for this engagement
- {{deployed URL / PR / handoff doc / walkthrough / evals / AI history}}

## In scope / out of scope
| In | Out |
|---|---|
| {{...}} | {{...}} |

## Ownership
| Area | Owner | Notes |
|---|---|---|
| Existing code, services, data | {{partner}} | Agent may read; changes need a step card with sign-off |
| New code in `{{paths}}` | {{us}} | |
| Brand assets, customer quotes, prices, policies | {{partner}} | Every use listed in `sign-off.md` |
| Docs in `{{DOCS}}/` | {{us}} | |
| IP and licensing | {{...}} | |

## Data, privacy and access
- Data used in the build: {{synthetic only / anonymised extract / production read-only}}
- Where it may live: {{...}} · Who can access the deployment: {{...}}
- Secrets: {{where they live; never in the repo}}
- AI history: shared with {{whom}}, redacted under `ai-history/redaction-policy.md`

## Constraints
{{Stack, compliance, budget, vendors that must or must not be used, time.}}

## Communication
{{Cadence, channel, who decides, how decisions are recorded (decisions.md).}}
