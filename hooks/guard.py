#!/usr/bin/env python3
"""PreToolUse guard for the shapeup-team plugin.

Enforces the team's file, git and production rules on Write/Edit/Bash calls.
Active only inside a repo that has shape/team.md, or when the caller is one of the team's agents.
Deny: exit 2 with the reason on stderr. Ask the human: permissionDecision "ask". Otherwise: exit 0, no output.
"""
import json
import os
import re
import sys
from fnmatch import fnmatch

ROLES = {"po", "backend-drf", "frontend-react", "qa", "dba"}
AGENT_ROLES = {"product-owner": "po", "qa-engineer": "qa", "backend-drf": "backend-drf", "frontend-react": "frontend-react", "dba": "dba"}
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "db", "postgres", "host.docker.internal"}
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


def find_repo(start):
    d = os.path.abspath(start)
    if os.path.isfile(d):
        d = os.path.dirname(d)
    while True:
        if os.path.isfile(os.path.join(d, "shape", "team.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def team_paths(repo):
    """Backend and frontend paths from team.md, resolved against the repo root."""
    paths = {}
    try:
        for line in open(os.path.join(repo, "shape", "team.md"), encoding="utf-8"):
            m = re.match(r"\|\s*(Backend|Frontend) path\s*\|\s*([^|<]+?)\s*\|", line)
            if m:
                value = m.group(2).split(",")[0].split()[0].strip("`")
                paths[m.group(1).lower()] = os.path.normpath(os.path.join(repo, value))
    except OSError:
        pass
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


def pitch_doc(rel, names):
    parts = rel.split("/")
    return len(parts) == 4 and parts[:2] == ["shape", "pitches"] and parts[3] in names


def inside(path, root):
    return root and (path == root or path.startswith(root + os.sep))


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
    backend, frontend = paths.get("backend"), paths.get("frontend")

    shape_docs = {
        "backend-drf": PITCH_DOCS + ("tech.md",),
        "frontend-react": PITCH_DOCS + ("tech.md",),
        "qa": PITCH_DOCS,
        "dba": PITCH_DOCS + ("tech.md", "runbook.md"),
    }
    if rel.startswith("shape/"):
        ok = rel != "shape/team.md" if role == "po" else pitch_doc(rel, shape_docs[role])
    elif role == "po":
        ok = False
    elif role == "backend-drf":
        ok = inside(path, backend)
    elif role == "frontend-react":
        ok = inside(path, frontend)
    elif role == "qa":
        root = next((r for r in (backend, frontend, repo) if inside(path, r)), None)
        ok = bool(root) and is_test_file(os.path.relpath(path, root).replace(os.sep, "/"))
    elif role == "dba":
        ok = "/migrations/" in "/" + rel and name.endswith(".py")
    else:
        ok = True
    if not ok:
        deny(f"{role} may not edit {rel}. Write a row on the board for the owner instead (roles/{role}.md).")


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


def check_bash(event, role):
    cmd = (event.get("tool_input") or {}).get("command") or ""
    repo = find_repo(event.get("cwd") or os.getcwd())
    if repo is None and role is None:
        return

    for pattern, reason in GIT_DENY + DEPLOY_DENY:
        if re.search(pattern, cmd):
            deny(f"{reason}. Write it as a HUMAN row or a runbook step.")

    if re.search(r"(>{1,2}|\btee\b[^|;&]*|\bsed\s+-i[^;&|]*|\bcp\b[^;&|]*|\bmv\b[^;&|]*)\s*\S*\.env\b", cmd):
        deny("env files are the user's; never write credentials.")

    if re.search(r"\bgcloud\s+sql\b", cmd):
        if re.search(r"\bgcloud\s+sql\s+backups\s+create\b", cmd):
            if role not in (None, "dba"):
                deny("only the DBA takes production backups.")
            ask("production backup. Approve only if the DBA's HUMAN row named this exact command, instance and reason.")
        if not re.search(SQL_READ, cmd):
            deny("the only production write allowed is an on-demand backup by the DBA (SKILL.md › Production access).")

    if re.search(r"\bcloud[-_]sql[-_]proxy\b", cmd):
        ask("Cloud SQL proxy opens a production connection. Approve only for the read-only user.")

    if re.search(r"\$\{?(?!READONLY_)[A-Z0-9_]*DATABASE_URL\b", cmd) or re.search(r"\bPGPASSWORD=", cmd):
        deny("only READONLY_DATABASE_URL may be used against a shared database.")

    for host in re.findall(r"postgres(?:ql)?(?:\+\w+)?://[^@\s'\"]*@\[?([^:/\s'\"\]]+)", cmd):
        if host.lower() not in LOCAL_HOSTS:
            deny(f"connection string to {host}: use READONLY_DATABASE_URL from the environment, never a literal URL.")

    if re.search(r"(--settings[= ]\S*(prod|prd|production)|DJANGO_SETTINGS_MODULE=\S*(prod|prd|production))", cmd, re.I):
        deny("Django commands against production settings are the user's (runbook step).")


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
