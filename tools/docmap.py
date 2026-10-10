#!/usr/bin/env python3
"""The doc map: where each kind of project document lives (the pack's template, a partner's
existing file, or a snapshot of a Google Doc). The installer, doccheck and the session skills
all read {docs}/doc-map.md, so a partner's PRD, ERD, evals or ADRs are used in place, not copied.

Usage (run from the repository root):
  python3 tools/docmap.py show     [--docs-dir docs]        roles, modes and where each resolves
  python3 tools/docmap.py detect   [--docs-dir docs]        propose rows for documents that already exist
  python3 tools/docmap.py snapshot <google-doc-url> <downloaded.md|.txt|.docx> [--docs-dir docs]
"""
import argparse, datetime, os, re, shutil, subprocess, sys
from pathlib import Path

# role -> pack files used when mode is "new", overlay used when mode is "adopt" or "extend", and what it is.
ROLES = {
    "charter":      {"files": ["project-charter.md"], "overlay": "charter.md",
                     "what": "Partner, ownership, constraints, data and IP rules, definition of done"},
    "thesis":       {"files": ["product-thesis.md"], "overlay": "thesis.md",
                     "what": "Why this, for whom, endpoint, headline metrics, evidence, bet (a PRD usually plays this role)"},
    "roadmap":      {"files": [], "overlay": "roadmap.md", "in": "product-thesis.md §7",
                     "what": "Now, next, later, each tied to a requirement ID and a metric"},
    "requirements": {"files": [], "overlay": None, "in": "implementation-plan.md §3",
                     "what": "Requirement IDs that are traced to code and tests (see Requirement IDs below)"},
    "plan":         {"files": ["implementation-plan.md"], "overlay": "step-cards.md",
                     "what": "System design, step cards with Done when, acceptance"},
    "data-model":   {"files": ["data-model.md"], "overlay": "data-model.md",
                     "what": "Entities and relationships (ERD), data classification, retention, migrations"},
    "design":       {"files": ["design/design-spec.md"], "overlay": "design.md",
                     "what": "Screens, states, components, copy rules"},
    "evals":        {"files": ["evals/eval-plan.md", "evals/RESULTS.md", "evals/dataset-schema.md", "evals/dataset.example.json"],
                     "overlay": "evals.md", "what": "Pre-registered evaluation of the AI parts against a baseline"},
    "decisions":    {"files": ["decisions.md"], "overlay": "decisions.md",
                     "what": "One line per decision; the latest wins (ADRs play this role)"},
    "research":     {"files": ["evidence/research-note.md"], "overlay": "research.md",
                     "what": "User and market evidence, tagged by strength"},
}
MODES = {"new", "adopt", "extend", "skip"}
PACK_ID = r"[A-Z]{1,3}R\d+"
URL = re.compile(r"https?://\S+")
GDOC = re.compile(r"https://docs\.google\.com/(document|spreadsheets|presentation)/d/([A-Za-z0-9_-]{10,})[^\s)>\]\"']*")
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")

def is_url(s): return bool(URL.match(s or ""))
def blank(s): return (s or "").strip() in ("", "—", "-") or bool(PLACEHOLDER.search(s or ""))

# ---------- parse ----------
def _table(text, heading):
    """Rows (as lists of cells) of the first table after a heading line that starts with `heading`."""
    lines = text.splitlines(); out = []; i = 0
    while i < len(lines) and not lines[i].startswith(heading): i += 1
    i += 1
    while i < len(lines) and not lines[i].startswith("|"):
        if lines[i].startswith("#"): return out
        i += 1
    header = True
    while i < len(lines) and lines[i].startswith("|"):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if header: header = False
        elif not set("".join(cells)) <= set("-: "): out.append(cells)
        i += 1
    return out

def load(docs, root="."):
    p = Path(root) / docs / "doc-map.md"
    if not p.exists(): return None
    t = p.read_text(errors="replace")
    roles = []
    for c in _table(t, "## Roles"):
        c += [""] * (7 - len(c))
        roles.append({"role": c[0].strip("` "), "mode": c[1].strip("` ").lower(), "source": c[2].strip("` "),
                      "local": c[3].strip("` "), "snapshot": c[4].strip(), "confirmed": c[5].strip().lower(), "notes": c[6]})
    ids = []
    for c in _table(t, "## Requirement IDs"):
        c += [""] * 3
        if not blank(c[0]) and not blank(c[1]):
            ids.append({"source": c[0].strip("` "), "pattern": c[1].strip("` "), "notes": c[2]})
    settings = {c[0].strip("` "): c[1].strip("` ") for c in _table(t, "## Settings") if len(c) >= 2}
    return {"path": p, "roles": roles, "ids": ids, "settings": settings}

def id_patterns(text):
    """{(prefix, dash): set(numbers)} for IDs defined at a line start, heading, bullet or first table cell."""
    out = {}
    for pre, dash, num in ID_DEF.findall(text):
        if pre not in ID_STOP: out.setdefault((pre, dash), set()).add(num)
    return {k: v for k, v in out.items() if len(v) >= 3}

def id_regex(pattern):
    return re.compile(r"(?<![\w-])(?:" + pattern + r")(?![\w-])")

def collect_ids(m, docs, root="."):
    """{id: source} across every Requirement IDs source; plus a list of sources that could not be read."""
    found, unreadable = {}, []
    by_url = {r["source"]: r["local"] for r in m["roles"] if is_url(r["source"])}
    for s in m["ids"]:
        path = by_url.get(s["source"], "") if is_url(s["source"]) else s["source"]
        path = path.replace("{{DOCS}}", docs)
        p = Path(root) / path if path else None
        if not p or not p.exists(): unreadable.append(s["source"]); continue
        files = sorted(p.rglob("*.md")) if p.is_dir() else [p]
        rx = id_regex(s["pattern"])
        for f in files:
            for x in rx.findall(f.read_text(errors="replace")):
                found.setdefault(x, s["source"])
    return found, unreadable

# ---------- detect ----------
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".next", "out", "target", "venv", ".venv",
             "__pycache__", "ai-history", "coverage", ".claude", ".turbo", ".cache"}
DOC_EXT = (".md", ".mdx", ".txt", ".markdown")
NAME_RULES = [  # (role, regex on the lower-case path, why)
    ("thesis",     r"(^|/)(prd|product[-_ ]?requirements?|product[-_ ]?spec|one[-_ ]?pager|vision|strategy|product[-_ ]?brief|thesis)[^/]*\.(md|mdx|txt)$", "product document by name"),
    ("roadmap",    r"(^|/)[^/]*roadmap[^/]*\.(md|mdx|txt)$", "roadmap by name"),
    ("charter",    r"(^|/)[^/]*(charter|statement[-_ ]of[-_ ]work|sow|partnership)[^/]*\.(md|mdx|txt)$", "charter by name"),
    ("data-model", r"(^|/)schema\.prisma$|\.dbml$|(^|/)[^/]*(erd|er[-_]diagram|data[-_ ]?model|schema)[^/]*\.(md|mmd|sql|png|svg)$", "data model by name"),
    ("design",     r"(^|/)[^/]*(design[-_ ]?spec|ux|ui[-_ ]?spec|wireframes?|design)[^/]*\.(md|mdx)$", "design document by name"),
    ("evals",      r"(^|/)promptfooconfig\.(ya?ml|json)$|(^|/)[^/]*evals?[^/]*\.(md|ya?ml|json|py|ts|js)$", "eval file by name"),
    ("decisions",  r"(^|/)[^/]*decisions?([-_ ]?log)?\.md$", "decision log by name"),
    ("research",   r"(^|/)[^/]*(research|interviews?|insights|user[-_ ]?studies)[^/]*\.(md|mdx|txt)$", "research by name"),
]
DIR_RULES = [("decisions", r"(^|/)(adrs?|decisions|architecture[-_]decisions?)$", "ADR folder"),
             ("evals", r"(^|/)evals?$", "eval folder"),
             ("research", r"(^|/)(research|interviews)$", "research folder")]
TITLE_RULES = [("thesis", r"\b(prd|product requirements?|product spec|one[- ]?pager|vision|strategy|brief|thesis)\b"),
               ("roadmap", r"roadmap"), ("charter", r"\b(charter|sow|statement of work|partnership)\b"),
               ("data-model", r"\b(erd|data model|schema|entities)\b"), ("design", r"\b(design|ux|ui spec|wireframes?|mockups?)\b"),
               ("evals", r"\bevals?\b|evaluation"), ("decisions", r"\b(decisions?|adr)\b"),
               ("research", r"\b(research|interviews?|insights|survey)\b")]
ID_DEF = re.compile(r"^\s*(?:\|\s*|#{1,6}\s+|[-*]\s+(?:\*\*)?|\*\*)([A-Z][A-Z]{1,5})(-?)(\d{1,4})\b", re.M)
ID_STOP = {"ADR", "RFC", "ISO", "UTF", "SHA", "HTTP", "PR", "CVE", "TODO", "API", "UI", "UX", "MVP", "KPI", "OKR", "Q"}

def _walk(root, docs):
    root = Path(root); skip_docs = (root / docs).resolve()
    for d, dirs, files in os.walk(root):
        dp = Path(d)
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and (dp / x).resolve() != skip_docs)
        yield dp.relative_to(root).as_posix() if dp != root else "", sorted(dirs), sorted(files)

def detect(root=".", docs="docs"):
    """Propose (role, source, why) rows, requirement ID patterns and Google Docs. Proposals only."""
    rows, idrows, gdocs, seen = [], [], {}, set()
    claimed_dirs = []
    for rel, dirs, files in _walk(root, docs):
        for d in dirs:
            path = f"{rel}/{d}" if rel else d
            for role, rx, why in DIR_RULES:
                if re.search(rx, path.lower()):
                    n = sum(1 for _ in Path(root, path).rglob("*") if _.is_file())
                    rows.append((role, path + "/", f"{why}, {n} file(s)")); claimed_dirs.append(path + "/")
        for f in files:
            path = f"{rel}/{f}" if rel else f
            low = path.lower()
            if not any(path.startswith(c) for c in claimed_dirs):
                for role, rx, why in NAME_RULES:
                    if re.search(rx, low) and (role, path) not in seen:
                        if role == "design" and low.endswith(("readme.md",)): continue
                        seen.add((role, path)); rows.append((role, path, why)); break
            if low.endswith(DOC_EXT):
                try: text = Path(root, path).read_text(errors="replace")
                except Exception: continue
                if path.lower().endswith(".md") and "erdiagram" in text.lower() and ("data-model", path) not in seen:
                    seen.add(("data-model", path)); rows.append(("data-model", path, "contains a mermaid erDiagram"))
                for (pre, dash), nums in id_patterns(text).items():
                        idrows.append((path, f"{pre}{dash}\\d+", f"{len(nums)} IDs defined, e.g. {pre}{dash}{sorted(nums, key=int)[0]}"))
                for m in GDOC.finditer(text):
                    url = m.group(0); key = m.group(2)
                    if key in gdocs: continue
                    lt = re.search(r"\[([^\]]{2,80})\]\(" + re.escape(url), text)
                    gdocs[key] = {"url": url, "kind": m.group(1), "title": lt.group(1) if lt else "", "seen_in": path}
    for path, pat, why in idrows:
        rows.append(("requirements", path, f"requirement IDs: {why}"))
    for g in gdocs.values():
        g["role"] = next((r for r, rx in TITLE_RULES if re.search(rx, g["title"].lower())), "?")
    return rows, idrows, list(gdocs.values())

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "doc"

def render(docs, mode, rows=(), idrows=(), gdocs=()):
    """The doc-map.md text: greenfield = every role new and confirmed; brownfield = proposals to confirm."""
    today = datetime.date.today().isoformat()
    out = [f"# Doc map", "",
           f"**Last updated:** {today} · Planning confirms; the build agent proposes (installer, `/kickoff`) and never edits partner documents.",
           "",
           "<!-- guide: One row per role per source; a role can have several rows (e.g. a PRD and a Google Doc). "
           "Mode: new = use the pack's file; adopt = the partner's document is the source of truth and the pack adds only "
           "the missing sections in an overlay beside it; extend = as adopt, and the overlay's sections are meant to be "
           "pasted into the partner's document once they agree; skip = not used in this project. "
           "Source: a path from the repo root, a folder, or a URL. Local copy: for a URL, the snapshot the agent reads "
           "(`python3 tools/docmap.py snapshot <url> <file>`). Confirmed: yes once planning has checked the row; "
           "the installer applies confirmed rows only. -->", "",
           "## Roles", "",
           "| Role | Mode | Source | Local copy | Snapshot | Confirmed | Notes |",
           "|---|---|---|---|---|---|---|"]
    detected = {r for r, _, _ in rows}
    for role, spec in ROLES.items():
        mine = [r for r in rows if r[0] == role]
        if mine:
            for _, src, why in mine:
                out.append(f"| {role} | adopt | `{src}` | — | — | no | detected: {why}. {{{{what it covers; what is missing}}}} |")
        elif mode == "greenfield":
            where = spec["files"][0] if spec["files"] else spec.get("in", "")
            out.append(f"| {role} | new | `{docs}/{where}` | — | — | yes | {spec['what']} |" if spec["files"]
                       else f"| {role} | new | in `{docs}/{where}` | — | — | yes | {spec['what']} |")
        else:
            out.append(f"| {role} | new | — | — | — | no | nothing detected. {spec['what']} |")
    for g in gdocs:
        local = f"{docs}/external/{slug(g['title'] or g['kind'])}-{GDOC.match(g['url']).group(2)[:6]}.md"
        title = f" \"{g['title']}\"" if g["title"] else ""
        out.append(f"| {g['role']} | adopt | {g['url']} | `{local}` | — | no | Google {g['kind']}{title}, linked from `{g['seen_in']}`. Set the role, or delete the row |")
    out += ["", "## Requirement IDs", "",
            "<!-- guide: Every source whose IDs are traced in traceability.md, with the ID pattern as a regular expression. "
            "Keep the pack's own row for requirements the partner's documents do not cover (safety, quality, measurement). -->", "",
            "| Source | ID pattern | Notes |", "|---|---|---|",
            f"| `{docs}/implementation-plan.md` | `{PACK_ID}` | the pack's FR, SR, QR, MR requirements |"]
    for path, pat, why in idrows:
        out.append(f"| `{path}` | `{pat}` | detected: {why} |")
    out += ["", "## Settings", "", "| Key | Value |", "|---|---|", "| snapshot_max_age_days | 14 |", ""]
    return "\n".join(out)

# ---------- snapshot ----------
def snapshot(url, file, docs, root="."):
    m = load(docs, root)
    if not m: sys.exit(f"no {docs}/doc-map.md; install the pack first")
    rows = [r for r in m["roles"] if r["source"] == url or (GDOC.match(url) and GDOC.match(r["source"] or "")
            and GDOC.match(url).group(2) == GDOC.match(r["source"]).group(2))]
    if not rows: sys.exit("that URL is not in the doc map; add a row for it under ## Roles first")
    local = rows[0]["local"] if not blank(rows[0]["local"]) else f"{docs}/external/{slug(rows[0]['role'])}-{(GDOC.match(url).group(2) if GDOC.match(url) else slug(url))[:6]}.md"
    src = Path(file)
    if src.suffix.lower() == ".docx":
        if not shutil.which("pandoc"): sys.exit("a .docx needs pandoc; or download the Google Doc as Markdown (File > Download > Markdown)")
        body = subprocess.run(["pandoc", "-t", "gfm", str(src)], capture_output=True, text=True, check=True).stdout
    else:
        body = src.read_text(errors="replace")
    today = datetime.date.today().isoformat()
    dest = Path(root) / local; dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"<!-- snapshot of {url} taken {today}. Read-only copy: the Google Doc is the source of truth. "
                    f"Refresh with: python3 tools/docmap.py snapshot <url> <file> -->\n\n" + body)
    t = m["path"].read_text()
    new = []
    for line in t.splitlines():
        cells = line.split("|")
        if line.startswith("|") and len(cells) > 6 and (cells[3].strip() == url or (GDOC.match(url) and GDOC.match(cells[3].strip() or "") and GDOC.match(cells[3].strip()).group(2) == GDOC.match(url).group(2))):
            cells[4] = f" `{local}` "; cells[5] = f" {today} "; line = "|".join(cells)
        new.append(line)
    m["path"].write_text("\n".join(new) + ("\n" if t.endswith("\n") else ""))
    print(f"wrote {local} ({len(body.splitlines())} lines) and set its snapshot date to {today} in {docs}/doc-map.md")
    known = {s["source"] for s in m["ids"]}
    for (pre, dash), nums in id_patterns(body).items():
        if url not in known:
            print(f"found {len(nums)} requirement IDs like {pre}{dash}{min(nums, key=int)}; to trace them, add this row under "
                  f"## Requirement IDs:\n| {url} | `{pre}{dash}\\d+` | from the Google Doc |")

# ---------- cli ----------
def show(docs, root="."):
    m = load(docs, root)
    if not m: sys.exit(f"no {docs}/doc-map.md")
    for r in m["roles"]:
        spec = ROLES.get(r["role"])
        if r["mode"] == "new" and spec:
            where = ", ".join(f"{docs}/{f}" for f in spec["files"]) or f"{docs}/{spec.get('in')}"
        elif r["mode"] in ("adopt", "extend"):
            where = (r["local"] if is_url(r["source"]) else r["source"]) + (f" + {docs}/overlays/{spec['overlay']}" if spec and spec["overlay"] else "")
        else:
            where = "not used"
        print(f"{r['role']:<13} {r['mode']:<7} {'' if r['confirmed']=='yes' else '(unconfirmed) '}{where}")
    print("\nrequirement IDs:")
    ids, bad = collect_ids(m, docs, root)
    for s in m["ids"]:
        n = sum(1 for v in ids.values() if v == s["source"])
        print(f"  {s['source']}  /{s['pattern']}/  {n} ID(s)" + ("  (cannot read)" if s["source"] in bad else ""))

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["show", "detect", "snapshot"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--docs-dir", default="docs")
    a = ap.parse_args(); docs = a.docs_dir.rstrip("/")
    if a.cmd == "show": show(docs)
    elif a.cmd == "detect":
        rows, idrows, gdocs = detect(".", docs)
        print(render(docs, "brownfield", rows, idrows, gdocs))
        print("\n<!-- proposals only: copy the rows you agree with into", f"{docs}/doc-map.md -->")
    elif a.cmd == "snapshot":
        if len(a.args) != 2: sys.exit("usage: docmap.py snapshot <url> <downloaded-file>")
        snapshot(a.args[0], a.args[1], docs)

if __name__ == "__main__":
    main()
