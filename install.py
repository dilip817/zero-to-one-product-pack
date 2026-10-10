#!/usr/bin/env python3
"""Install the zero-to-one starter pack into a repository without overwriting anything.

  python3 install.py <repo> --mode greenfield                       everything, every role "new"
  python3 install.py <repo> --mode brownfield --docs-dir docs/z21   core files + a doc map proposed from what already exists
  python3 install.py <repo> --apply-map --docs-dir docs/z21         install templates or overlays for the confirmed doc-map rows
  add --dry-run to any of them to see what would happen

A file that already exists is never overwritten: if it differs, the pack's version is written next
to it as <name>.starter.<ext>; if it is identical it is reported as up to date. Safe to re-run."""
import argparse, datetime, os, shutil, stat, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import docmap  # noqa: E402

ROLE_FILES = {f for spec in docmap.ROLES.values() for f in spec["files"]}

class Installer:
    def __init__(self, target, docs, dry):
        self.t, self.docs, self.dry = Path(target).resolve(), docs, dry
        self.new, self.sidecar, self.same, self.skipped, self.kept = [], [], [], [], []
        mf = self.t / docs / ".starter-manifest"
        self.ours = {l.split(" ", 1)[1].strip() for l in mf.read_text().splitlines()
                     if l.startswith(("new ", "sidecar "))} if mf.exists() else set()

    def place(self, src, rel, subs=None):
        text = Path(src).read_text().replace("{{DOCS}}", self.docs)
        for k, v in (subs or {}).items(): text = text.replace(k, v)
        dest = self.t / rel
        if dest.exists():
            if dest.read_text(errors="replace") == text: self.same.append(rel); return
            if rel in self.ours: self.kept.append(rel); return  # the pack created it and you have edited it since
            name = Path(rel).name
            alt_name = f"{name.rsplit('.', 1)[0]}.starter.{name.rsplit('.', 1)[1]}" if "." in name[1:] else name + ".starter"
            alt = str(Path(rel).parent / alt_name) if str(Path(rel).parent) != "." else alt_name
            if (self.t / alt).exists():
                if (self.t / alt).read_text(errors="replace") == text: self.same.append(alt)
                else: self.skipped.append(f"{rel} (and {alt}) already exist; delete {alt} to get the latest")
                return
            rel, dest = alt, self.t / alt; self.sidecar.append(rel)
        else:
            self.new.append(rel)
        if not self.dry:
            dest.parent.mkdir(parents=True, exist_ok=True); dest.write_text(text)
            if os.access(src, os.X_OK): dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def core(self, mode):
        tdocs = HERE / "templates" / "docs"
        for f in sorted(p for p in tdocs.rglob("*") if p.is_file()):
            rel = f.relative_to(tdocs).as_posix()
            if rel in ROLE_FILES or rel == "doc-map.md": continue
            if mode == "greenfield" and rel == "existing-system-audit.md": continue
            self.place(f, f"{self.docs}/{rel}")
        self.place(HERE / "templates" / "CLAUDE.md", "CLAUDE.md")
        self.place(HERE / "templates" / "README.project.md", "README.md")
        for f in sorted(p for p in (HERE / "templates" / ".claude").rglob("*") if p.is_file()):
            rel = f.relative_to(HERE / "templates").as_posix()
            if mode == "greenfield" and "/kickoff/" in rel: continue
            self.place(f, rel)
        for f in sorted(p for p in (HERE / "tools").rglob("*") if p.is_file() and "__pycache__" not in p.parts):
            self.place(f, f.relative_to(HERE).as_posix())

    def doc_map(self, mode):
        rel = f"{self.docs}/doc-map.md"
        if (self.t / rel).exists():
            print(f"{rel} exists and is kept; `python3 tools/docmap.py detect --docs-dir {self.docs}` shows fresh proposals.")
            return None
        if mode == "greenfield":
            text = docmap.render(self.docs, "greenfield")
            found = ([], [], [])
        else:
            found = docmap.detect(self.t, self.docs)
            text = docmap.render(self.docs, "brownfield", *found)
        self.new.append(rel)
        if not self.dry:
            (self.t / rel).parent.mkdir(parents=True, exist_ok=True); (self.t / rel).write_text(text)
        return found

    def apply_map(self, text_if_dry=None):
        m = docmap.load(self.docs, self.t)
        if m is None and text_if_dry is not None:  # dry run of a greenfield install: map not written yet
            m = {"roles": [{"role": r, "mode": "new", "source": "", "local": "", "confirmed": "yes"} for r in docmap.ROLES]}
        if m is None: sys.exit(f"no {self.docs}/doc-map.md; run the installer with --mode first")
        pending, problems = [], []
        by_role = {}
        for r in m["roles"]:
            if r["role"] not in docmap.ROLES: problems.append(f"unknown role '{r['role']}' ({r['source'] or 'no source'})"); continue
            if r["mode"] not in docmap.MODES: problems.append(f"{r['role']}: mode '{r['mode']}' is not new/adopt/extend/skip"); continue
            if r["confirmed"] != "yes": pending.append(f"{r['role']} ({r['mode']} {r['source'] or ''})".strip()); continue
            by_role.setdefault(r["role"], []).append(r)
        for role, rows in by_role.items():
            spec = docmap.ROLES[role]
            if any(r["mode"] == "new" for r in rows):
                for f in spec["files"]: self.place(HERE / "templates" / "docs" / f, f"{self.docs}/{f}")
            ext = [r for r in rows if r["mode"] in ("adopt", "extend")]
            if ext and spec["overlay"]:
                srcs = "; ".join(f"`{r['source']}`" + (f" (read the snapshot `{r['local']}`)" if docmap.is_url(r["source"]) else "")
                                 + (" [extend]" if r["mode"] == "extend" else "") for r in ext)
                self.place(HERE / "templates" / "overlays" / spec["overlay"], f"{self.docs}/overlays/{spec['overlay']}",
                           {"{{SOURCE}}": srcs})
        return pending, problems

    def gitignore(self):
        gi = self.t / ".gitignore"; cur = gi.read_text().splitlines() if gi.exists() else []
        add = [x for x in ("ai-history/", "tools/history/redaction-config.json", ".env*") if x not in cur]
        if add and not self.dry:
            pre = "\n" if gi.exists() and gi.read_text() and not gi.read_text().endswith("\n") else ""
            with gi.open("a") as fh: fh.write(pre + "# zero-to-one starter pack\n" + "\n".join(add) + "\n")
        return add

    def report(self, label):
        def lst(title, xs):
            if xs: print(f"{title}: {len(xs)}"); [print("  " + x) for x in xs]
        lst("New files", self.new)
        lst("Already existed and differ, written next to them for you to merge", self.sidecar)
        lst("Skipped", self.skipped)
        if self.same: print(f"Already up to date: {len(self.same)}")
        if self.kept: print(f"Installed earlier and edited since, kept as they are: {len(self.kept)}")
        if not self.dry and (self.new or self.sidecar):
            mf = self.t / self.docs / ".starter-manifest"; mf.parent.mkdir(parents=True, exist_ok=True)
            with mf.open("a") as fh:
                fh.write(f"installed {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ} {label} docs={self.docs}\n")
                for x in self.new: fh.write(f"new {x}\n")
                for x in self.sidecar: fh.write(f"sidecar {x}\n")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target"); ap.add_argument("--mode", choices=["greenfield", "brownfield"])
    ap.add_argument("--docs-dir", default="docs"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply-map", action="store_true")
    a = ap.parse_args()
    if not Path(a.target).is_dir(): sys.exit(f"target not found: {a.target}")
    if not a.mode and not a.apply_map: sys.exit("give --mode greenfield|brownfield, or --apply-map")
    docs = a.docs_dir.strip("/") or "docs"
    ins = Installer(a.target, docs, a.dry_run)
    print(f"Target: {ins.t}   Docs: {docs}   {'(dry run, nothing written)' if a.dry_run else ''}")
    pending = problems = []; found = None
    if a.mode:
        ins.core(a.mode)
        found = ins.doc_map(a.mode)
    if a.mode == "greenfield" or a.apply_map:
        pending, problems = ins.apply_map(text_if_dry="" if a.dry_run else None)
    added = ins.gitignore()
    ins.report(f"mode={a.mode or 'apply-map'}")
    if added: print(".gitignore entries added: " + " ".join(added))
    if found and a.mode == "brownfield":
        rows, idrows, gdocs = found
        print(f"\nDetected {len(rows)} existing document(s) or folder(s), {len(idrows)} requirement-ID pattern(s), {len(gdocs)} Google Doc link(s):")
        for role, src, why in rows: print(f"  {role:<13} {src}  ({why})")
        for g in gdocs:
            title = f' "{g["title"]}"' if g["title"] else ""
            print(f"  {g['role']:<13} {g['url']}  (Google {g['kind']}{title})")
    if problems: print("\nDoc-map problems:"); [print("  " + p) for p in problems]
    if pending: print(f"\nNot applied, waiting for Confirmed = yes: {len(pending)}"); [print("  " + p) for p in pending]
    print()
    if a.mode == "brownfield":
        print(f"Next: (1) merge any *.starter.* files; (2) run /kickoff in Claude Code, which checks each proposed row in {docs}/doc-map.md;\n"
              f"(3) set Mode and Confirmed = yes per row; (4) bash {HERE}/install.sh {a.target} --apply-map --docs-dir {docs}")
    elif a.mode == "greenfield":
        print(f"Next: fill {docs}/project-charter.md and the Core thesis in {docs}/product-thesis.md, then {docs}/implementation-plan.md.")
    print(f"Check progress any time: python3 tools/doccheck.py --docs-dir {docs}")

if __name__ == "__main__":
    main()
