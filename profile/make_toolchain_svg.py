"""Generate the soft-kite toolchain diagram (light and dark SVG) for the org profile.

Run from this folder:  python make_toolchain_svg.py
"""
from pathlib import Path

GH = "https://github.com/"
LINKS = {
    "TEF": GH + "awegroup/TEF",
    "AWESPA": GH + "awegroup/AWESPA",
    "EcoMo": GH + "awegroup/EcoMo",
    "AWETrim": GH + "awegroup/AWETrim",
    "VSM": GH + "awegroup/Vortex-Step-Method",
    "Billow": GH + "awegroup/Billow",
    "OpenSourceAWE": GH + "OpenSourceAWE",
    "EKF-AWE": GH + "awegroup/EKF-AWE",
    "awe-event-predictor": GH + "awegroup/awe-event-predictor",
    "awesIO": GH + "awegroup/awesIO",
}

THEMES = {
    "light": dict(bg="#ffffff", ink="#1a1a1a", soft="#555555", line="#444444",
                  tef=("#fdf1dc", "#fffaf0", "#8a5a00"), kite=("#ffffff", "#f5f9fd", "#2c5282"),
                  op=("#e6f2e6", None, "#2e6b30"), io=("#f3eefa", None, "#5b3a8c"),
                  data=("#f0f0f0", None, "#555555")),
    "dark": dict(bg="#0d1117", ink="#e6edf3", soft="#9da7b3", line="#9da7b3",
                 tef=("#3a2a0c", "#1f190e", "#e3a948"), kite=("#161b22", "#121a26", "#79a8e8"),
                 op=("#13281a", None, "#6cc070"), io=("#251b38", None, "#b79be6"),
                 data=("#21262d", None, "#9da7b3")),
}


def svg(theme):
    t = THEMES[theme]
    out = []
    add = out.append

    def text(x, y, s, size=13, weight="normal", fill=None, anchor="middle", italic=False, rot=None):
        tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
        style = ' font-style="italic"' if italic else ""
        add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill or t["ink"]}" '
            f'text-anchor="{anchor}"{style}{tr}>{s}</text>')

    def rect(x, y, w, h, fill, stroke, rx=10, dash=False, sw=1.3):
        d = ' stroke-dasharray="5 4"' if dash else ""
        add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d}/>')

    def tool(x, y, w, h, name, sub, pal, link=True, name_ink=None):
        fill, _, ink = pal
        if link and name in LINKS:
            add(f'<a href="{LINKS[name]}" target="_blank">')
        rect(x, y, w, h, fill, ink)
        cy = y + h / 2
        text(x + w / 2, cy - (4 if sub else -5), name, 15, "bold", name_ink or ink)
        if sub:
            text(x + w / 2, cy + 15, sub, 11.5, fill=t["soft"])
        if link and name in LINKS:
            add("</a>")

    def arrow(pts, dash=False, both=False):
        p = " ".join(f"{x},{y}" for x, y in pts)
        d = ' stroke-dasharray="5 4"' if dash else ""
        start = ' marker-start="url(#a)"' if both else ""
        add(f'<polyline points="{p}" fill="none" stroke="{t["line"]}" stroke-width="1.4"{d}'
            f' marker-end="url(#a)"{start}/>')

    W, H = 1015, 515
    add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">')
    add(f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{t["line"]}"/></marker></defs>')
    add(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')

    # level headers
    for x, s, key in ((165, "System level", "tef"), (505, "Kite level", "kite"), (840, "Operation level", "op")):
        text(x, 28, s, 17, "bold", t[key][2])

    # 01 system level: TEF
    _, outer, ink = t["tef"]
    add(f'<a href="{LINKS["TEF"]}" target="_blank">')
    rect(20, 45, 290, 340, outer, ink, rx=18, sw=1.6)
    text(165, 72, "TEF", 16, "bold", ink)
    add("</a>")
    tool(40, 90, 250, 70, "AWESPA", "wind resource → power curves → AEP", t["tef"])
    arrow([(165, 160), (165, 192)])
    text(172, 181, "AEP, system sizing", 11, fill=t["soft"], anchor="start", italic=True)
    tool(40, 192, 250, 70, "EcoMo", "capital, O&amp;M and replacement cost", t["tef"])
    arrow([(165, 262), (165, 292)])
    rect(65, 292, 200, 40, t["bg"], ink)
    text(165, 317, "LCoE · AEP · design optimum", 12.5, "bold")

    # 02 kite level: AWETrim
    _, outer, ink = t["kite"]
    add(f'<a href="{LINKS["AWETrim"]}" target="_blank">')
    rect(355, 45, 300, 340, outer, ink, rx=18, sw=1.6)
    text(505, 72, "AWETrim", 16, "bold", ink)
    add("</a>")
    tool(372, 90, 112, 62, "VSM", "aerodynamics", t["kite"], name_ink=t["ink"])
    tool(526, 90, 112, 62, "Billow", "structure", t["kite"], name_ink=t["ink"])
    arrow([(488, 121), (522, 121)], both=True)
    arrow([(505, 152), (505, 192)])
    text(512, 177, "identified aerodynamics", 11, fill=t["soft"], anchor="start", italic=True)
    rect(372, 192, 266, 42, t["kite"][0], ink)
    text(505, 218, "Reduced-order model", 14)
    arrow([(505, 234), (505, 262)])
    rect(372, 262, 266, 42, t["kite"][0], ink)
    text(505, 288, "Trajectory optimisation", 14)
    text(505, 335, "+ flight-data processing", 11, fill=t["soft"], italic=True)

    # power model: ROM -> AWESPA
    arrow([(372, 213), (332, 213), (332, 125), (292, 125)])
    text(325, 170, "power model", 11, fill=t["soft"], italic=True, rot=-90)

    # 03 operation level
    tool(700, 45, 280, 78, "OpenSourceAWE", "Julia simulation and path tracking", t["op"])
    tool(700, 165, 280, 60, "EKF-AWE", "real-time wind and state estimation", t["op"])
    tool(700, 265, 280, 70, "awe-event-predictor", "early warning of tether-force peaks", t["op"])
    arrow([(840, 165), (840, 125)], dash=True)
    text(848, 149, "wind estimate (planned)", 11, fill=t["soft"], anchor="start", italic=True)
    arrow([(980, 300), (992, 300), (992, 84), (982, 84)])
    text(1004, 192, "load warnings", 11, fill=t["soft"], italic=True, rot=90)
    # optimal paths: trajectory optimisation -> OpenSourceAWE
    arrow([(638, 283), (675, 283), (675, 84), (698, 84)])
    text(668, 190, "optimal paths", 11, fill=t["soft"], italic=True, rot=-90)

    # flight data
    fill, _, ink = t["data"]
    rect(730, 372, 220, 46, fill, ink)
    text(840, 400, "Flight data", 14, "bold")
    arrow([(760, 372), (760, 356), (688, 356), (688, 195), (698, 195)])
    arrow([(900, 372), (900, 337)])
    arrow([(730, 404), (505, 404), (505, 387)], dash=True)
    text(515, 398, "validation and model identification", 11, fill=t["soft"], anchor="start", italic=True)

    # awesIO
    fill, _, ink = t["io"]
    add(f'<a href="{LINKS["awesIO"]}" target="_blank">')
    rect(20, 440, 960, 44, fill, ink)
    text(500, 467, '<tspan font-weight="bold">awesIO</tspan>  –  common standard for system definitions '
                   'and data exchange, shared by all tools', 13.5, fill=ink)
    add("</a>")
    add("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    here = Path(__file__).parent
    for theme in THEMES:
        (here / f"soft_kite_toolchain_{theme}.svg").write_text(svg(theme), encoding="utf-8")
        print("written", theme)
