"""Behaviour of the sketch renderer and the `scaffold.py wireframe` / `lint` commands."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "shapeup-team" / "skills" / "shapeup-team" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import wireframe  # noqa: E402

SHELL = "layout: side+top\nbrand: Acme\nnav: Deals | Reports\naccount: top-right\nsearch: yes\nmobile: bottom-tabs\n"
SKETCH = """title: Won this week
nav: Reports
# Won this week  >>  [Export CSV]^1
| Deal | Amount | x3
notes:
1 Downloads the rows shown.
"""


# Small: the renderer alone

def test_same_sketch_and_shell_draw_the_same_svg():
    assert wireframe.render(SKETCH, SHELL, "w") == wireframe.render(SKETCH, SHELL, "w")


def test_the_svg_carries_the_labels_the_reader_needs():
    svg = wireframe.render(SKETCH, SHELL, "w")
    for label in ("Won this week", "Export CSV", "Deal", "Amount", "Downloads the rows shown.", "Acme", "Reports"):
        assert f">{label}<" in svg


def test_the_current_nav_item_is_bold_and_the_others_are_not():
    svg = wireframe.render(SKETCH, SHELL, "w")
    assert 'font-weight="bold">Reports<' in svg
    assert 'font-weight="normal">Deals<' in svg


def test_an_unfilled_shell_draws_the_screen_without_app_chrome():
    template = "layout: <side | top>\nbrand: <name>\nnav: <Item | Item>\n"
    svg = wireframe.render(SKETCH, template, "w")
    assert ">Export CSV<" in svg
    assert "&lt;name&gt;" not in svg and "Search" not in svg


def test_labels_are_escaped():
    svg = wireframe.render('## Mark "A & B" <won>\n', None, "w")
    assert "A &amp; B" in svg and "<won>" not in svg


def test_a_row_splits_into_left_and_right_groups_with_markers():
    left, right = wireframe.tokens("(Owner ▾)  {Search}^2  >>  [Cancel]  [*Save]^3")
    assert [(k, l, m) for k, l, m in left] == [("select", "Owner", None), ("input", "Search", "2")]
    assert [(k, l, m) for k, l, m in right] == [("button", "Cancel", None), ("primary", "Save", "3")]


def test_the_digest_changes_when_the_shell_changes():
    assert wireframe.digest(SKETCH, SHELL) != wireframe.digest(SKETCH, SHELL.replace("Acme", "Beta"))


# Medium: the scaffold commands on a repo

SCAFFOLD = SCRIPTS / "scaffold.py"


def scaffold(*args):
    return subprocess.run([sys.executable, str(SCAFFOLD), *map(str, args)], capture_output=True, text=True)


@pytest.fixture
def pitch(tmp_path):
    scaffold("init", tmp_path)
    (tmp_path / "shape" / "shell.txt").write_text(SHELL)
    scaffold("pitch", tmp_path, "win", "--title", "Win a deal")
    sketches = tmp_path / "shape" / "pitches" / "win" / "wireframes"
    sketches.mkdir()
    (sketches / "won-this-week.txt").write_text(SKETCH)
    return tmp_path


def lint_rows(repo):
    return [l for l in scaffold("lint", repo, "win").stdout.splitlines() if "wireframe" in l.lower() or "sketch" in l.lower()]


def test_init_creates_the_shell_template(tmp_path):
    scaffold("init", tmp_path)
    assert "layout:" in (tmp_path / "shape" / "shell.txt").read_text()


def test_wireframe_draws_each_sketch_and_prints_the_embed_line(pitch):
    out = scaffold("wireframe", pitch, "win").stdout
    assert (pitch / "shape" / "pitches" / "win" / "wireframes" / "won-this-week.svg").exists()
    assert "![Won this week](wireframes/won-this-week.svg)" in out


def test_wireframe_without_a_pitch_draws_the_shell_preview(pitch):
    scaffold("wireframe", pitch)
    assert ">Acme<" in (pitch / "shape" / "shell.svg").read_text()


def test_lint_flags_a_sketch_that_is_not_drawn_or_not_embedded(pitch):
    rows = lint_rows(pitch)
    assert any("stale or missing" in r for r in rows)
    assert any("not embedded" in r for r in rows)


def test_lint_is_quiet_once_the_sketch_is_drawn_and_embedded(pitch):
    scaffold("wireframe", pitch, "win")
    p = pitch / "shape" / "pitches" / "win" / "pitch.md"
    p.write_text(p.read_text().replace("![<Screen>](wireframes/<screen>.svg)", "![Won this week](wireframes/won-this-week.svg)"))
    assert lint_rows(pitch) == []


def test_lint_flags_a_sketch_edited_after_drawing(pitch):
    scaffold("wireframe", pitch, "win")
    src = pitch / "shape" / "pitches" / "win" / "wireframes" / "won-this-week.txt"
    src.write_text(SKETCH.replace("Export CSV", "Download"))
    assert any("stale or missing" in r for r in lint_rows(pitch))


def test_lint_flags_an_ascii_wireframe_left_in_the_pitch(pitch):
    p = pitch / "shape" / "pitches" / "win" / "pitch.md"
    p.write_text(p.read_text() + "\n```text\n+--------+\n| Deals  |\n+--------+\n```\n")
    assert any("ASCII wireframe" in r for r in lint_rows(pitch))


def test_a_right_hand_group_too_wide_for_a_state_box_moves_below_and_is_reported():
    warnings = []
    svg = wireframe.render("# Northwind\nstate: Requested\n# Northwind  >>  [Go back]  [Request Account 360]  [Cancel request]\n",
                           SHELL, "w", warnings)
    assert any("doesn't fit on one line" in w for w in warnings)
    xs = [float(x) for x in __import__("re").findall(r'<text x="([\d.]+)"[^>]*>Go back<', svg)]
    assert xs and min(xs) > 20  # inside the state box, not pushed off its left edge


def test_a_sketch_that_fits_reports_nothing():
    warnings = []
    wireframe.render(SKETCH, SHELL, "w", warnings)
    assert warnings == []


def test_wireframe_prints_check_lines_for_layout_problems(pitch):
    src = pitch / "shape" / "pitches" / "win" / "wireframes" / "won-this-week.txt"
    src.write_text(SKETCH + "state: Busy\n# Won  >>  [Export CSV]  [Mark every deal reviewed]  [Share]\n")
    assert "check:" in scaffold("wireframe", pitch, "win").stdout


def solution_rows(repo):
    return [l for l in scaffold("lint", repo, "win").stdout.splitlines() if "Solution" in l or "Flow" in l or "breadboard" in l]


def set_solution(repo, body):
    p = repo / "shape" / "pitches" / "win" / "pitch.md"
    text = p.read_text()
    start, end = text.index("## Solution"), text.index("## Wireframes")
    p.write_text(text[:start] + "## Solution\nReps mark their own deals as won.\n\n" + body + "\n" + text[end:])


def test_the_pitch_template_passes_the_solution_checks(pitch):
    assert solution_rows(pitch) == []


def test_lint_flags_a_solution_without_flow_or_breadboard(pitch):
    set_solution(pitch, "| Place | Affordances |\n|---|---|\n| Deals | Mark won |\n")
    rows = solution_rows(pitch)
    assert any("### Flow" in r for r in rows) and any("### Breadboard" in r for r in rows)


def test_lint_flags_a_breadboard_without_numbered_steps_and_a_flow_that_is_not_a_swimlane(pitch):
    set_solution(pitch, "### Flow\n```mermaid\nflowchart TB\n  a --> b\n```\n\n### Breadboard\n"
                        "```mermaid\nflowchart LR\n  subgraph Deals\n    win[Mark won]\n  end\n```\n")
    rows = solution_rows(pitch)
    assert any("not a swimlane" in r for r in rows)
    assert any("no 'Step 1" in r for r in rows)


def test_lint_flags_more_than_four_sketches(pitch):
    sketches = pitch / "shape" / "pitches" / "win" / "wireframes"
    for n in range(4):
        (sketches / f"extra-{n}.txt").write_text(SKETCH)
    assert any("max 4" in r for r in lint_rows(pitch))


def test_audit_creates_a_dated_review_from_the_template(tmp_path):
    scaffold("init", tmp_path)
    scaffold("audit", tmp_path, "release", "--title", "Release process")
    files = list((tmp_path / "shape" / "audits").glob("*-release.md"))
    assert len(files) == 1
    text = files[0].read_text()
    assert "# Readiness review: Release process" in text and "| Pillar |" in text


def test_init_adds_the_services_table(tmp_path):
    scaffold("init", tmp_path)
    assert "## Services" in (tmp_path / "shape" / "team.md").read_text()
