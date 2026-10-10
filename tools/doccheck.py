#!/usr/bin/env python3
"""Check the project documents against the doc map: every role resolved, partner sources and
Google Doc snapshots present and fresh, no unfilled placeholders in pack files, required sections,
requirement-to-test traceability across every ID source, and duplicate decision IDs.

Usage (from the repository root): python3 tools/doccheck.py [--docs-dir docs] [--strict]
Exit code is 1 only with --strict and at least one problem."""
import argparse, datetime, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import docmap  # noqa: E402

REQUIRED = {  # pack file -> headings it must keep
    "product-thesis.md": ["# Core thesis", "## 1. Endpoint", "## 2. Evidence", "## 5. Product bet", "## 7. Roadmap"],
    "implementation-plan.md": ["## 3. Requirements", "## 4. System design", "### 6.1 Step cards", "## 7. Acceptance"],
    "decisions.md": ["# Decisions"],
    "data-model.md": ["## 2. Entities and relationships", "## 3. Field classification"],
    "progress.md": ["## Step status", "## Questions for planning"],
    "traceability.md": ["| ID | Status |"],
    "doc-map.md": ["## Roles", "## Requirement IDs"],
}
PLACEHOLDER = docmap.PLACEHOLDER
GUIDE = re.compile(r"<!--\s*guide:")
ROW_ID = re.compile(r"^\|\s*`?([A-Z][A-Za-z0-9_-]*\d)`?\s*\|", re.M)
STATUSES = {"exists", "partial", "missing", "conflicts"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--docs-dir", default="docs"); ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(); docs = a.docs_dir.strip("/"); d = Path(docs)
    if not d.is_dir(): print(f"docs dir not found: {d}"); return 2
    problems = 0
    def flag(msg, n=1):
        nonlocal problems; problems += n; print("  " + msg)
    print(f"# doccheck: {d}\n")
    m = docmap.load(docs)

    print("## Doc map")
    need = set()  # files that must exist with their required headings
    overlays, decisions_files = [], []
    if not m:
        flag("doc-map.md missing; every role falls back to the pack's files")
        need |= set(REQUIRED) - {"doc-map.md"}
        decisions_files = [d / "decisions.md"]
    else:
        max_age = int(m["settings"].get("snapshot_max_age_days", "14") or 14)
        seen_roles = {r["role"] for r in m["roles"]}
        for role in docmap.ROLES:
            if role not in seen_roles: flag(f"{role}: no row (add one, mode skip if unused)")
        for r in m["roles"]:
            role, mode = r["role"], r["mode"]
            if role not in docmap.ROLES: flag(f"'{role}': unknown role"); continue
            if mode not in docmap.MODES: flag(f"{role}: mode '{mode}' is not new/adopt/extend/skip"); continue
            if r["confirmed"] != "yes": flag(f"{role}: not confirmed ({mode} {r['source']})".rstrip())
            spec = docmap.ROLES[role]
            if mode == "new":
                need |= {f for f in spec["files"] if f.endswith(".md") and f in REQUIRED}
                if role == "decisions": decisions_files.append(d / "decisions.md")
            elif mode in ("adopt", "extend"):
                src = r["source"]
                if docmap.blank(src): flag(f"{role}: {mode} with no source"); continue
                if docmap.is_url(src):
                    local = r["local"].replace("{{DOCS}}", docs)
                    if docmap.blank(local) or not Path(local).exists():
                        flag(f"{role}: no snapshot of {src}; run tools/docmap.py snapshot <url> <file>")
                    else:
                        try:
                            age = (datetime.date.today() - datetime.date.fromisoformat(r["snapshot"])).days
                            if age > max_age: flag(f"{role}: snapshot {local} is {age} days old (limit {max_age}); refresh it")
                        except ValueError:
                            flag(f"{role}: snapshot date missing for {local}")
                elif not Path(src).exists():
                    flag(f"{role}: source {src} not found")
                if spec["overlay"]:
                    ov = d / "overlays" / spec["overlay"]
                    if not ov.exists(): flag(f"{role}: overlay {ov} missing; run install.py --apply-map")
                    else:
                        overlays.append(ov)
                        if role == "decisions": decisions_files.append(ov)
        need |= {"progress.md", "traceability.md", "doc-map.md"}
        if not problems: print("  every role resolved")

    print("\n## Placeholders and guide notes still in pack files")
    mf = d / ".starter-manifest"
    if mf.exists():
        files = {Path(l.split(" ", 1)[1].strip()) for l in mf.read_text().splitlines() if l.startswith(("new ", "sidecar "))}
        files = sorted(f for f in files if f.suffix == ".md" and f.exists() and d in f.parents)
    else:
        files = sorted(f for f in d.rglob("*.md") if "external" not in f.relative_to(d).parts)
    rows = []
    for f in files:
        t = f.read_text(errors="replace"); p, g = len(PLACEHOLDER.findall(t)), len(GUIDE.findall(t))
        if p or g: rows.append((f.relative_to(d), p, g))
    for r, p, g in rows: print(f"  {r}: {p} placeholder(s), {g} guide note(s)")
    if not rows: print("  none")
    problems += sum(1 for _, p, _ in rows if p)

    print("\n## Required sections")
    bad = False
    for name in sorted(need):
        f = d / name
        if not f.exists(): flag(f"{name}: file missing"); bad = True; continue
        miss = [h for h in REQUIRED[name] if h not in f.read_text(errors="replace")]
        if miss: flag(f"{name}: missing {miss}"); bad = True
    for ov in overlays:
        if "**Source of truth:**" not in ov.read_text(errors="replace"):
            flag(f"{ov.relative_to(d)}: missing the 'Source of truth' line"); bad = True
    if not bad: print("  all present")

    print("\n## Traceability")
    trace = d / "traceability.md"
    if m and trace.exists():
        req, unreadable = docmap.collect_ids(m, docs)
        req = {k: v for k, v in req.items() if not PLACEHOLDER.search(k)}
        for s in unreadable: flag(f"ID source not readable: {s} (missing file or snapshot)")
        pats = [docmap.id_regex(s["pattern"]) for s in m["ids"]]
        rows = {}
        for line in trace.read_text().splitlines():
            mm = ROW_ID.match(line)
            if mm and (not pats or any(p.fullmatch(mm.group(1)) or p.search(mm.group(1)) for p in pats)):
                rows[mm.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")][1:]
        by_src = {}
        for k, v in req.items(): by_src[v] = by_src.get(v, 0) + 1
        print(f"  requirement IDs found: {len(req)} ({', '.join(f'{n} in {s}' for s, n in by_src.items()) or 'none'}); rows in matrix: {len(rows)}")
        not_traced = sorted(r for r in req if r not in rows)
        orphan = sorted(r for r in rows if r not in req)
        unverified = sorted(r for r, c in rows.items() if len(c) < 3 or c[2].lower() in ("", "none") or PLACEHOLDER.search(c[2]))
        bad_status = sorted(r for r, c in rows.items() if not c or c[0].strip("` ") not in STATUSES)
        not_done = sorted(r for r, c in rows.items() if c and c[0].strip("` ") in ("partial", "missing", "conflicts"))
        for label, items, counts in (("in a source, not in the matrix", not_traced, True), ("in the matrix, in no source", orphan, True),
                                     ("no test or named check", unverified, True), ("status not exists/partial/missing/conflicts", bad_status, True),
                                     ("not yet complete (partial/missing/conflicts)", not_done, False)):
            if items:
                print(f"  {label}: {', '.join(items)}")
                if counts: problems += len(items)
    else:
        print("  skipped (doc map or matrix missing)")

    print("\n## Decision IDs")
    for f in decisions_files:
        if f.exists():
            ids = [i for i in ROW_ID.findall(f.read_text()) if not PLACEHOLDER.search(i)]
            dup = sorted({i for i in ids if ids.count(i) > 1})
            print(f"  {f.relative_to(d)}: {len(ids)} decision(s)" + (f"; duplicate IDs: {', '.join(dup)}" if dup else "; no duplicates"))
            problems += len(dup)

    print(f"\nproblems: {problems}")
    return 1 if (a.strict and problems) else 0

if __name__ == "__main__":
    sys.exit(main())
