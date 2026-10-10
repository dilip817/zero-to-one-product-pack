"""Shared redaction rules for scan.py and redact.py. Values from the config are never printed."""
import json, re

SECRETS = {
    "secret: Anthropic key": r"sk-ant-[A-Za-z0-9_\-]{20,}",
    "secret: other sk- key": r"\bsk-[A-Za-z0-9]{32,}",
    "secret: GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})",
    "secret: AWS key id": r"\bAKIA[0-9A-Z]{16}\b",
    "secret: Slack token": r"\bxox[baprs]-[A-Za-z0-9-]{10,}",
    "secret: JWT": r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]+",
    "secret: Bearer token": r"[Bb]earer\s+[A-Za-z0-9._\-]{24,}",
    "secret: private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "secret: key/token/password assigned a long value": r"(?i)(?:api[_-]?key|token|secret|password|passwd)[\"']?\s*[=:]\s*[\"']?(?!(?:process|os\.environ|\$\{?|<|your|xxx|example))[A-Za-z0-9_\-/+=]{20,}",
}
EMAIL = r"(?i)(?<![\\\w.%+\-])[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}\b"

def _filled(xs):
    return [x for x in xs if x and "{{" not in x]

def load(path):
    cfg = json.load(open(path)) if path else {}
    keep = [k.lower() for k in cfg.get("keep_emails", [])]
    rules = []  # (category, compiled, redact?)
    for cat, pat in SECRETS.items():
        rules.append((cat, re.compile(pat), True, "secret"))
    for group, redact in (("redact", True), ("report_only", False)):
        for r in cfg.get(group, []):
            pats = [re.escape(x) for x in _filled(r.get("literal", []))] + _filled(r.get("regex", []))
            if pats:
                rules.append((r["category"], re.compile("(?i)" + "|".join(pats)), redact, r["category"]))
            if r.get("any_email"):
                rules.append((r["category"], re.compile(EMAIL), redact, r["category"]))
    return rules, keep

def kept(match_text, keep):
    t = match_text.lower()
    return any(k in t for k in keep)

def strings(x):
    """Every string inside a parsed JSON value, keys included."""
    if isinstance(x, str): yield x
    elif isinstance(x, list):
        for v in x: yield from strings(v)
    elif isinstance(x, dict):
        for k, v in x.items(): yield k; yield from strings(v)

def units(path):
    """Yield (line_no, parsed_json_or_None, raw_text). A .json file is one unit; .jsonl is one per line."""
    with open(path, errors="surrogateescape") as fh:
        if path.endswith(".json"):
            raw = fh.read()
            try: yield 1, json.loads(raw), raw
            except Exception: yield 1, None, raw
            return
        for i, line in enumerate(fh, 1):
            obj = None
            if path.endswith(".jsonl") and line.strip():
                try: obj = json.loads(line)
                except Exception: obj = None
            yield i, obj, line
