#!/usr/bin/env python3
"""Create and inspect the docs folder of a Shape Up team. Stdlib only. Never overwrites a file.

The docs folder is chosen at bootstrap and recorded in <repo>/.shapeup.json ({"docs": "shape"}); `shape` when absent.

  scaffold.py init     <repo> [--product NAME] [--docs FOLDER]
  scaffold.py pitch    <repo> <slug> --title "Title" [--why "reason"]
  scaffold.py kickoff  <repo> <slug> --cycle 2026-C1
  scaffold.py add      <repo> <slug> tech|runbook
  scaffold.py log      <repo> <slug> --by Shaper --kind decision|cut|phase|gate|action --entry "..." --why "..."
  scaffold.py status   <repo>
  scaffold.py lint     <repo> <slug>      writing limits: pitch words, scope names, Log sentences, captions, filler
  scaffold.py pack     <out-dir> <name> --layer backend|frontend|database --tech "Django + DRF"   new stack pack plugin
  scaffold.py house    <repo> <role-id> --pack stack-<name>   house rules for one role: <docs>/stack/<role-id>.md
  scaffold.py lint-pack <pack-dir>       required sections, Small/Medium/Large rows, sources, no placeholders
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"
DEFAULT_BUDGET = {"small": 2, "big": 6}   # reviews with the user
DEFAULT_TURN_CAP = 30                     # agent turns per review round
KINDS = ("decision", "cut", "phase", "gate", "action")
TODAY = dt.date.today().isoformat()
CONFIG = ".shapeup.json"


def docs(repo: Path) -> Path:
    """The team's docs folder: from .shapeup.json at the repo root, else `shape`."""
    import json
    cfg = repo / CONFIG
    if cfg.exists():
        folder = json.loads(cfg.read_text()).get("docs", "shape")
    else:
        folder = "shape"
    return repo / folder.strip("/")


def render(name: str, **values: str) -> str:
    text = (TEMPLATES / name).read_text()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_new(path: Path, content: str) -> None:
    if path.exists():
        print(f"exists, kept: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"created: {path}")


def row_after(text: str, heading_cell: str) -> list[str]:
    """Cells of the first data row of the table whose header starts with heading_cell."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| " + heading_cell) and i + 2 < len(lines):
            return [c.strip() for c in lines[i + 2].strip().strip("|").split("|")]
    return []


def folder(repo: Path, slug: str) -> Path:
    d = docs(repo) / "pitches" / slug
    if not (d / "pitch.md").exists():
        sys.exit(f"no pitch: {d / 'pitch.md'}")
    return d


def pitch_meta(d: Path) -> tuple[str, list[str]]:
    text = (d / "pitch.md").read_text()
    return text.splitlines()[0].lstrip("# ").strip(), row_after(text, "Status")


def append_log(d: Path, by: str, kind: str, entry: str, why: str) -> None:
    if kind not in KINDS:
        sys.exit(f"kind must be one of {KINDS}")
    log = d / "log.md"
    text = log.read_text()
    nums = [int(m) for m in re.findall(r"^\| (\d+) \|", text, re.M)]
    clean = lambda s: s.replace("|", "/").replace("\n", " ").strip()
    line = f"| {max(nums, default=0) + 1} | {TODAY} | {clean(by)} | {kind} | {clean(entry)} | {clean(why)} |"
    log.write_text(text.rstrip("\n") + "\n" + line + "\n")
    print(f"logged: {line}")


def setting(repo: Path, key: str, default: int) -> int:
    """A number from team.md › Settings (e.g. `| Pitch word limit | 600 |`), or the default."""
    team = docs(repo) / "team.md"
    if team.exists():
        m = re.search(rf"\|\s*{re.escape(key)}\s*\|\s*(\d+)", team.read_text(), re.I)
        if m:
            return int(m.group(1))
    return default


def budget(repo: Path, appetite: str) -> int:
    size = "big" if "big" in appetite.lower() else "small"
    team = docs(repo) / "team.md"
    if team.exists():
        m = re.search(rf"\|\s*Reviews {size} batch\s*\|\s*(\d+)", team.read_text(), re.I)
        if m:
            return int(m.group(1))
    return DEFAULT_BUDGET[size]


def cmd_init(repo: Path, product: str, folder: str) -> None:
    import json
    folder = folder.strip("/") or "shape"
    cfg = repo / CONFIG
    if cfg.exists() and json.loads(cfg.read_text()).get("docs") != folder:
        sys.exit(f"{cfg} already sets docs to {json.loads(cfg.read_text()).get('docs')!r}; edit it by hand to move the folder")
    if not cfg.exists():
        write_new(cfg, json.dumps({"docs": folder}, indent=2) + "\n")
    shape = repo / folder
    for sub in ("pitches", "betting"):
        (shape / sub).mkdir(parents=True, exist_ok=True)
    write_new(shape / "team.md", render("team.md", product=product))
    write_new(shape / "decisions.md", render("decisions.md"))
    write_new(shape / "ideas.md", render("ideas.md"))


def cmd_pitch(repo: Path, slug: str, title: str, why: str) -> None:
    d = docs(repo) / "pitches" / slug
    write_new(d / "pitch.md", render("pitch.md", title=title, date=TODAY))
    write_new(d / "log.md", render("log.md", title=title, date=TODAY, why=why))


def cmd_kickoff(repo: Path, slug: str, cycle: str) -> None:
    d = folder(repo, slug)
    title, row = pitch_meta(d)
    if not row or row[0] != "bet":
        sys.exit(f"pitch status is '{row[0] if row else '?'}'; kickoff needs 'bet' (set it only after the betting table bets)")
    appetite = row[1]
    if "<" in appetite:
        sys.exit("pitch has no appetite set")
    reviews = budget(repo, appetite)
    cap = setting(repo, "Turn cap per round", DEFAULT_TURN_CAP)
    branch = "cycle/{cycle}-{slug}"
    team = docs(repo) / "team.md"
    if team.exists():
        m = re.search(r"\|\s*Branch pattern\s*\|\s*([^|<]+?)\s*\|", team.read_text())
        if m:
            branch = m.group(1).strip("` ")
    branch = branch.replace("<cycle>", cycle).replace("<slug>", slug).replace("{cycle}", cycle).replace("{slug}", slug)
    write_new(d / "board.md", render("board.md", title=title, slug=slug, cycle=cycle, branch=branch,
                                     appetite=appetite, budget=str(reviews), cap=str(cap)))
    pitch = (d / "pitch.md").read_text()
    old = "| " + " | ".join(row) + " |"
    new = "| " + " | ".join(["building", row[1], row[2], cycle, TODAY]) + " |"
    (d / "pitch.md").write_text(pitch.replace(old, new, 1))
    append_log(d, "Conductor", "phase", f"Kickoff: cycle {cycle}, status building, budget {reviews} reviews, {cap} turns per round",
               f"The betting table bet on it; {appetite} budget from team.md")


def cmd_add(repo: Path, slug: str, doc: str) -> None:
    d = folder(repo, slug)
    title, row = pitch_meta(d)
    cycle = row[3] if len(row) > 3 else "—"
    write_new(d / f"{doc}.md", render(f"{doc}.md", title=title, slug=slug, cycle=cycle))


def cmd_status(repo: Path) -> None:
    print("| Pitch | Status | Appetite | Cycle | Reviews | Board status | Log entries |")
    print("|---|---|---|---|---|---|---|")
    for p in sorted((docs(repo) / "pitches").glob("*/pitch.md")):
        d = p.parent
        row = row_after(p.read_text(), "Status") + ["?"] * 5
        rounds = bstatus = "—"
        if (d / "board.md").exists():
            b = row_after((d / "board.md").read_text(), "Cycle")
            if len(b) >= 8:
                rounds, bstatus = b[4], b[7]
            elif len(b) >= 6:
                rounds, bstatus = b[4], b[5]
        n = len(re.findall(r"^\| \d+ \|", (d / "log.md").read_text(), re.M)) if (d / "log.md").exists() else 0
        print(f"| {d.name} | {row[0]} | {row[1]} | {row[3]} | {rounds} | {bstatus} | {n} |")


RESIDUE = ("with or without", "as on the web", "regardless of", "in all cases", "as usual", "in any case", "as before")
BANNED = ("see above", "as discussed", "as mentioned", "as stated", "it is worth noting", "in order to", "basically", "please note")


def table_rows(text: str, header_start: str) -> list[list[str]]:
    rows, on = [], False
    for line in text.splitlines():
        if line.startswith("| " + header_start):
            on = True
            continue
        if on:
            if not line.startswith("|"):
                break
            if not line.startswith("|---"):
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def sentences(s: str) -> int:
    s = re.sub(r"`[^`]*`", "x", s.split("Options:")[0])
    return len([p for p in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", s.strip()) if p])


def cmd_lint(repo: Path, slug: str) -> None:
    d = folder(repo, slug)
    issues = []
    pitch = (d / "pitch.md").read_text()
    words = len(re.sub(r"```.*?```", "", pitch, flags=re.S).split())
    limit = setting(repo, "Pitch word limit", 600)
    if words > limit:
        issues.append(("pitch.md", f"{words} words outside code blocks (max {limit}, team.md › Pitch word limit)"))
    problem = re.search(r"^## Problem\n(.*?)(?=^## )", pitch, re.S | re.M)
    if problem:
        lines = [l for l in problem.group(1).splitlines() if l.strip()]
        if len(lines) > 5:
            issues.append(("pitch.md", f"Problem has {len(lines)} lines (max 5: baseline, workaround, cost)"))
    appetite = re.search(r"^## Appetite\n(.*?)(?=^## )", pitch, re.S | re.M)
    if appetite:
        body = [l for l in appetite.group(1).splitlines() if l.strip()]
        if len(body) > 1:
            issues.append(("pitch.md", "Appetite: one imperative sentence on what the bet builds"))
        if re.search(r"\b(batch|rounds?|reviews?)\b", appetite.group(1), re.I):
            issues.append(("pitch.md", "Appetite repeats the size; it lives in the header table"))
    prose = re.sub(r"```.*?```", "", pitch, flags=re.S)
    for i, line in enumerate(prose.splitlines(), 1):
        if re.search(r"(^|[.:|]\s+)We\s", line):
            issues.append(("pitch.md", f"'We …': start with the verb (writing-style › sentence edit, cut 2): {line.strip()[:60]}"))
        hedge = re.search(r"\b(should|might|could|ideally|potentially|hopefully)\b", line, re.I)
        if hedge:
            issues.append(("pitch.md", f"hedge '{hedge.group(1)}': use an imperative, must or can: {line.strip()[:60]}"))
    if re.search(r"^## Tech check", pitch, re.M):
        issues.append(("pitch.md", "'Tech check' section: move its risks to Rabbit holes and the check to log.md"))
    for other in (docs(repo) / "pitches").glob("*/pitch.md"):
        if other.parent == d:
            continue
        title = other.read_text().splitlines()[0].lstrip("# ").strip()
        if title and title.lower() in pitch.lower() or re.search(r"\b(the|other|previous|next) [\w-]+ pitch\b", pitch, re.I):
            issues.append(("pitch.md", f"names another pitch ('{title}'); dependencies go in the betting pack and log.md"))
    for i, line in enumerate(pitch.splitlines(), 1):
        if re.search(r"\b(TBD|TODO)\b|\bneeded:", line):
            issues.append(("pitch.md", f"line {i}: meta-note in the pitch; move it to your reply and log.md"))
    if (d / "board.md").exists():
        board = (d / "board.md").read_text()
        for r in table_rows(board, "ID"):
            name = re.sub(r"\*", "", r[1]) if len(r) > 1 else ""
            if len(name.split()) > 5:
                issues.append(("board.md Scopes", f"{r[0]} name has {len(name.split())} words (max 5)"))
        for r in table_rows(board, "# | Rnd"):
            if len(r) > 5 and sentences(r[5]) > 3:
                issues.append(("board.md Log", f"#{r[0]} has {sentences(r[5])} sentences (max 3, Options excluded)"))
    if (d / "log.md").exists():
        for r in table_rows((d / "log.md").read_text(), "# | Date"):
            if len(r) > 5 and not r[5]:
                issues.append(("log.md", f"#{r[0]} has no why"))
    if (d / "tech.md").exists():
        lines = (d / "tech.md").read_text().splitlines()
        for i, line in enumerate(lines):
            if line.startswith("```mermaid"):
                body = "\n".join(lines[i + 1:i + 3]).strip()
                prev = next((l for l in reversed(lines[:i]) if l.strip()), "")
                if body.split("\n")[0].strip() in ("erDiagram", "classDiagram", "sequenceDiagram", "flowchart TD") and lines[i + 2].startswith("```"):
                    issues.append(("tech.md", f"line {i + 1}: empty diagram; delete the section if it doesn't apply"))
                elif prev.startswith("#") or prev.startswith("<"):
                    issues.append(("tech.md", f"line {i + 1}: diagram has no caption line above it"))
    for f in d.glob("*.md"):
        low = f.read_text().lower()
        issues += [(f.name, f"contains '{b}'") for b in BANNED if b in low]
    for f in [d / n for n in ("pitch.md", "tech.md", "runbook.md") if (d / n).exists()]:
        low = f.read_text().lower()
        issues += [(f.name, f"conversation residue '{r}': delete it if the general statement already covers it") for r in RESIDUE if r in low]
    if not issues:
        print("lint: clean")
        return
    print("| File | Issue |\n|---|---|")
    for f, msg in issues:
        print(f"| {f} | {msg} |")
    sys.exit(1)


AGENT_FOR_LAYER = {"backend": "backend-dev", "frontend": "frontend-dev", "database": "dba"}
PACK_SECTIONS = ("Layering", "Rules", "Tests per size", "Performance", "Review checklist", "Sources")
DB_PACK_SECTIONS = ("Commands", "Migration review", "Rules", "Tests per size", "Performance", "Review checklist", "Sources")
PACK_MAX_LINES = 220


def cmd_pack(out: Path, name: str, layer: str, tech: str) -> None:
    name = name.removeprefix("stack-")
    root = out / f"stack-{name}"
    agent = AGENT_FOR_LAYER[layer]
    write_new(root / ".claude-plugin" / "plugin.json",
              '{\n  "name": "stack-%s",\n  "version": "0.1.0",\n  "description": "Stack pack for the shapeup-team plugin: %s.",\n'
              '  "keywords": ["shapeup-team", "stack-pack", "%s"]\n}\n' % (name, tech, layer))
    write_new(root / "skills" / f"stack-{name}" / "SKILL.md",
              render("stack-pack.md", slug=name, tech=tech, layer=layer, agent=agent,
                     summary=f"{tech} rules for the {layer} layer"))
    write_new(root / "skills" / f"stack-{name}" / "references" / "sources.md",
              f"# Sources: {tech}\n\nOfficial docs first. Where a source conflicts with this pack's SKILL.md, the pack wins: it is the house style.\n\n"
              "## <Area>\n\n| Source | URL | Use it for |\n|---|---|---|\n| <page> | <https://…> | <what to look up there> |\n")


def cmd_house(repo: Path, role: str, pack: str) -> None:
    write_new(docs(repo) / "stack" / f"{role}.md", render("house-rules.md", role=role, pack=pack))


def cmd_lint_pack(root: Path) -> None:
    skills = sorted((root / "skills").glob("stack-*/SKILL.md"))
    if not skills:
        sys.exit(f"lint-pack: no skills/stack-*/SKILL.md under {root}")
    problems = []
    for skill in skills:
        text = skill.read_text()
        name = skill.parent.name
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        meta = fm.group(1) if fm else ""
        if not re.search(rf"^name:\s*{re.escape(name)}\s*$", meta, re.M):
            problems.append(f"{name}: frontmatter name must be {name}")
        desc = re.search(r"^description:\s*(.+)$", meta, re.M)
        if not desc or "<" in desc.group(1) or len(desc.group(1)) > 1024:
            problems.append(f"{name}: description missing, over 1024 chars, or has angle brackets")
        headings = re.findall(r"^## (.+)$", text, re.M)
        is_db = re.search(r"^\|\s*database\s*\|", text, re.M)
        for section in (DB_PACK_SECTIONS if is_db else PACK_SECTIONS):
            if not any(h.startswith(section) for h in headings):
                problems.append(f"{name}: missing section '## {section}'")
        tests = text.split("## Tests per size", 1)[-1].split("\n## ", 1)[0]
        for size in ("Small", "Medium", "Large"):
            if not re.search(rf"^\|\s*{size}\s*\|", tests, re.M):
                problems.append(f"{name}: Tests per size has no {size} row")
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for cell in re.findall(r"\|\s*(<[^>|]+>)\s*\|", prose):
            problems.append(f"{name}: placeholder left: {cell}")
        lines = text.count("\n")
        if lines > PACK_MAX_LINES:
            problems.append(f"{name}: {lines} lines; keep a pack under {PACK_MAX_LINES} (move detail to references/)")
        sources = skill.parent / "references" / "sources.md"
        urls = re.findall(r"https?://[^\s|)>]+", sources.read_text()) if sources.exists() else []
        if len(urls) < 5:
            problems.append(f"{name}: references/sources.md needs at least 5 source URLs (has {len(urls)})")
    print("\n".join(problems) if problems else "lint-pack: clean")
    sys.exit(1 if problems else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("repo"); s.add_argument("--product", default="<product>"); s.add_argument("--docs", default="shape")
    s = sub.add_parser("pitch"); s.add_argument("repo"); s.add_argument("slug")
    s.add_argument("--title", required=True); s.add_argument("--why", default="Raw idea brought to shaping")
    s = sub.add_parser("kickoff"); s.add_argument("repo"); s.add_argument("slug"); s.add_argument("--cycle", required=True)
    s = sub.add_parser("add"); s.add_argument("repo"); s.add_argument("slug"); s.add_argument("doc", choices=["tech", "runbook"])
    s = sub.add_parser("log"); s.add_argument("repo"); s.add_argument("slug")
    s.add_argument("--by", required=True); s.add_argument("--kind", required=True, choices=KINDS)
    s.add_argument("--entry", required=True); s.add_argument("--why", required=True)
    s = sub.add_parser("status"); s.add_argument("repo")
    s = sub.add_parser("lint"); s.add_argument("repo"); s.add_argument("slug")
    s = sub.add_parser("pack"); s.add_argument("repo", metavar="out_dir"); s.add_argument("name")
    s.add_argument("--layer", required=True, choices=sorted(AGENT_FOR_LAYER)); s.add_argument("--tech", required=True)
    s = sub.add_parser("house"); s.add_argument("repo"); s.add_argument("role"); s.add_argument("--pack", required=True)
    s = sub.add_parser("lint-pack"); s.add_argument("repo", metavar="pack_dir")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    if a.cmd == "init":
        cmd_init(repo, a.product, a.docs)
    elif a.cmd == "pitch":
        cmd_pitch(repo, a.slug, a.title, a.why)
    elif a.cmd == "kickoff":
        cmd_kickoff(repo, a.slug, a.cycle)
    elif a.cmd == "add":
        cmd_add(repo, a.slug, a.doc)
    elif a.cmd == "log":
        append_log(folder(repo, a.slug), a.by, a.kind, a.entry, a.why)
    elif a.cmd == "lint":
        cmd_lint(repo, a.slug)
    elif a.cmd == "pack":
        cmd_pack(repo, a.name, a.layer, a.tech)
    elif a.cmd == "house":
        cmd_house(repo, a.role, a.pack)
    elif a.cmd == "lint-pack":
        cmd_lint_pack(repo)
    else:
        cmd_status(repo)


if __name__ == "__main__":
    main()
