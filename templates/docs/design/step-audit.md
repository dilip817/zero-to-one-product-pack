# Step audit: does every step need to exist?

<!-- guide: Answers "what is the least a user must do" and "where do we expect drop-off". Every statement tagged [code], [docs] or [hypothesis]. Count taps and typed inputs from the code, not from memory. -->

## How to read this
**Taps** = one press, tick or choice. **Typed inputs** = fields a real user would fill. Tags: [code] counted from the build · [docs] from the repo docs · [hypothesis] not measured.

## Screen by screen
### {{N}}. {{Screen}}
- **Purpose [code]:** {{…}}
- **Why it exists:** {{rule / decision ID / evidence}}
- **Taps and typed inputs [code]:** {{n}} / {{n}}
- **Could be removed, merged or deferred?** {{…}}
- **Expected drop-off:** [docs] {{funnel figure if any}} · [hypothesis] {{…}}
- **Events that would read it:** {{…}}

## Paths compared
| Path | Taps | Screens | Typed inputs | Gives up |
|---|---|---|---|---|
| A. Today's flow | | | | |
| B. Least possible (floor) [hypothesis, not built] | | | | |
| C. As built [code] | | | | |

## The AI part's benefit is a hypothesis
- **What is known:** {{eval numbers; what they do and do not show}}
- **What would test it:** {{arms: AI vs same choices from a list vs form-only floor}}

## Open questions for {{PARTNER}}
1. {{…}}
