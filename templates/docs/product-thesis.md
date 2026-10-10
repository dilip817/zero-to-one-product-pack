# {{PROJECT_NAME}}: product thesis and roadmap

**Status:** v{{0.1}} · **Last updated:** {{DATE}} · **Deliverable due:** {{DATE}}

**Evidence tags:** **[F]** sourced fact · **[O]** observed (one tester, one path) · **[I]** inference · **[H]** hypothesis · **[D]** decision · **[A]** assumption · **[?]** open question

<!-- guide: Planning-only. The "Core thesis" is what the build agent reads every session; keep it to about one screen. Everything else is appendix. -->

---

# Core thesis

**In one sentence:** {{rebuild/build X so that <user> can <outcome>, tracked to <endpoint>; AI does <narrow job>; fixed rules decide <eligibility/safety/money>.}}

## 1. Endpoint
- The journey ends at **`{{endpoint.event}}`**: {{definition}}. {{What does NOT count.}} [D]
- **Two headline metrics, always reported together** [D]:
  - **{{Completion}}:** {{eligible starts → endpoint}}.
  - **{{Correct outcome}}:** {{all starts → the right ending, including correct rejections}}.
- Why both: {{stops a classification change from gaming success}}.
- Today the trail stops at {{last observed event}}, {{x%}} of starts [F].

## 2. Evidence
| What we know | Source |
|---|---|
| {{step → next step: −N sessions (x%)}} | {{Funnel [F]}} |
| {{observation}} | {{Walkthrough [O]}} |

**Limits:** {{sessions vs people; segments; one tester; no user research; …}}

## 3. Segment
- **{{Who}}** [D]. **Why:** {{size, need, fit}} [I].
- **Not in the MVP:** {{other segments}}; they keep today's flow.

## 4. Priority problems
**P0 #1 — "{{user-voice problem}}"**
- **Data-backed:** {{number}} [F]
- **Hypothesis:** {{cause}} [H]

**P0 #2 — "{{…}}"**

**P1 — "{{…}}"** {{tracked now, redesigned later}} [D]

## 5. Product bet
- **MVP = {{quick wins + AI core}}**, built in {{N}} hours. [D]
- **Quick wins (no AI):** {{…}}
- **AI core (the bet):** {{the one narrow thing AI does, and what it may never do}}
- **Not doing:** {{…}}

## 6. How we will know
| Element | Primary metric | Guardrail |
|---|---|---|
| {{element}} | {{metric}} | {{metric that must not get worse}} |
| Overall | {{starts → endpoint}} | {{e.g. no-show rate, complaint rate}} |

## 7. Roadmap
| Horizon | What | Exit gate |
|---|---|---|
| Now (MVP) | {{…}} | {{…}} |
| Next | {{…}} | {{…}} |
| Later | {{…}} | {{…}} |

## 8. Experiments and staging
| Stage | Question | Design | Pass bar |
|---|---|---|---|
| 0. Diagnose | {{what we cannot yet tell apart}} | {{instrument first, no experiment}} | {{…}} |
| 1. Quick wins | {{…}} | {{A/B}} | {{…}} |
| 2. AI core | {{…}} | {{A/B against stage-1 winner}} | {{lift at 95%, zero safety failures, …}} |

## 9. Risks and what would change our mind
- {{risk}} → {{signal}} → {{response}}

## 10. Open questions
- {{question}} [?] (owner: {{…}})

---

# Appendix
<!-- guide: Journey walkthrough (stage by stage, with [O] tags), competitor notes, sizing, alternatives considered and why rejected, allowed user-facing facts (prices, policies, capabilities) with sources. The plan's "allowed facts" section points here. -->

## A1. Current journey, stage by stage
## A2. Alternatives considered
## A3. Allowed user-facing facts (source for every price, policy and capability)
| Fact | Exact wording | Source |
|---|---|---|
| {{…}} | {{…}} | {{screenshot / page / contract}} |
