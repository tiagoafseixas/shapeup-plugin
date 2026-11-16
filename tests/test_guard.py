"""Behaviour of the PreToolUse guard: what each role may edit and which commands are blocked or need the user."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

GUARD = Path(__file__).resolve().parents[1] / "plugins" / "shapeup-team" / "hooks" / "guard.py"


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "app"
    (root / "shape" / "pitches" / "win").mkdir(parents=True)
    (root / "shape" / "team.md").write_text(
        "## Roles\n\n| Role id | Agent | Stack pack | Path |\n|---|---|---|---|\n"
        "| backend-drf | backend-dev | stack-django-drf | backend/ |\n"
        "| frontend-react | frontend-dev | stack-react-mui | ../web (separate repo) |\n"
        "| database | dba | stack-postgres-cloudsql | — |\n"
    )
    (root / "backend" / "deals" / "migrations").mkdir(parents=True)
    (root / "backend" / "deals" / "tests").mkdir()
    (tmp_path / "web" / "src").mkdir(parents=True)
    (root / "shape" / "pitches" / "win" / "board.md").write_text("# Board\n")  # a cycle has started
    return root


def run(repo, tool, tool_input, agent=""):
    event = {"tool_name": tool, "agent_type": agent, "cwd": str(repo), "tool_input": tool_input}
    result = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(event), capture_output=True, text=True)
    if result.returncode == 2:
        return "deny"
    if '"ask"' in result.stdout:
        return "ask"
    return "allow"


def edit(repo, agent, relpath):
    return run(repo, "Edit", {"file_path": str((repo / relpath).resolve())}, agent)


def bash(repo, command, agent=""):
    return run(repo, "Bash", {"command": command}, agent)


def test_backend_dev_edits_backend_code_and_tech_doc(repo):
    assert edit(repo, "shapeup-team:backend-dev", "backend/deals/services.py") == "allow"
    assert edit(repo, "shapeup-team:backend-dev", "shape/pitches/win/tech.md") == "allow"


def test_backend_dev_cannot_edit_pitch_or_frontend(repo):
    assert edit(repo, "shapeup-team:backend-dev", "shape/pitches/win/pitch.md") == "deny"
    assert edit(repo, "shapeup-team:backend-dev", "../web/src/page.js") == "deny"


def test_frontend_dev_edits_the_separate_web_repo(repo):
    assert edit(repo, "shapeup-team:frontend-dev", "../web/src/page.js") == "allow"


def test_qa_edits_tests_and_board_only(repo):
    assert edit(repo, "shapeup-team:qa-engineer", "backend/deals/tests/test_win.py") == "allow"
    assert edit(repo, "shapeup-team:qa-engineer", "shape/pitches/win/board.md") == "allow"
    assert edit(repo, "shapeup-team:qa-engineer", "backend/deals/services.py") == "deny"


def test_dba_edits_migrations_and_runbook_only(repo):
    assert edit(repo, "shapeup-team:dba", "backend/deals/migrations/0008_x.py") == "allow"
    assert edit(repo, "shapeup-team:dba", "shape/pitches/win/runbook.md") == "allow"
    assert edit(repo, "shapeup-team:dba", "backend/deals/models.py") == "deny"


def test_po_edits_shape_docs_but_not_team_config_or_code(repo):
    assert edit(repo, "shapeup-team:product-owner", "shape/pitches/win/pitch.md") == "allow"
    assert edit(repo, "shapeup-team:product-owner", "shape/team.md") == "deny"
    assert edit(repo, "shapeup-team:product-owner", "backend/deals/models.py") == "deny"


def test_main_session_has_no_file_limits_except_env_files(repo):
    assert edit(repo, "", "backend/deals/models.py") == "allow"
    assert edit(repo, "", "backend/.env") == "deny"


def test_pushing_the_cycle_branch_is_allowed(repo):
    assert bash(repo, "git push origin cycle/2026-C1-win", "shapeup-team:backend-dev") == "allow"


def test_force_push_push_to_main_and_merge_are_blocked(repo):
    assert bash(repo, "git push --force origin cycle/2026-C1-win") == "deny"
    assert bash(repo, "git push origin HEAD:main") == "deny"
    assert bash(repo, "git merge main") == "deny"
    assert bash(repo, "gh pr merge 412") == "deny"


def test_read_only_git_commands_pass(repo):
    assert bash(repo, "git merge-base main HEAD") == "allow"


def test_deploys_are_blocked(repo):
    assert bash(repo, "gcloud app deploy app_prd.yaml") == "deny"
    assert bash(repo, "./deploy.sh prd") == "deny"


def test_dba_backup_asks_the_cto(repo):
    assert bash(repo, "gcloud sql backups create --instance=pg", "shapeup-team:dba") == "ask"


def test_other_roles_cannot_take_backups(repo):
    assert bash(repo, "gcloud sql backups create --instance=pg", "shapeup-team:backend-dev") == "deny"


def test_cloud_sql_writes_other_than_backups_are_blocked(repo):
    assert bash(repo, "gcloud sql instances patch pg --tier=db-custom-4", "shapeup-team:dba") == "deny"
    assert bash(repo, "gcloud sql backups list --instance=pg", "shapeup-team:dba") == "ask"


def test_only_the_read_only_database_url_is_usable_and_it_asks_first(repo):
    assert bash(repo, 'psql "$READONLY_DATABASE_URL" -c "select 1"') == "ask"
    assert bash(repo, 'psql "$DATABASE_URL" -c "select 1"') == "deny"
    assert bash(repo, "psql postgres://admin:pw@10.0.0.5:5432/app") == "deny"
    assert bash(repo, "psql postgres://u:p@localhost:5432/test") == "allow"


def test_env_writes_and_production_settings_are_blocked(repo):
    assert bash(repo, "echo SECRET=1 >> backend/.env") == "deny"
    assert bash(repo, "python manage.py migrate --settings=config.settings_prod") == "deny"


def test_guard_is_inactive_outside_shape_repos(tmp_path):
    assert bash(tmp_path, "git push --force origin main") == "allow"


def test_a_second_backend_role_gets_its_own_path(repo):
    team = repo / "shape" / "team.md"
    team.write_text(team.read_text() + "| backend-node | backend-dev | stack-node-nest | services/billing/ |\n")
    assert edit(repo, "shapeup-team:backend-dev", "services/billing/src/invoice.ts") == "allow"
    assert edit(repo, "shapeup-team:backend-dev", "backend/deals/services.py") == "allow"


def test_older_team_files_with_path_keys_still_work(tmp_path):
    root = tmp_path / "old"
    (root / "shape").mkdir(parents=True)
    (root / "shape" / "team.md").write_text("| Key | Value |\n|---|---|\n| Backend path | backend/ |\n")
    assert edit(root, "shapeup-team:backend-dev", "backend/x.py") == "allow"
    assert edit(root, "shapeup-team:backend-dev", "web/x.js") == "deny"


def test_aws_snapshot_asks_and_other_rds_writes_are_blocked(repo):
    assert bash(repo, "aws rds create-db-snapshot --db-instance-identifier app --db-snapshot-identifier pre-s4", "shapeup-team:dba") == "ask"
    assert bash(repo, "aws rds describe-db-snapshots --db-instance-identifier app", "shapeup-team:dba") == "ask"
    assert bash(repo, "aws rds modify-db-instance --db-instance-identifier app --apply-immediately", "shapeup-team:dba") == "deny"


def test_literal_mysql_and_mongo_urls_to_remote_hosts_are_blocked(repo):
    assert bash(repo, "mysql --url mysql://root:pw@10.0.0.9/app") == "deny"
    assert bash(repo, "mongosh mongodb+srv://u:p@cluster0.example.net/app") == "deny"


def test_backend_and_dba_connections_to_production_ask_the_user(repo):
    assert bash(repo, 'psql "$READONLY_DATABASE_URL" -c "select count(*) from deals_deal"', "shapeup-team:dba") == "ask"
    assert bash(repo, 'psql "${READONLY_DATABASE_URL}" -c "select 1"', "shapeup-team:backend-dev") == "ask"
    assert bash(repo, "cloud-sql-proxy proj:europe-west1:pg", "shapeup-team:dba") == "ask"


def test_po_qa_and_frontend_have_no_production_access(repo):
    assert bash(repo, 'psql "$READONLY_DATABASE_URL" -c "select 1"', "shapeup-team:qa-engineer") == "deny"
    assert bash(repo, "gcloud sql instances list", "shapeup-team:frontend-dev") == "deny"
    assert bash(repo, "cloud-sql-proxy proj:europe-west1:pg", "shapeup-team:product-owner") == "deny"


def test_a_database_client_aimed_at_a_remote_host_asks_and_local_passes(repo):
    assert bash(repo, "psql -h 10.20.0.3 -U agent_ro app -c 'select 1'", "shapeup-team:dba") == "ask"
    assert bash(repo, "pg_dump --host=db.prod.internal app", "shapeup-team:backend-dev") == "ask"
    assert bash(repo, "psql -h localhost -U app test_app -c 'select 1'", "shapeup-team:backend-dev") == "allow"


@pytest.fixture
def fresh_repo(repo):
    (repo / "shape" / "pitches" / "win" / "board.md").unlink()  # setup or shaping: no cycle yet
    return repo


def test_before_the_first_kickoff_github_and_git_remote_calls_ask(fresh_repo):
    assert bash(fresh_repo, "gh auth status") == "ask"
    assert bash(fresh_repo, "git fetch origin") == "ask"
    assert bash(fresh_repo, "git push origin cycle/2026-C1-win", "shapeup-team:backend-dev") == "ask"


def test_before_the_first_kickoff_databases_tests_and_installs_ask(fresh_repo):
    assert bash(fresh_repo, "psql -h localhost -U app test_app -c 'select 1'") == "ask"
    assert bash(fresh_repo, "python manage.py migrate") == "ask"
    assert bash(fresh_repo, "cd backend && pytest -q") == "ask"
    assert bash(fresh_repo, "npm install") == "ask"
    assert bash(fresh_repo, "docker compose up -d db") == "ask"


def test_before_the_first_kickoff_reading_files_and_local_scripts_pass(fresh_repo):
    assert bash(fresh_repo, "cat package.json requirements.txt") == "allow"
    assert bash(fresh_repo, "grep -rlE 'postgres://' --include='*.py' .") == "allow"
    assert bash(fresh_repo, "python3 scaffold.py init . --product Deals") == "allow"
    assert bash(fresh_repo, "git status && git log --oneline -5") == "allow"


def test_hard_blocks_still_win_before_the_first_kickoff(fresh_repo):
    assert bash(fresh_repo, "git push --force origin main") == "deny"
    assert bash(fresh_repo, 'psql "$READONLY_DATABASE_URL"', "shapeup-team:qa-engineer") == "deny"
