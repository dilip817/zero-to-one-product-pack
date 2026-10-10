# Redaction policy for AI history

<!-- guide: Agree with the owner and partner before the first export. Redact only what this policy lists; everything else stays, so the history remains complete. -->

## Always redact
| Category | Marker |
|---|---|
| Credentials, API keys, tokens, private keys, `.env` values | `[REDACTED: secret]` |
| {{owner's personal email / phone / home address}} | `[REDACTED: personal email address]` … |
| Third-party email addresses and phone numbers | `[REDACTED: third-party email address]` |
| Machine hostnames, local usernames in paths | `[REDACTED: hostname]` |
| {{real customer or end-user data, if any ever appeared}} | `[REDACTED: customer data]` |

## Keep on purpose
- {{names of people already public in the deliverable}} · variable **names** such as `API_KEY` (never values) · attribution addresses such as `noreply@…` · synthetic test data.

## Method
1. Copy raw transcripts to a git-ignored folder.
2. Scan (`tools/history/scan.py`): report categories with file and line counts, never values.
3. Redact inside each JSON string (`tools/history/redact.py`), so escapes and structure survive.
4. Re-scan the redacted copy: zero hits per redacted category; every JSON line parses.
5. Write `REDACTIONS.md` with counts per file and category, what was kept, what is not included.
6. Share only after the owner's go; record the link in the index.
