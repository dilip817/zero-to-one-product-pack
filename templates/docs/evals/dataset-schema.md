# Evaluation dataset schema

One JSON array in `{{DOCS}}/evals/dataset.json` (or the eval folder of your choice). Each item:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable ID, e.g. `dev-001`, `ho-001` |
| `split` | `"dev"` \| `"heldout"` | Held-out is not read during development |
| `author` | string | Who wrote it (`team`, `user-written`, …) |
| `text` | string | The input, synthetic |
| `expected_labels` | string[] | Keys from the fixed table that should be returned |
| `expected_prefs` | string[] | Optional secondary keys |
| `risk` | `"none"` \| `"direct"` \| `"indirect"` | Safety class |
| `tags` | string[] | Coverage tags: `paraphrase`, `negation`, `typo`, `language:es`, `identity`, `off-topic` |
| `notes` | string | Why this item exists |

See `dataset.example.json` for shape only (placeholder values).
