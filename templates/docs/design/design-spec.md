# Design spec: {{PROJECT_NAME}}

<!-- guide: The visual and interaction source of truth. Brownfield: if the partner has a design system, this file links it and records only deltas. -->

## 1. Sources
| Source | What it gives us | Where |
|---|---|---|
| {{partner design system / production screenshots / Figma}} | {{tokens, components, tone}} | {{path or link}} |

Reference screenshots live in `{{DOCS}}/design/screens/` (docs only, never in a deployed folder). Inventory: {{numbered list, what each shows}}.

## 2. Tokens
| Token | Value | Source |
|---|---|---|
| color.primary | {{…}} | {{…}} |
| type.title | {{size/line-height}} | {{…}} |
| space.unit | {{…}} | {{…}} |

## 3. Components
| Component | States | Notes |
|---|---|---|
| Button | default, hover, disabled, loading | min target {{44px}} |

## 4. Layout and breakpoints
{{Widths tested (e.g. 390, 1100, 1280), sticky elements, what changes at each breakpoint.}}

## 5. Voice and copy rules
- {{tone}} · {{reading level}} · {{words we never use (e.g. "you may have")}}
- Every sentence users see is registered in `copy-sources.md`.

## 6. Accessibility targets
{{WCAG level, contrast minimum, keyboard-only path, focus order, labels.}}

## 7. Mock labelling
{{How a mocked surface is labelled on screen, one label per screen, exact wording.}}

## 8. Exceptions and open design questions
