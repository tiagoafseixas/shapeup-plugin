#!/usr/bin/env python3
"""PreToolUse guard for the shapeup-team plugin.

Enforces the team's file, git and production rules on Write/Edit/Bash calls.
Active only inside a repo bootstrapped by the team (.shapeup.json, or a shape/team.md), or when the caller is one of the team's agents.
Deny: exit 2 with the reason on stderr. Ask the human: permissionDecision "ask". Otherwise: exit 0, no output.
"""
import json
import os
import re
import sys
from fnmatch import fnmatch

AGENT_ROLES = {"product-owner": "po", "qa-engineer": "qa", "backend-dev": "backend", "frontend-dev": "frontend", "dba": "dba"}
LAYER_OF_AGENT = {"backend-dev": "backend", "frontend-dev": "frontend", "dba": "database"}
MIGRATION_DIRS = ("/migrations/", "/migrate/", "/alembic/versions/", "/db/migrations/")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "db", "postgres", "mysql", "mongo", "host.docker.internal"}
PITCH_DOCS = ("board.md", "log.md")


def deny(reason):
    sys.stderr.write(f"shapeup-team guard: {reason}\n")
    sys.exit(2)


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": f"shapeup-team guard: {reason}",
    }}))
    sys.exit(0)


def docs_folder(repo):
    """The docs folder chosen at bootstrap (.shapeup.json), relative to the repo root; `shape` when absent."""
    try:
        with open(os.path.join(repo, ".shapeup.json"), encoding="utf-8") as fh:
            return json.load(fh).get("docs", "shape").strip("/") or "shape"
    except (OSError, ValueError):
        return "shape"


def find_repo(start):
    d = os.path.abspath(start)
    if os.path.isfile(d):
        d = os.path.dirname(d)
    while True:
        if os.path.isfile(os.path.join(d, ".shapeup.json")) or os.path.isfile(os.path.join(d, "shape", "team.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def clean_path(repo, cell):
    value = cell.split(",")[0].split()[0].strip("`") if cell.strip() else ""
    if not value or value in ("—", "-") or value.startswith("<"):
        return None
    return os.path.normpath(os.path.join(repo, value))


def team_paths(repo):
    """Paths per layer from team.md › Roles (Role id | Agent | Stack pack | Path), resolved against the repo root.
    Also reads the older single-row keys `Backend path` / `Frontend path`."""
    paths = {"backend": [], "frontend": [], "database": []}
    try:
        lines = open(os.path.join(repo, docs_folder(repo), "team.md"), encoding="utf-8").read().splitlines()
    except OSError:
        return paths
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[1].strip("`") in LAYER_OF_AGENT:
            path = clean_path(repo, cells[3])
            if path:
                paths[LAYER_OF_AGENT[cells[1].strip("`")]].append(path)
        m = re.match(r"\|\s*(Backend|Frontend) path\s*\|\s*([^|<]+?)\s*\|", line)
        if m:
            path = clean_path(repo, m.group(2))
            if path:
                paths[m.group(1).lower()].append(path)
    return paths


def role_of(event):
    raw = event.get("agent_type") or event.get("subagent_type") or ""
    raw = raw.split(":")[-1].strip().lower()
    return AGENT_ROLES.get(raw)


def is_test_file(rel):
    parts = rel.split("/")
    name = parts[-1]
    if any(p in ("tests", "test", "e2e", "cypress", "__tests__") for p in parts[:-1]):
        return True
    return (fnmatch(name, "test_*.py") or fnmatch(name, "*_test.py") or name == "conftest.py"
            or fnmatch(name, "*.test.*") or fnmatch(name, "*.spec.*") or fnmatch(name, "cypress.config.*"))


def pitch_doc(rel, names, docs="shape"):
    prefix = docs.split("/") + ["pitches"]
    parts = rel.split("/")
    return len(parts) == len(prefix) + 2 and parts[:len(prefix)] == prefix and parts[-1] in names


def inside(path, root):
    return bool(root) and (path == root or path.startswith(root + os.sep))


def inside_any(path, roots):
    return next((r for r in roots if inside(path, r)), None)


def check_file(event, role):
    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or tool_input.get("path")
    if not path:
        return
    path = os.path.abspath(os.path.join(event.get("cwd") or os.getcwd(), path))
    name = os.path.basename(path)
    repo = find_repo(path) or find_repo(event.get("cwd") or os.getcwd())
    if repo is None and role is None:
        return
    if name.startswith(".env"):
        deny(f"{name} is off-limits: secrets and env files are the user's (SKILL.md › Git rules).")
    if role is None or repo is None:
        return

    paths = team_paths(repo)
    rel = os.path.relpath(path, repo).replace(os.sep, "/")
    shape_docs = {
        "backend": PITCH_DOCS + ("tech.md",),
        "frontend": PITCH_DOCS + ("tech.md",),
        "qa": PITCH_DOCS,
        "dba": PITCH_DOCS + ("tech.md", "runbook.md"),
    }
    docs = docs_folder(repo)
    if rel.startswith(docs + "/"):
        ok = rel != f"{docs}/team.md" if role == "po" else pitch_doc(rel, shape_docs[role], docs)
    elif rel == ".shapeup.json":
        ok = False
    elif role == "po":
        ok = False
    elif role in ("backend", "frontend"):
        ok = inside_any(path, paths[role]) is not None
    elif role == "qa":
        root = inside_any(path, paths["backend"] + paths["frontend"] + [repo])
        ok = bool(root) and is_test_file(os.path.relpath(path, root).replace(os.sep, "/"))
    elif role == "dba":
        in_code = not rel.startswith("..") or inside_any(path, paths["backend"]) is not None
        ok = in_code and any(d in path.replace(os.sep, "/") for d in MIGRATION_DIRS)
    else:
        ok = True
    if not ok:
        who = {"po": "the PO", "qa": "QA", "dba": "the DBA"}.get(role, f"a {role} role")
        deny(f"{who} may not edit {rel}: it's outside the role's area in team.md › Roles. Write a row on the board for the owner instead.")


GIT_DENY = [
    (r"\bgit\s+push\b[^;&|]*(\s--force\b|\s-f\b|\s--force-with-lease\b|\s\+\S)", "force-push is never allowed"),
    (r"\bgit\s+push\b[^;&|]*\s(\S+:)?(refs/heads/)?(main|master|develop|production|prod)\b(?!-)", "push to the base branch is never allowed"),
    (r"\bgit\s+(merge|rebase)(?![-\w])(?![^;&|]*--(abort|continue|quit))", "merge and rebase are the user's"),
    (r"\bgh\s+pr\s+merge\b", "only the user merges"),
    (r"\bgit\s+commit\b[^;&|]*--no-verify", "commits keep their hooks (--no-verify)"),
]
DEPLOY_DENY = [
    (r"\bgcloud\s+(app|run|functions)\s+(deploy|services\s+update|update)\b", "deploys are the user's"),
    (r"\bgcloud\s+builds\s+submit\b", "deploys are the user's"),
    (r"(^|[\s/;&|])deploy\.sh\b", "deploys are the user's"),
    (r"\bterraform\s+(apply|destroy|import)\b", "infrastructure changes are the user's"),
    (r"\bkubectl\s+(apply|delete|edit|patch|scale|rollout)\b", "infrastructure changes are the user's"),
]
SQL_READ = r"\bgcloud\s+sql\s+(backups\s+(list|describe)|instances\s+(list|describe)|operations\s+(list|describe|wait)|databases\s+(list|describe)|users\s+list|flags\s+list|tiers\s+list)\b"


NO_PROD_ROLES = ("po", "qa", "frontend")


def prod_connection(role, what):
    """Production is off by default: only the backend role and the DBA may connect, and only after the user approves."""
    if role in NO_PROD_ROLES:
        deny(f"{what}: this role has no production access. ASK the backend role or the DBA, who ask the user.")
    ask(f"{what}. Approve only if you chose to let the agent connect read-only for this one question "
        "(otherwise answer with the numbers or run the query yourself).")


OFFLINE_ASK = [
    (r"(^|[\s;&|(])gh\s", "a GitHub request"),
    (r"\bgit\s+(push|fetch|pull|clone|ls-remote|remote\s+update|submodule\s+update)\b", "a call to the git remote"),
    (r"\b(pip3?\s+install|uv\s+(pip\s+install|sync|add)|poetry\s+(install|add)|npm\s+(install|i|ci|add)\b|yarn(\s+(add|install))?\s*($|[;&|])|pnpm\s+(add|install|i)\b|brew\s+install|apt(-get)?\s+install)", "a package install"),
    (r"\b(psql|pg_dump|pg_restore|mysql|mysqldump|mongosh|mongodump|redis-cli|cloud[-_]sql[-_]proxy)\b", "a database connection"),
    (r"\bmanage\.py\s+(migrate|test|dbshell|shell|runserver|loaddata|flush|createsuperuser|showmigrations)\b", "a database connection (manage.py)"),
    (r"\b(pytest|jest|vitest|cypress|playwright)\b|\b(npm|yarn|pnpm)\s+(run\s+)?(test|e2e|dev|start)\b", "a test run or a server"),
    (r"\bdocker(\s+compose|-compose)?\s+(up|run|start|exec|pull|build)\b", "a container"),
    (r"\b(curl|wget)\s", "a network request"),
]


def cycle_started(repo):
    pitches = os.path.join(repo, docs_folder(repo), "pitches")
    try:
        return any(os.path.isfile(os.path.join(pitches, d, "board.md")) for d in os.listdir(pitches))
    except OSError:
        return False


def check_offline(cmd, repo):
    """Before the first kickoff (no pitch has a board), setup and shaping stay offline: ask before anything external."""
    for pattern, what in OFFLINE_ASK:
        if re.search(pattern, cmd):
            ask(f"no cycle has started, so setup and shaping stay offline (SKILL.md › Offline until kickoff). "
                f"This is {what}. Approve only if you want it now.")


def check_bash(event, role):
    cmd = (event.get("tool_input") or {}).get("command") or ""
    repo = find_repo(event.get("cwd") or os.getcwd())
    if repo is None and role is None:
        return

    for pattern, reason in GIT_DENY + DEPLOY_DENY:
        if re.search(pattern, cmd):
            deny(f"{reason}. Write it as a HUMAN row or a runbook step.")

    offline = repo is not None and not cycle_started(repo)
    if re.search(r"(>{1,2}|\btee\b[^|;&]*|\bsed\s+-i[^;&|]*|\bcp\b[^;&|]*|\bmv\b[^;&|]*)\s*\S*\.env\b", cmd):
        deny("env files are the user's; never write credentials.")

    if re.search(r"\bgcloud\s+sql\b", cmd):
        if re.search(r"\bgcloud\s+sql\s+backups\s+create\b", cmd):
            if role not in (None, "dba"):
                deny("only the DBA takes production backups.")
            ask("production backup. Approve only if the DBA's HUMAN row named this exact command, instance and reason.")
        if not re.search(SQL_READ, cmd):
            deny("the only production write allowed is an on-demand backup by the DBA (SKILL.md › Production access).")
        prod_connection(role, "gcloud sql reads production metadata")

    if re.search(r"\baws\s+rds\b", cmd):
        if re.search(r"\baws\s+rds\s+create-db-(cluster-)?snapshot\b", cmd):
            if role not in (None, "dba"):
                deny("only the DBA takes production backups.")
            ask("production snapshot. Approve only if the DBA's HUMAN row named this exact command, instance and reason.")
        if not re.search(r"\baws\s+rds\s+(describe|list)-", cmd):
            deny("the only production write allowed is an on-demand backup by the DBA (SKILL.md › Production access).")
        prod_connection(role, "aws rds reads production metadata")

    if re.search(r"\bcloud[-_]sql[-_]proxy\b", cmd):
        prod_connection(role, "Cloud SQL proxy opens a production connection")

    if re.search(r"\$\{?(?!READONLY_)[A-Z0-9_]*DATABASE_URL\b", cmd) or re.search(r"\b(PGPASSWORD|MYSQL_PWD)=", cmd):
        deny("only READONLY_DATABASE_URL may be used against a shared database.")

    for host in re.findall(r"(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?)(?:\+\w+)?://[^@\s'\"]*@\[?([^:/\s'\"\]]+)", cmd):
        if host.lower() not in LOCAL_HOSTS:
            deny(f"connection string to {host}: use READONLY_DATABASE_URL from the environment, never a literal URL.")

    if re.search(r"\$\{?READONLY_DATABASE_URL\b", cmd):
        prod_connection(role, "this command connects to production with READONLY_DATABASE_URL")

    for host in re.findall(r"\b(?:psql|pg_dump|pg_dumpall|mysql|mysqldump|mongosh|mongodump)\b[^;&|]*?(?:-h\s*|--host[= ])([^\s'\"]+)", cmd):
        if host.lower() not in LOCAL_HOSTS:
            prod_connection(role, f"this command connects to the database host {host}")

    if re.search(r"(--settings[= ]\S*(prod|prd|production)|DJANGO_SETTINGS_MODULE=\S*(prod|prd|production)|RAILS_ENV=production)", cmd, re.I):
        deny("commands against production settings are the user's (runbook step).")

    if offline:
        check_offline(cmd, repo)


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        sys.exit(0)
    role = role_of(event)
    tool = event.get("tool_name", "")
    if tool == "Bash":
        check_bash(event, role)
    elif tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        check_file(event, role)
    sys.exit(0)


if __name__ == "__main__":
    main()
