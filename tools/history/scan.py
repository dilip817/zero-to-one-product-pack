#!/usr/bin/env python3
"""Scan transcripts for secrets and configured personal data. Prints categories with file,
line counts and line numbers only, never the matched values.
Usage: python3 scan.py <dir> [--config redaction-config.json]"""
import argparse, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import load, kept, units, strings

ap = argparse.ArgumentParser(); ap.add_argument("dir"); ap.add_argument("--config")
a = ap.parse_args()
rules, keep = load(a.config)
hits = collections.defaultdict(lambda: collections.defaultdict(list))
for root, _, files in os.walk(a.dir):
    for fn in sorted(files):
        p = os.path.join(root, fn)
        for i, obj, raw in units(p):
            texts = list(strings(obj)) if obj is not None else [raw]
            # Same order as redact.py: once a value is matched it is masked, so it is not counted twice.
            for cat, rx, _, _ in rules:
                n = 0
                def mask(m):
                    global n
                    if kept(m.group(0), keep): return m.group(0)
                    n += 1; return "\0"
                texts = [rx.sub(mask, t) for t in texts]
                if n: hits[cat][os.path.relpath(p, a.dir)].append((i, n))
cats = [r[0] for r in rules]
total = 0
for cat in dict.fromkeys(cats):
    print(f"## {cat}")
    if not hits[cat]: print("   none"); continue
    for f, ls in hits[cat].items():
        total += sum(n for _, n in ls)
        lines = ", ".join(str(i) for i, _ in ls[:40]) + (" ..." if len(ls) > 40 else "")
        print(f"   {f}: {len(ls)} line(s), {sum(n for _, n in ls)} hit(s); lines {lines}")
print(f"\ntotal hits: {total}")
