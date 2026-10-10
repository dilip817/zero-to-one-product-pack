# Overlay: evals

**Source of truth:** {{SOURCE}}

<!-- guide: This overlay holds only what the source lacks. Never copy the source here, and never edit a partner document from a build session. In extend mode, these sections are meant to be pasted into the source once the partner agrees; until then this file is what the agent reads alongside it. Delete a section once the source covers it, and say where in the "Covered by the source" table. -->

The source is the partner's eval harness (for example a promptfoo config, a pytest suite or a notebook). This overlay adds the rules that make its numbers trustworthy: written before the results, run once on held-out data, compared with a simple baseline.

## Harness
| | |
|---|---|
| Config / entry point | {{path}} |
| Run command | {{…}} |
| Output location | {{path of results the harness writes}} |
| Datasets | {{paths; which is development and which is held out}} |

## Pre-registration (fill and commit before the held-out run)
| Item | Value |
|---|---|
| Question | {{Does <AI part> beat <baseline> on <task>?}} |
| Metric and how it is scored | {{…}} |
| Baseline (non-AI or current behaviour) | {{…}} |
| Pass rule | {{e.g. at least X points above baseline, and no safety-case misses}} |
| Held-out set and its hash | {{path}} · {{sha256}} |
| Sealed on | {{date and commit}} |
| Run once | The held-out set is run once; any rerun after a change is a new pre-registration and a new decision ID. |

## Results
| Date | Commit | Baseline | AI | Pass rule met? | Harness output |
|---|---|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} | {{yes / no}} | {{path}} |

## Changes after seeing results
{{Each one is a decision in the decisions role, with its ID.}}
