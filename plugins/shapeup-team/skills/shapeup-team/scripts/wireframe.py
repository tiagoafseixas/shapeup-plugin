#!/usr/bin/env python3
"""Fat-marker wireframes: a few lines of text -> a hand-drawn-style SVG. Stdlib only.

A sketch is drawn inside the app's shell (<docs>/shell.txt): the shell in grey, the pitch's parts in ink.
Notation: references/diagrams.md › Sketches. Same input -> same SVG (the wobble is seeded from the input).

  wireframe.py <sketch.txt> [--shell shell.txt] [-o out.svg]
"""
import hashlib
import html
import random
import re
import sys
from pathlib import Path

VERSION = "2"
INK, GREY, PAPER, NOTE, SHADE, FILL = "#3a3a3a", "#a5a5a5", "#fdfdfb", "#c0392b", "#ececec", "#e4e4e4"
FONT = "'Comic Sans MS','Comic Neue','Chalkboard SE','Segoe Print','Bradley Hand',cursive"
META_KEYS = ("title", "screen", "frame", "nav")
SHELL_KEYS = ("layout", "brand", "nav", "account", "search", "mobile")
GAP, ROW_GAP, PAD = 12, 14, 24


def width_of(s: str, size: float) -> float:
    return len(s) * size * 0.56


# ---------------------------------------------------------------- drawing

class Pen:
    def __init__(self, seed: int):
        self.rnd = random.Random(seed)
        self.out: list[str] = []
        self.warnings: list[str] = []

    def _j(self, v: float, a: float = 1.2) -> float:
        return v + self.rnd.uniform(-a, a)

    def line(self, x1, y1, x2, y2, color=INK, w=1.6, passes=2):
        for _ in range(passes):
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.out.append(f'<path d="M{self._j(x1):.1f},{self._j(y1):.1f} Q{self._j(mx, 2):.1f},{self._j(my, 2):.1f} '
                            f'{self._j(x2):.1f},{self._j(y2):.1f}" stroke="{color}" stroke-width="{w}" fill="none" '
                            f'stroke-linecap="round"/>')

    def box(self, x, y, w, h, color=INK, fill=None, sw=1.6, passes=2):
        if fill:
            self.out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{fill}"/>')
        self.line(x, y, x + w, y, color, sw, passes)
        self.line(x + w, y, x + w, y + h, color, sw, passes)
        self.line(x + w, y + h, x, y + h, color, sw, passes)
        self.line(x, y + h, x, y, color, sw, passes)

    def text(self, x, y, s, size=14, color=INK, anchor="start", weight="normal", underline=False):
        deco = ' text-decoration="underline"' if underline else ""
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{color}" '
                        f'text-anchor="{anchor}" font-weight="{weight}"{deco}>{html.escape(s)}</text>')

    def scribble(self, x, y, w, color=GREY):
        n = max(2, int(w / 8))
        pts = " ".join(f"L{x + i * 8:.1f},{y + (2.5 if i % 2 else -2.5):.1f}" for i in range(1, n))
        self.out.append(f'<path d="M{x:.1f},{y:.1f} {pts}" stroke="{color}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')

    def circle(self, cx, cy, r, color=INK, fill="none", sw=1.4):
        self.out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="{sw}"/>')

    def marker(self, n, x, y):
        self.out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{NOTE}"/>')
        self.text(x, y + 4.5, n, 12, "#fff", "middle", "bold")


# ---------------------------------------------------------------- parsing

def parse_sketch(text: str):
    meta, main, states, notes = {}, [], [], []
    rows, section = main, "main"
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        key = re.match(r"^(\w+):\s*(.*)$", line)
        if key and section == "main" and not main and key.group(1) in META_KEYS:
            meta[key.group(1)] = key.group(2).strip()
            continue
        if key and key.group(1) == "state":
            states.append((key.group(2).strip(), []))
            rows, section = states[-1][1], "state"
            continue
        if re.match(r"^notes:\s*$", line):
            section = "notes"
            continue
        if section == "notes":
            m = re.match(r"^(\d+)[.)]?\s+(.*)$", line)
            if m:
                notes.append([m.group(1), m.group(2)])
            elif notes:
                notes[-1][1] += " " + line
            continue
        rows.append(line)
    return meta, main, states, notes


def parse_shell(text: str | None) -> dict:
    shell = {}
    for raw in (text or "").splitlines():
        line = raw.split(" #")[0].strip()
        m = re.match(r"^([\w ]+):\s*(.*)$", line)
        if m and not line.startswith("#") and m.group(1).strip() in SHELL_KEYS:
            value = m.group(2).strip()
            if value and "<" not in value:
                shell[m.group(1).strip()] = value
    if shell.get("layout") not in ("side", "top", "side+top"):
        return {}
    shell["items"] = [i.strip() for i in shell.get("nav", "").split("|") if i.strip()]
    return shell


INLINE = [
    ("marker", r"\^(\d+)"),
    ("right", r">>"),
    ("primary", r"\[\*([^\]]+)\]"),
    ("check", r"\[([ xX])\]"),
    ("radio", r"\(([ xX•])\)"),
    ("button", r"\[([^\]#][^\]]*)\]"),
    ("input", r"\{([^{}]*)\}"),
    ("select", r"\(([^()]*?)\s*(?:▾|\sv)\)"),
    ("link", r"<([^<>]+)>"),
    ("quoted", r"\"([^\"]*)\""),
    ("text", r"(?:[^\[\]{}()<>\"^]|>(?!>))+"),
]


def tokens(row: str) -> tuple[list, list]:
    """Split one row into left and right groups of (kind, label, marker)."""
    left, right, group = [], [], None
    group = left
    pos = 0
    heading = re.match(r"^(#{1,2})\s+(.+?)(?=\s+>>|\s*\^\d|$)", row)
    if heading:
        group.append(["h1" if len(heading.group(1)) == 1 else "h2", heading.group(2).strip(), None])
        pos = heading.end()
    while pos < len(row):
        if row[pos].isspace():
            pos += 1
            continue
        for kind, pattern in INLINE:
            m = re.compile(pattern).match(row, pos)
            if not m:
                continue
            pos = m.end()
            if kind == "marker":
                target = group or left
                if target:
                    target[-1][2] = m.group(1)
            elif kind == "right":
                group = right
            elif kind in ("text", "quoted"):
                label = m.group(1) if kind == "quoted" else m.group(0).strip()
                if label:
                    group.append(["text", label, None])
            else:
                group.append([kind, m.group(1).strip(), None])
            break
        else:
            group.append(["text", row[pos], None])
            pos += 1
    return left, right


def inline_size(kind: str, label: str) -> tuple[float, float]:
    return {
        "h1": (width_of(label, 22) + 4, 30),
        "h2": (width_of(label, 17) + 4, 24),
        "primary": (width_of(label, 14) + 34, 34),
        "button": (width_of(label, 14) + 34, 34),
        "input": (max(200, width_of(label, 14) + 60), 32),
        "select": (width_of(label, 14) + 50, 30),
        "check": (16, 20),
        "radio": (16, 20),
        "link": (width_of(label, 14), 20),
        "text": (width_of(label, 14), 20),
    }[kind]


# ---------------------------------------------------------------- content layout

BLOCKS = [
    ("divider", r"^-{2,}$"),
    ("para", r"^~~~(?:\s*x(\d+))?$"),
    ("table", r"^\|(.+)\|(?:\s*x(\d+))?$"),
    ("cards", r"^cards:\s*(.*?)(?:\s*x(\d+))?$"),
    ("tabs", r"^tabs:\s*(.*)$"),
    ("empty", r"^\?\s+(.*)$"),
    ("image", r"^\[#\s*([^\]]*)\](?:\s*(\d+))?$"),
    ("textarea", r"^\{\{([^}]*)\}\}$"),
]


def layout(pen: Pen, rows: list[str], x: float, y: float, w: float) -> float:
    """Draw rows top to bottom inside width w; return the height used."""
    top = y
    for row in rows:
        color = INK
        if row.startswith(". ") or row == ".":
            color, row = GREY, row[1:].strip()
        marker = None
        m = re.search(r"\s*\^(\d+)\s*$", row)
        block = None
        for kind, pattern in BLOCKS:
            body = row[:m.start()] if m else row
            bm = re.match(pattern, body)
            if bm:
                block, marker = (kind, bm), (m.group(1) if m else None)
                break
        if block:
            h = draw_block(pen, block[0], block[1], x, y, w, color)
            if marker:
                pen.marker(marker, x + w, y)
        else:
            h = draw_inline_row(pen, row, x, y, w, color)
        y += h + ROW_GAP
    return max(0, y - top - ROW_GAP)


def draw_inline_row(pen: Pen, row: str, x: float, y: float, w: float, color: str) -> float:
    left, right = tokens(row)
    sized = lambda group: [(k, l, mk, *inline_size(k, l)) for k, l, mk in group]
    left, right = sized(left), sized(right)
    lines, cur, used = [], [], 0.0
    for t in left:  # wrap the left group when it overflows
        if t[3] > w:
            pen.warnings.append(f"'{t[1]}' is wider than its box ({t[3]:.0f} > {w:.0f}px): shorten the label")
        if cur and used + t[3] > w:
            lines.append(cur)
            cur, used = [], 0.0
        cur.append(t)
        used += t[3] + GAP
    lines.append(cur)
    right_lines, cur, used = [], [], 0.0
    for t in right:  # the right group wraps too, each line right-aligned
        if cur and used + t[3] > w:
            right_lines.append(cur)
            cur, used = [], 0.0
        cur.append(t)
        used += t[3] + GAP
    if cur:
        right_lines.append(cur)
    span = lambda group: sum(t[3] for t in group) + GAP * max(0, len(group) - 1)
    first = 0
    if right_lines and lines[0] and (len(right_lines) > 1 or len(lines) > 1
                                     or span(lines[0]) + GAP + span(right_lines[0]) > w):  # never overlap the left part
        pen.warnings.append(f"row '{row[:40]}' doesn't fit on one line ({span(lines[0]) + GAP + span(right):.0f} > {w:.0f}px): "
                            "the right-hand part moved below; draw only what changes")
        first = len(lines)
    elif len(right_lines) > 1:
        pen.warnings.append(f"row '{row[:40]}': the right-hand part is wider than the box ({span(right):.0f} > {w:.0f}px) and wraps")
    lines += [[] for _ in range(max(0, first + len(right_lines) - len(lines)))]
    total = 0.0
    for i, line in enumerate(lines):
        group_right = right_lines[i - first] if 0 <= i - first < len(right_lines) else []
        h = max([t[4] for t in line + group_right] or [20])
        cx = x
        for t in line:
            draw_inline(pen, t, cx, y + total, h, color)
            cx += t[3] + (6 if t[0] in ("check", "radio") else GAP)
        cx = x + w - span(group_right)
        for t in group_right:
            draw_inline(pen, t, cx, y + total, h, color)
            cx += t[3] + GAP
        total += h + (8 if i < len(lines) - 1 else 0)
    return total


def draw_inline(pen: Pen, t, x: float, y: float, row_h: float, color: str) -> None:
    kind, label, marker, w, h = t
    ty = y + (row_h - h) / 2
    mid = ty + h / 2 + 5
    if kind == "h1":
        pen.text(x, ty + 23, label, 22, color, weight="bold")
    elif kind == "h2":
        pen.text(x, ty + 18, label, 17, color, weight="bold")
    elif kind in ("button", "primary"):
        primary = kind == "primary"
        pen.box(x, ty, w, h, color, fill=FILL if primary else None, sw=2.2 if primary else 1.6)
        pen.text(x + w / 2, mid, label, 14, color, "middle")
    elif kind == "input":
        pen.box(x, ty, w, h, color)
        pen.text(x + 10, mid, label, 13, GREY)
    elif kind == "select":
        pen.box(x, ty, w, h, color)
        pen.text(x + 10, mid, label, 14, color)
        pen.text(x + w - 16, mid, "▾", 14, color, "middle")
    elif kind == "check":
        pen.box(x, ty + 2, 16, 16, color, sw=1.4, passes=1)
        if label.lower() == "x":
            pen.line(x + 3, ty + 10, x + 7, ty + 15, color, 1.8, 1)
            pen.line(x + 7, ty + 15, x + 14, ty + 4, color, 1.8, 1)
    elif kind == "radio":
        pen.circle(x + 8, ty + 10, 8, color)
        if label.strip():
            pen.circle(x + 8, ty + 10, 4, color, fill=color)
    elif kind == "link":
        pen.text(x, mid, label, 14, NOTE if color == INK else color, underline=True)
    else:
        pen.text(x, mid, label, 14, color)
    if marker:
        pen.marker(marker, x + w, ty)


def draw_block(pen: Pen, kind: str, m, x: float, y: float, w: float, color: str) -> float:
    if kind == "divider":
        pen.line(x, y + 4, x + w, y + 4, GREY, 1.2, 1)
        return 8
    if kind == "para":
        n = int(m.group(1) or 1)
        for i in range(n):
            pen.scribble(x, y + 8 + i * 18, w * (0.62 if i == n - 1 and n > 1 else 0.92))
        return n * 18
    if kind == "table":
        cols = [c.strip() for c in m.group(1).split("|")]
        n = int(m.group(2) or 3)
        h = 36 + n * 46
        pen.box(x, y, w, h, color)
        pen.line(x, y + 36, x + w, y + 36, color, 1.4, 1)
        cw = w / len(cols)
        for label in cols:
            if width_of(label, 14) + 24 > cw:
                pen.warnings.append(f"table column '{label}' is wider than its column ({cw:.0f}px): fewer or shorter columns")
        for c, label in enumerate(cols):
            pen.text(x + 12 + c * cw, y + 24, label, 14, color, weight="bold")
        for r in range(n):
            ry = y + 36 + r * 46
            if r:
                pen.line(x + 6, ry, x + w - 6, ry, GREY, 1, 1)
            for c in range(len(cols)):
                pen.scribble(x + 12 + c * cw, ry + 24, min(cw - 30, 120))
        return h
    if kind == "cards":
        title, n = m.group(1).strip(), int(m.group(2) or 3)
        per = max(1, min(n, int((w + GAP) // (170 + GAP))))
        cw = (w - GAP * (per - 1)) / per
        rows = (n + per - 1) // per
        for i in range(n):
            cx, cy = x + (i % per) * (cw + GAP), y + (i // per) * (110 + GAP)
            pen.box(cx, cy, cw, 110, color)
            if title:
                if width_of(title, 14) + 24 > cw and i == 0:
                    pen.warnings.append(f"card title '{title}' is wider than the card ({cw:.0f}px)")
                pen.text(cx + 12, cy + 26, title, 14, color, weight="bold")
            else:
                pen.scribble(cx + 12, cy + 22, min(cw - 40, 100), color)
            pen.scribble(cx + 12, cy + 56, cw - 30)
            pen.scribble(cx + 12, cy + 78, (cw - 30) * 0.6)
        return rows * 110 + (rows - 1) * GAP
    if kind == "tabs":
        cx = x
        pen.line(x, y + 32, x + w, y + 32, GREY, 1.2, 1)
        for label in [t.strip() for t in m.group(1).split("|") if t.strip()]:
            active = label.startswith("*")
            label = label.lstrip("*").strip()
            tw = width_of(label, 14)
            pen.text(cx, y + 20, label, 14, color, weight="bold" if active else "normal")
            if active:
                pen.line(cx - 4, y + 32, cx + tw + 4, y + 32, color, 3, 1)
            cx += tw + 28
        return 34
    if kind == "empty":
        pen.box(x, y, w, 90, GREY, passes=1)
        pen.text(x + w / 2, y + 50, m.group(1), 14, GREY, "middle")
        return 90
    if kind == "image":
        h = int(m.group(2) or 150)
        pen.box(x, y, w, h, color)
        pen.line(x, y, x + w, y + h, GREY, 1, 1)
        pen.line(x + w, y, x, y + h, GREY, 1, 1)
        if m.group(1).strip():
            tw = width_of(m.group(1), 14) + 16
            pen.out.append(f'<rect x="{x + w / 2 - tw / 2:.1f}" y="{y + h / 2 - 14:.1f}" width="{tw:.1f}" height="24" fill="{PAPER}"/>')
            pen.text(x + w / 2, y + h / 2 + 3, m.group(1).strip(), 14, color, "middle")
        return h
    if kind == "textarea":
        pen.box(x, y, w, 80, color)
        pen.text(x + 10, y + 22, m.group(1).strip(), 13, GREY)
        return 80
    return 0


def measure(rows: list[str], w: float) -> float:
    return layout(Pen(0), rows, 0, 0, w)


# ---------------------------------------------------------------- shell and frames

def draw_shell_desktop(pen: Pen, shell: dict, active: str, x, y, w, h) -> tuple[float, float, float, float]:
    """Draw the app shell in grey inside the window; return the content area (x, y, w, h)."""
    layout_kind = shell.get("layout", "")
    items, brand = shell.get("items", []), shell.get("brand", "")
    cx, cy, cw, ch = x, y, w, h
    if layout_kind in ("side", "side+top"):
        nav_w = 170
        pen.line(x + nav_w, y, x + nav_w, y + h, GREY, 1.2, 1)
        if brand:
            pen.text(x + 18, y + 32, brand, 16, GREY, weight="bold")
        for i, item in enumerate(items):
            iy = y + 62 + i * 36
            on = item.lower() == active.lower()
            if on:
                pen.out.append(f'<rect x="{x + 10:.1f}" y="{iy - 6:.1f}" width="{nav_w - 20}" height="30" rx="5" fill="{FILL}"/>')
            pen.circle(x + 26, iy + 9, 6, GREY if not on else INK, sw=1.2)
            pen.text(x + 40, iy + 14, item, 14, INK if on else GREY, weight="bold" if on else "normal")
        if shell.get("account", "none") != "none" and layout_kind == "side":
            pen.circle(x + 30, y + h - 30, 13, GREY)
            pen.scribble(x + 52, y + h - 30, 70)
        cx, cw = x + nav_w, w - nav_w
    if layout_kind in ("top", "side+top"):
        bar = 52
        pen.line(cx, y + bar, cx + cw, y + bar, GREY, 1.2, 1)
        tx = cx + 18
        if layout_kind == "top":
            if brand:
                pen.text(tx, y + 32, brand, 16, GREY, weight="bold")
                tx += width_of(brand, 16) + 34
            for item in items:
                on = item.lower() == active.lower()
                pen.text(tx, y + 32, item, 14, INK if on else GREY, weight="bold" if on else "normal")
                if on:
                    pen.line(tx - 4, y + bar - 2, tx + width_of(item, 14) + 4, y + bar - 2, INK, 3, 1)
                tx += width_of(item, 14) + 26
        right = cx + cw - 18
        if shell.get("account", "none") != "none":
            pen.circle(right - 14, y + 26, 13, GREY)
            right -= 44
        if shell.get("search", "no") in ("yes", "true", "on"):
            pen.box(right - 200, y + 12, 200, 28, GREY, passes=1)
            pen.text(right - 190, y + 31, "Search", 13, GREY)
        cy, ch = y + bar, h - bar
    return cx, cy, cw, ch


def render(sketch: str, shell_text: str | None = None, name: str = "", warnings: list | None = None) -> str:
    """Draw a sketch. Layout problems (overflow, clipped labels) are appended to `warnings`."""
    meta, main, states, notes = parse_sketch(sketch)
    shell = parse_shell(shell_text)
    frame = meta.get("frame", "page")
    mobile = meta.get("screen", "desktop") == "mobile"
    title = meta.get("title") or next((r.lstrip("# ").split(">>")[0].strip() for r in main if r.startswith("#")), name)
    active = meta.get("nav", "")
    source = digest(sketch, shell_text)
    pen = Pen(int(source[:8], 16))

    ox, oy = 20, 20
    fw = 390 if mobile else (760 if shell.get("layout", "").startswith("side") else 700)
    if frame == "none":
        fw = 390 if mobile else 600
    chrome = 0 if frame == "none" else (24 if mobile else 36)
    bar_mobile = 52 if mobile and shell else 0
    tabs_mobile = 60 if mobile and shell.get("mobile", "bottom-tabs") == "bottom-tabs" and shell.get("items") and frame != "none" else 0

    # content area width before drawing, to measure
    side = shell.get("layout", "").startswith("side") and not mobile and frame != "none"
    top_bar = (shell.get("layout") in ("top", "side+top") and not mobile and frame != "none")
    area_w = fw - (170 if side else 0)
    panel_w = {"dialog": min(460, area_w - 60), "drawer": min(380, area_w - 40)}.get(frame, area_w)
    if mobile and frame in ("dialog", "drawer"):
        panel_w = area_w
    inner_w = panel_w - 2 * PAD
    content_h = measure(main, inner_w)
    panel_h = content_h + 2 * PAD + (10 if frame in ("dialog", "drawer") else 0)
    area_h = max(panel_h + (120 if frame == "dialog" and not mobile else 0), 300 if mobile else 380)
    if frame == "none":
        area_h = panel_h
    fh = chrome + (52 if top_bar else 0) + bar_mobile + area_h + tabs_mobile
    if mobile and frame != "none":
        fh = max(fh, 640)

    # window and shell
    if frame == "none":
        pen.text(ox, oy - 4, title, 12, GREY)
        pen.box(ox, oy + 4, fw, fh, INK, sw=2)
        ax, ay, aw, ah = ox, oy + 4, fw, fh
    else:
        pen.box(ox, oy, fw, fh, INK, sw=2.4)
        if mobile:
            pen.line(ox + fw / 2 - 30, oy + 12, ox + fw / 2 + 30, oy + 12, GREY, 3, 1)
        else:
            pen.line(ox, oy + chrome, ox + fw, oy + chrome, GREY, 1.2, 1)
            for i in range(3):
                pen.circle(ox + 18 + i * 16, oy + 18, 4, GREY, sw=1.2)
            pen.text(ox + fw / 2, oy + 23, title, 13, GREY, "middle")
        ax, ay, aw, ah = ox, oy + chrome, fw, fh - chrome
        if mobile and shell:
            pen.line(ax, ay + 52, ax + aw, ay + 52, GREY, 1.2, 1)
            if shell.get("mobile") == "menu":
                for i in range(3):
                    pen.line(ax + 16, ay + 18 + i * 8, ax + 36, ay + 18 + i * 8, GREY, 2, 1)
            pen.text(ax + aw / 2, ay + 32, shell.get("brand", ""), 15, GREY, "middle", "bold")
            if shell.get("account", "none") != "none":
                pen.circle(ax + aw - 28, ay + 26, 12, GREY)
            if tabs_mobile:
                items = shell["items"][:5]
                ty = ay + ah - tabs_mobile
                pen.line(ax, ty, ax + aw, ty, GREY, 1.2, 1)
                step = aw / len(items)
                for i, item in enumerate(items):
                    on = item.lower() == active.lower()
                    c = INK if on else GREY
                    pen.circle(ax + step * (i + 0.5), ty + 20, 8, c, sw=1.2)
                    pen.text(ax + step * (i + 0.5), ty + 46, item, 11, c, "middle", "bold" if on else "normal")
            ay, ah = ay + 52, ah - 52 - tabs_mobile
        elif shell:
            ax, ay, aw, ah = draw_shell_desktop(pen, shell, active, ax, ay, aw, ah)

    # the pitch's part: page, dialog, drawer
    if frame == "dialog" and not mobile:
        pen.out.append(f'<rect x="{ax + 2:.1f}" y="{ay + 2:.1f}" width="{aw - 4:.1f}" height="{ah - 4:.1f}" fill="{SHADE}"/>')
        px, py = ax + (aw - panel_w) / 2, ay + (ah - panel_h) / 2
        pen.box(px, py, panel_w, panel_h, INK, fill=PAPER, sw=2)
        pen.text(px + panel_w - 20, py + 26, "×", 18, INK, "middle")
    elif frame == "drawer" and not mobile:
        pen.out.append(f'<rect x="{ax + 2:.1f}" y="{ay + 2:.1f}" width="{aw - 4:.1f}" height="{ah - 4:.1f}" fill="{SHADE}"/>')
        px, py = ax + aw - panel_w, ay
        pen.box(px, py, panel_w, ah, INK, fill=PAPER, sw=2)
        pen.text(px + panel_w - 20, py + 26, "×", 18, INK, "middle")
    elif frame in ("dialog", "drawer"):  # mobile: bottom sheet
        pen.out.append(f'<rect x="{ax + 2:.1f}" y="{ay + 2:.1f}" width="{aw - 4:.1f}" height="{ah - 4:.1f}" fill="{SHADE}"/>')
        px, py = ax, ay + ah - panel_h
        pen.box(px, py, panel_w, panel_h, INK, fill=PAPER, sw=2)
        pen.line(px + panel_w / 2 - 22, py + 10, px + panel_w / 2 + 22, py + 10, GREY, 3, 1)
    else:
        px, py = ax, ay
    layout(pen, main, px + PAD, py + PAD + (10 if frame in ("dialog", "drawer") else 0), inner_w)

    # notes and states
    nx, ny = ox + fw + 34, oy + 10
    width = nx + 260
    if notes:
        pen.text(nx, ny + 14, "Notes", 16, NOTE, weight="bold")
        ny += 40
        for n, body in notes:
            pen.text(nx, ny, n, 13, NOTE, weight="bold")
            for k, chunk in enumerate(wrap(body, 30)):
                pen.text(nx + 18, ny + k * 20, chunk, 13, INK)
            ny += 20 * len(wrap(body, 30)) + 8
    height = max(oy + fh + 4, ny) + 20
    if states:
        sw_ = 340 if not mobile else 300
        per = max(1, int((width - 20 + 30) // (sw_ + 30)))
        sy = height + 10
        row_h = 0.0
        for i, (label, rows) in enumerate(states):
            if i and i % per == 0:
                sy += row_h + 50
                row_h = 0.0
            sx = 20 + (i % per) * (sw_ + 30)
            h = measure(rows, sw_ - 2 * PAD) + 2 * PAD
            pen.text(sx, sy, f"State: {label}", 15, NOTE, weight="bold")
            pen.box(sx, sy + 12, sw_, h, GREY, passes=1)
            layout(pen, rows, sx + PAD, sy + 12 + PAD, sw_ - 2 * PAD)
            row_h = max(row_h, h)
        height = sy + 12 + row_h + 20
    width = max(width, ox + fw + 20)
    if warnings is not None:
        warnings.extend(dict.fromkeys(pen.warnings))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" '
            f'height="{height:.0f}">\n<!-- shapeup-wireframe v{VERSION} sha256:{source} {html.escape(name)} -->\n'
            f'<title>{html.escape(title)}</title>\n<rect width="100%" height="100%" fill="{PAPER}"/>\n'
            + "\n".join(pen.out) + "\n</svg>\n")


def wrap(s: str, n: int) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > n:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def digest(sketch: str, shell_text: str | None) -> str:
    return hashlib.sha256(f"v{VERSION}\n{sketch}\n--shell--\n{shell_text or ''}".encode()).hexdigest()[:16]


def svg_digest(svg: str) -> str | None:
    m = re.search(r"shapeup-wireframe v\d+ sha256:([0-9a-f]+)", svg)
    return m.group(1) if m else None


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sketch")
    ap.add_argument("--shell")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    src = Path(a.sketch)
    shell = Path(a.shell).read_text() if a.shell else None
    out = Path(a.out) if a.out else src.with_suffix(".svg")
    warnings: list[str] = []
    out.write_text(render(src.read_text(), shell, src.stem, warnings))
    print(f"drawn: {out}")
    for w in warnings:
        print(f"  check: {w}")


if __name__ == "__main__":
    sys.exit(main())
