# Security

## Reporting

Please report security problems privately through GitHub's "Report a vulnerability" (Security tab) rather than in a public issue.

## The redaction tools are best-effort

`tools/history/` finds secrets and personal data by pattern and by the values you list in `redaction-config.json`. It will miss values it has no pattern for: names, addresses, internal project names, secrets in unusual formats. Always read a redacted export before you share it, and keep `redaction-config.json` and `ai-history/` out of version control (the installer adds both to `.gitignore`).

## Snapshots of partner documents

`docs/external/` holds copies of Google Docs. They may be confidential. Follow your project charter's data rules before committing them to a repository others can read.
