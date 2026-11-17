"""Generate the shapeup-team logo (hill chart with the crew) and the square plugin icon."""
import math

P0, P1, P2, P3 = (60, 262), (210, 262), (230, 78), (340, 78)
Q0, Q1, Q2, Q3 = (340, 78), (450, 78), (470, 262), (620, 262)
INK = "#5b6472"


def bez(p0, p1, p2, p3, t):
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return x, y


def face(cx, cy, r, look=0):
    ex, ey, er = r * 0.36, r * 0.12, r * 0.2
    s = ""
    for dx in (-ex, ex):
        s += f'<circle cx="{cx + dx:.1f}" cy="{cy - ey:.1f}" r="{er:.1f}" fill="#fff"/>'
        s += f'<circle cx="{cx + dx + look:.1f}" cy="{cy - ey:.1f}" r="{er * 0.55:.1f}" fill="#1f2430"/>'
    s += f'<path d="M{cx - r * 0.22:.1f} {cy + r * 0.32:.1f} q{r * 0.22:.1f} {r * 0.16:.1f} {r * 0.44:.1f} 0" stroke="#1f2430" stroke-width="2" fill="none" stroke-linecap="round"/>'
    return s


def body(cx, cy, r, color):
    # little feet + round body standing on the curve point (cx, cy is the foot point)
    by = cy - r - 3
    return (f'<ellipse cx="{cx - r * 0.4:.1f}" cy="{cy - 1:.1f}" rx="{r * 0.28:.1f}" ry="{r * 0.14:.1f}" fill="#5b6472"/>'
            f'<ellipse cx="{cx + r * 0.4:.1f}" cy="{cy - 1:.1f}" rx="{r * 0.28:.1f}" ry="{r * 0.14:.1f}" fill="#5b6472"/>'
            f'<circle cx="{cx:.1f}" cy="{by:.1f}" r="{r}" fill="{color}"/>'), by


def gear(x, y, r, color):
    teeth = "".join(
        f'<rect x="{x - r * 0.18:.1f}" y="{y - r * 1.25:.1f}" width="{r * 0.36:.1f}" height="{r * 0.5:.1f}" rx="1.5" fill="{color}" transform="rotate({a} {x:.1f} {y:.1f})"/>'
        for a in range(0, 360, 45))
    return teeth + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 0.42:.1f}" fill="#fff"/>'


def crew_svg():
    r = 21
    parts = []
    hill = (f'<path d="M{P0[0]} {P0[1]} C{P1[0]} {P1[1]} {P2[0]} {P2[1]} {P3[0]} {P3[1]} '
            f'C{Q1[0]} {Q1[1]} {Q2[0]} {Q2[1]} {Q3[0]} {Q3[1]}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    parts.append(f'<line x1="340" y1="40" x2="340" y2="272" stroke="{INK}" stroke-width="2" stroke-dasharray="4 7" opacity="0.6"/>')
    parts.append(hill)
    parts.append(f'<line x1="40" y1="272" x2="640" y2="272" stroke="{INK}" stroke-width="2" opacity="0.35"/>')
    parts.append(f'<text x="200" y="300" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" font-size="15" fill="{INK}">figuring it out</text>')
    parts.append(f'<text x="480" y="300" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" font-size="15" fill="{INK}">making it happen</text>')

    # designer: pink, paintbrush, first up the hill
    x, y = bez(P0, P1, P2, P3, 0.26)
    b, by = body(x, y, r, "#e64980")
    brush = (f'<g transform="rotate(-35 {x + r:.1f} {by:.1f})">'
             f'<rect x="{x + r - 2:.1f}" y="{by - 26:.1f}" width="5" height="26" rx="2" fill="#a0522d"/>'
             f'<rect x="{x + r - 3:.1f}" y="{by - 30:.1f}" width="7" height="6" fill="#adb5bd"/>'
             f'<path d="M{x + r - 3:.1f} {by - 30:.1f} q3.5 -12 7 0 z" fill="#fcc419"/></g>')
    parts += [b, face(x, by, r, 1.5), brush]

    # frontend dev: cyan, a code tag
    x, y = bez(P0, P1, P2, P3, 0.52)
    b, by = body(x, y, r, "#15aabf")
    tag = (f'<rect x="{x + r - 1:.1f}" y="{by - 34:.1f}" width="30" height="18" rx="4" fill="#f1f3f5" stroke="{INK}" stroke-width="2"/>'
           f'<text x="{x + r + 14:.1f}" y="{by - 21:.1f}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="11" '
           f'font-weight="700" fill="#1f2430">&lt;/&gt;</text>')
    parts += [b, face(x, by, r, 1.5), tag]

    # backend dev: blue, gear
    x, y = bez(P0, P1, P2, P3, 0.80)
    b, by = body(x, y, r, "#4c6ef5")
    parts += [b, face(x, by, r, 1.5), gear(x + r + 6, by - 14, 8, "#868e96")]

    # Shaper: magenta, at the top holding the flag
    x, y = P3
    b, by = body(x, y, r, "#be4bdb")
    flag = (f'<line x1="{x + r - 2:.1f}" y1="{by + 4:.1f}" x2="{x + r - 2:.1f}" y2="{by - 62:.1f}" stroke="#5b6472" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{x + r - 1:.1f} {by - 62:.1f} l34 9 l-34 9 z" fill="#f59f00"/>')
    parts += [flag, b, face(x, by, r, 0)]

    # QA: yellow, magnifier, downhill
    x, y = bez(Q0, Q1, Q2, Q3, 0.30)
    b, by = body(x, y, r, "#fab005")
    lens = (f'<line x1="{x - r - 4:.1f}" y1="{by + 2:.1f}" x2="{x - r - 14:.1f}" y2="{by + 14:.1f}" stroke="#5b6472" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="{x - r + 2:.1f}" cy="{by - 6:.1f}" r="9" fill="#e7f5ff" fill-opacity="0.8" stroke="#5b6472" stroke-width="3"/>')
    parts += [b, face(x, by, r, -1.5), lens]

    # DBA: red, database cylinder held close, downhill
    x, y = bez(Q0, Q1, Q2, Q3, 0.66)
    b, by = body(x, y, r, "#f03e3e")
    cx, cy, w, h = x + r + 4, by - 2, 22, 22
    db = (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h}" fill="#dee2e6" stroke="#5b6472" stroke-width="2"/>'
          f'<ellipse cx="{cx:.1f}" cy="{cy + h / 2:.1f}" rx="{w / 2}" ry="4" fill="#dee2e6" stroke="#5b6472" stroke-width="2"/>'
          f'<rect x="{cx - w / 2 + 1:.1f}" y="{cy - h / 2:.1f}" width="{w - 2}" height="{h}" fill="#dee2e6"/>'
          f'<ellipse cx="{cx:.1f}" cy="{cy - h / 2:.1f}" rx="{w / 2}" ry="4" fill="#f1f3f5" stroke="#5b6472" stroke-width="2"/>'
          f'<path d="M{cx - w / 2:.1f} {cy:.1f} q{w / 2} 7 {w} 0" fill="none" stroke="#5b6472" stroke-width="1.5"/>')
    parts += [b, face(x, by, r, 1.5), db]

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 -30 640 350" width="640" height="350" role="img" '
            'aria-label="shapeup-team: six crew members on a hill chart; the Shaper holds the flag at the top">'
            + "".join(parts) + "</svg>\n")


def icon_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128" role="img" aria-label="shapeup-team">'
            '<rect width="128" height="128" rx="28" fill="#1f2430"/>'
            '<path d="M16 100 C44 100 46 40 64 40 C82 40 84 100 112 100" fill="none" stroke="#f8f9fa" stroke-width="7" stroke-linecap="round"/>'
            '<line x1="64" y1="40" x2="64" y2="12" stroke="#f8f9fa" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M65 12 l20 6 l-20 6 z" fill="#f59f00"/>'
            '<circle cx="27" cy="94" r="6.5" fill="#e64980"/><circle cx="38" cy="76" r="6.5" fill="#15aabf"/><circle cx="48" cy="56" r="6.5" fill="#4c6ef5"/>'
            '<circle cx="82" cy="58" r="7" fill="#fab005"/><circle cx="94" cy="80" r="7" fill="#f03e3e"/>'
            '<circle cx="64" cy="40" r="7" fill="#be4bdb"/>'
            '</svg>\n')


if __name__ == "__main__":
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    (root / "docs" / "logo.svg").write_text(crew_svg())
    (root / "plugins" / "shapeup-team" / ".claude-plugin" / "icon.svg").write_text(icon_svg())
