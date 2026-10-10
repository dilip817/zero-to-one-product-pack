# Evaluation plan (pre-registered)

**Written:** {{DATE}}, before any held-out result was seen. This section is not edited after results exist; later changes go in dated entries in `RESULTS.md`.

<!-- guide: The point is to make the AI claim falsifiable. A baseline that needs no model, a held-out split run once, thresholds written first, and limits stated as plainly as results. -->

## 1. Question
{{Does <model approach> beat <non-AI baseline> at <task>, without <safety failure>?}}

## 2. What is compared
| Arm | Description |
|---|---|
| Baseline | {{keyword table / rules / form}} |
| Model | {{model, prompt version, output schema, validator}} |

## 3. Dataset
- Size and split: {{n}} items, {{dev n}} / {{held-out n}}. Held-out is not read while developing.
- Who writes it: {{…}} · Synthetic: {{yes}} · Schema: `dataset-schema.md`.
- Coverage: {{plain, paraphrase, negation, typos, other languages, identity statements that must not create preferences, off-topic, direct and indirect risk}}.

## 4. Metrics
| ID | Metric | Definition |
|---|---|---|
| M1 | {{label F1 (micro)}} | {{…}} |
| M2 | {{false-positive rate on <class>}} | {{…}} |
| M3 | {{risk recall of the fixed screen}} | {{…}} |

## 5. Pre-registered thresholds and decision rules
| ID | Threshold | If met | If not met |
|---|---|---|---|
| T1 | {{M1 model ≥ baseline + x}} | {{ship model}} | {{ship baseline}} |
| T2 | {{safety: zero <class> passes the screen}} | | {{block}} |

## 6. Method rules
- Fixes are made on dev only. A held-out-driven fix is recorded as a deviation.
- Held-out is run once, after code freeze, {{k}} repeats for nondeterminism.
- Scoring: {{strict / lenient}}, defined before running.
- Every run records provenance: commit, prompt hash, model, date, dirty flag.

## 7. Requirement mapping
| Requirement | Metric / threshold |
|---|---|
