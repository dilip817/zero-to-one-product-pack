#!/usr/bin/env python3
"""End-to-end tests for the starter pack, on temporary copies of a synthetic partner repo.
Run: python3 tests/test_pack.py   (exit code 1 on any failure; no dependencies)"""
import json, re, shutil, subprocess, sys, tempfile, datetime
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
FIX = PACK / "tests" / "fixtures" / "brownfield"
results = []

def run(args, cwd=None, ok=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if ok and p.returncode != 0: raise AssertionError(f"{args} failed:\n{p.stdout}\n{p.stderr}")
    return p

def check(name, cond, detail=""):
    results.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  -- {detail}"))

def install(repo, *args): return run([sys.executable, str(PACK / "install.py"), str(repo), *args]).stdout
def doccheck(repo, docs): return run([sys.executable, "tools/doccheck.py", "--docs-dir", docs], cwd=repo).stdout
def confirm_all(mapfile, **modes):
    t = mapfile.read_text().replace("{{what it covers; what is missing}}", "checked")
    for role, mode in modes.items(): t = re.sub(rf"^\| {role} \| \w+ \|", f"| {role} | {mode} |", t, flags=re.M)
    mapfile.write_text(re.sub(r"\| no \|", "| yes |", t))

def greenfield(tmp):
    g = tmp / "green"; g.mkdir()
    out = install(g, "--mode", "greenfield", "--dry-run")
    check("greenfield dry run writes nothing", not any(g.iterdir()), out)
    install(g, "--mode", "greenfield")
    for f in ["docs/doc-map.md", "docs/product-thesis.md", "docs/implementation-plan.md", "docs/data-model.md",
              "docs/decisions.md", "docs/evals/eval-plan.md", "CLAUDE.md", ".claude/skills/start-step/SKILL.md",
              "tools/docmap.py", "tools/doccheck.py", "tools/history/redact.py"]:
        check(f"greenfield installs {f}", (g / f).exists())
    check("greenfield has no kickoff skill or audit", not (g / ".claude/skills/kickoff").exists() and not (g / "docs/existing-system-audit.md").exists())
    check("greenfield has no overlays", not (g / "docs/overlays").exists())
    check("no {{DOCS}} left", not any("{{DOCS}}" in p.read_text(errors="ignore") for p in g.rglob("*") if p.is_file()))
    out = doccheck(g, "docs")
    check("greenfield doccheck: every role resolved", "every role resolved" in out, out[:400])
    check("greenfield doccheck: pack IDs traced", "requirement IDs found: 5" in out, out)
    out = install(g, "--mode", "greenfield")
    check("greenfield re-run is a no-op", "New files" not in out and "differ" not in out, out)

def brownfield(tmp):
    b = tmp / "brown"; shutil.copytree(FIX, b)
    before = {p.relative_to(b): p.read_bytes() for p in b.rglob("*") if p.is_file()}
    out = install(b, "--mode", "brownfield", "--docs-dir", "docs/z21")
    after = {p: (b / p).read_bytes() for p in before}
    check("brownfield changes no partner file", before == after)
    check("partner CLAUDE.md gets a sidecar", (b / "CLAUDE.starter.md").exists())
    m = (b / "docs/z21/doc-map.md").read_text()
    for role, src in [("thesis", "docs/PRD.md"), ("requirements", "docs/PRD.md"), ("data-model", "prisma/schema.prisma"),
                      ("evals", "evals/"), ("decisions", "docs/adr/"), ("research", "docs/research/")]:
        check(f"detects {role} -> {src}", re.search(rf"^\| {role} \| adopt \| `{re.escape(src)}`", m, re.M), m)
    check("detects REQ- IDs", "`REQ-\\d+`" in m)
    check("does not treat ADR-0001 as requirement IDs", "ADR-\\d+" not in m)
    check("finds 3 Google links with role guesses", m.count("docs.google.com") == 3 and '| thesis | adopt | https://docs.google.com/document/d/1AbC' in m, m)
    check("nothing applied before confirmation", not (b / "docs/z21/product-thesis.md").exists() and not (b / "docs/z21/overlays").exists())
    check("kickoff skill installed", (b / ".claude/skills/kickoff/SKILL.md").exists())

    confirm_all(b / "docs/z21/doc-map.md", roadmap="skip")
    install(b, "--apply-map", "--docs-dir", "docs/z21")
    check("adopted roles get overlays", all((b / f"docs/z21/overlays/{o}.md").exists() for o in ["thesis", "data-model", "evals", "decisions", "research", "design"]))
    check("adopted roles get no duplicate template", not any((b / f"docs/z21/{f}").exists() for f in ["product-thesis.md", "decisions.md", "evals/eval-plan.md", "data-model.md", "evidence/research-note.md"]))
    check("new roles get templates", all((b / f"docs/z21/{f}").exists() for f in ["project-charter.md", "implementation-plan.md", "design/design-spec.md"]))
    ov = (b / "docs/z21/overlays/thesis.md").read_text()
    check("overlay names both sources, URL via snapshot", "`docs/PRD.md`" in ov and "read the snapshot" in ov, ov[:300])

    out = doccheck(b, "docs/z21")
    check("doccheck flags missing snapshots", out.count("no snapshot of") == 3, out)
    check("doccheck traces PRD IDs", "4 in docs/PRD.md" in out and "REQ-1" in out, out)

    dl = tmp / "dl"; dl.mkdir()
    (dl / "s.md").write_text("# Strategy\n- **US-1** a\n- **US-2** b\n- **US-3** c\n")
    url = "https://docs.google.com/document/d/1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789/edit"
    out = run([sys.executable, "tools/docmap.py", "snapshot", url + "?tab=t.0", str(dl / "s.md"), "--docs-dir", "docs/z21"], cwd=b).stdout
    check("snapshot matches the URL by document ID", "wrote docs/z21/external/" in out, out)
    check("snapshot suggests the US- ID row", "`US-\\d+`" in out, out)
    mp = b / "docs/z21/doc-map.md"; t = mp.read_text()
    mp.write_text(t.replace("| `docs/PRD.md` | `REQ-\\d+` |", f"| {url} | `US-\\d+` | from the Google Doc |\n| `docs/PRD.md` | `REQ-\\d+` |"))
    p = run([sys.executable, "tools/docmap.py", "snapshot", "https://docs.google.com/document/d/notInTheMap123/edit", str(dl / "s.md"), "--docs-dir", "docs/z21"], cwd=b, ok=False)
    check("snapshot refuses a URL that is not in the map", p.returncode != 0)
    out = doccheck(b, "docs/z21")
    check("doccheck traces IDs from the Google Doc snapshot", "3 in https://docs.google.com" in out, out)
    check("only the two un-snapshotted links remain flagged", out.count("no snapshot of") == 2, out)

    old = (datetime.date.today() - datetime.timedelta(days=40)).isoformat()
    t = mp.read_text(); mp.write_text(t.replace(f"| {datetime.date.today().isoformat()} |", f"| {old} |"))
    check("doccheck flags a stale snapshot", "days old" in doccheck(b, "docs/z21"))

    (b / "docs/z21/traceability.md").write_text(
        "| ID | Status | Code location | Verified by | Last checked | Notes |\n|---|---|---|---|---|---|\n"
        "| REQ-1 | exists | src/reminders.ts:1 | tests/r.test.ts | d | |\n| REQ-2 | missing | — | none | d | |\n| REQ-9 | exists | x | y | d | |\n")
    out = doccheck(b, "docs/z21")
    check("trace: orphan, no-test and incomplete rows flagged", "in no source: REQ-9" in out and "no test or named check: REQ-2" in out and "not yet complete" in out, out)
    (b / "docs/z21/overlays/decisions.md").write_text("# Overlay\n**Source of truth:** x\n| ID | Date | Decision | Record |\n|---|---|---|---|\n| ADR-0001 | d | a | r |\n| ADR-0001 | d | b | r |\n")
    check("duplicate decision IDs in the ADR index flagged", "duplicate IDs: ADR-0001" in doccheck(b, "docs/z21"))
    p = run([sys.executable, "tools/doccheck.py", "--docs-dir", "docs/z21", "--strict"], cwd=b, ok=False)
    check("--strict exits 1 with problems", p.returncode == 1)

    out = install(b, "--apply-map", "--docs-dir", "docs/z21") + install(b, "--mode", "brownfield", "--docs-dir", "docs/z21")
    check("re-runs keep edited files without sidecars", "differ" not in out and "edited since" in out, out)
    check("re-run keeps the confirmed doc map", "| yes |" in mp.read_text())
    show = run([sys.executable, "tools/docmap.py", "show", "--docs-dir", "docs/z21"], cwd=b).stdout
    check("docmap show resolves roles", "thesis        adopt   docs/PRD.md + docs/z21/overlays/thesis.md" in show, show)

def history(tmp):
    h = tmp / "hist"; raw = h / "raw"; (raw / "sub").mkdir(parents=True)
    lines = [{"m": "mail owner@founder.test, call (555) 555-0100\nfriend:jane@acme.io"},
             {"m": "Contact\njane@acme.io or noreply@anthropic.com; host my-laptop.local"},
             {"m": "key sk-ant-" + "A" * 30}, {"m": "Owner Name says hi"}]
    (raw / "s.jsonl").write_text("\n".join(json.dumps(l) for l in lines) + "\nnot json owner@founder.test\n")
    (raw / "sub/m.json").write_text(json.dumps({"by": "jane@acme.io\nx"}, indent=2))
    cfg = {"redact": [{"category": "personal email address", "literal": ["owner@founder.test"]},
                      {"category": "phone number", "regex": [r"\(?555\)?[ .\-]*555[ .\-]*0100"]},
                      {"category": "hostname", "literal": ["my-laptop.local"]},
                      {"category": "third-party email address", "any_email": True}],
           "keep_emails": ["noreply@anthropic.com"], "report_only": [{"category": "name", "literal": ["Owner Name"]}]}
    (h / "c.json").write_text(json.dumps(cfg))
    T = PACK / "tools/history"
    s1 = run([sys.executable, str(T / "scan.py"), str(raw), "--config", str(h / "c.json")]).stdout
    check("scan finds an email right after a \\n escape", "third-party email address\n   s.jsonl: 2 line(s), 2 hit(s)" in s1, s1)
    check("scan prints no values", "jane@" not in s1 and "owner@" not in s1)
    r = run([sys.executable, str(T / "redact.py"), str(raw), str(h / "red"), "--config", str(h / "c.json")]).stdout
    s2 = run([sys.executable, str(T / "scan.py"), str(h / "red"), "--config", str(h / "c.json")]).stdout
    check("redacted scan: only report-only hits left", "total hits: 1" in s2, s2)
    red = (h / "red/s.jsonl").read_text().splitlines()
    check("every redacted JSONL line parses", all(json.loads(l) for l in red[:4]))
    check("whole .json file parses after redaction", json.loads((h / "red/sub/m.json").read_text())["by"].startswith("[REDACTED"))

with tempfile.TemporaryDirectory() as d:
    tmp = Path(d)
    for f in (greenfield, brownfield, history):
        try: f(tmp)
        except Exception as e: check(f.__name__ + " ran without error", False, repr(e))
failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
