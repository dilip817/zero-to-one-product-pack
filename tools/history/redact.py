#!/usr/bin/env python3
"""Redact transcripts into a new folder. JSON and JSONL lines are parsed and redacted inside
each string, so JSON escapes cannot be damaged; other files are redacted as text.
Writes counts per file and category to <out>/redaction-counts.json.
Usage: python3 redact.py <in-dir> <out-dir> [--config redaction-config.json]"""
import argparse, collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import load, kept, units

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst"); ap.add_argument("--config")
a = ap.parse_args()
rules, keep = load(a.config)
active = [r for r in rules if r[2]]
counts = collections.defaultdict(collections.Counter)

def red(s, rel):
    for cat, rx, _, marker in active:
        def sub(m):
            if kept(m.group(0), keep): return m.group(0)
            counts[rel][cat] += 1
            return f"[REDACTED: {marker}]"
        s = rx.sub(sub, s)
    return s

def walk(x, rel):
    if isinstance(x, str): return red(x, rel)
    if isinstance(x, list): return [walk(v, rel) for v in x]
    if isinstance(x, dict): return {walk(k, rel): walk(v, rel) for k, v in x.items()}
    return x

for root, _, files in os.walk(a.src):
    for fn in sorted(files):
        p = os.path.join(root, fn); rel = os.path.relpath(p, a.src)
        out = os.path.join(a.dst, rel); os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", errors="surrogateescape") as o:
            for _, obj, raw in units(p):
                if obj is None:
                    o.write(red(raw, rel)); continue
                indent = 1 if fn.endswith(".json") else None
                seps = None if indent else (",", ":")
                o.write(json.dumps(walk(obj, rel), ensure_ascii=False, indent=indent, separators=seps) + ("\n" if raw.endswith("\n") else ""))
json.dump({k: dict(v) for k, v in counts.items()}, open(os.path.join(a.dst, "redaction-counts.json"), "w"), indent=1)
for k, v in sorted(counts.items()): print(k, dict(v))
print("files with redactions:", len(counts))
