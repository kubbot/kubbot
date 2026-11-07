#!/usr/bin/env python3
"""Render the profile's self-contained SVG diagrams. No third-party packages."""

import argparse
from html import escape
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "workflow"
THEMES = {
    "dark": dict(bg="#14233b", card="#1d3150", raised="#294263",
                 ink="#f2f6ff", muted="#b0c1da", line="#647e9f",
                 blue="#a6c5ff", teal="#89ded5", peach="#f1c59f"),
    "light": dict(bg="#f6f8fc", card="#ffffff", raised="#e8eff9",
                  ink="#182b46", muted="#50637e", line="#8295af",
                  blue="#315ebb", teal="#176e67", peach="#88501e"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


class Figure:
    def __init__(self, theme, mobile, height, title, description):
        self.c = THEMES[theme]
        self.w = 640 if mobile else 1200
        self.h = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
            f'height="{height}" viewBox="0 0 {self.w} {height}" '
            'role="img" aria-labelledby="title description">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="description">{escape(description)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="{self.c["line"]}" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
            '</marker></defs>',
        ]
        self.rect(1, 1, self.w - 2, height - 2, "bg", radius=24)

    def rect(self, x, y, w, h, color="card", radius=16, stroke=None):
        border = f' stroke="{self.c[stroke]}" stroke-width="1.5"' if stroke else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                          f'rx="{radius}" fill="{self.c[color]}"{border}/>')

    def text(self, x, y, value, size=24, color="ink", weight=400, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{escape(FONT, quote=True)}" '
                          f'font-size="{size}" font-weight="{weight}" '
                          f'fill="{self.c[color]}" text-anchor="{anchor}">{escape(value)}</text>')

    def path(self, d, color="line", arrow=False, dashed=False, width=2):
        end = ' marker-end="url(#arrow)"' if arrow else ""
        dash = ' stroke-dasharray="6 7"' if dashed else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="{self.c[color]}" '
                          f'stroke-width="{width}" stroke-linecap="round" '
                          f'stroke-linejoin="round"{end}{dash}/>')

    def dot(self, x, y, color="blue", r=5):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{self.c[color]}"/>')

    def node(self, x, y, w, h, title, subtitle, accent="blue", size=30):
        self.rect(x, y, w, h)
        self.rect(x + 20, y + 24, 4, h - 48, accent, radius=2)
        self.text(x + 40, y + 44, title, size, weight=600)
        self.text(x + 40, y + 79, subtitle, 23, "muted")

    def footer(self, value, y=None):
        y = self.h - 38 if y is None else y
        self.path(f"M 56 {y - 34} H {self.w - 56}", width=1)
        self.text(56, y, value, 21, "muted")

    def finish(self):
        return "\n".join(self.parts + ["</svg>", ""])


def overview(theme, mobile):
    f = Figure(theme, mobile, 1020 if mobile else 770,
               "kubbot: intent becomes working software",
               "Intent and relevant context feed agent execution. Connected tools support "
               "the work, and delivery includes a change and its evidence.")
    f.path("M 57 50 V 81 M 57 66 L 75 50 M 57 66 L 77 81", "blue", width=4)
    f.text(94, 76, "kubbot", 32, weight=650)
    f.text(f.w - 56, 73, "AI workflow", 22, "muted", anchor="end")
    f.text(56, 166 if not mobile else 158, "Intent becomes", 66 if not mobile else 54, weight=650)
    f.text(56, 240 if not mobile else 224, "working software.", 66 if not mobile else 54, weight=650)
    if mobile:
        f.text(56, 284, "A connected workflow,", 28, "muted")
        f.text(56, 323, "from a clear goal to reviewed work.", 28, "muted")
        nodes = [("Intent", "Goal + acceptance", "blue"),
                 ("Context", "Sources + constraints + skills", "teal"),
                 ("Agent execution", "Plan + build + connected tools", "blue"),
                 ("Delivery", "Change + evidence", "peach")]
        for i, (title, subtitle, accent) in enumerate(nodes):
            y = 372 + i * 140
            if i:
                f.path(f"M 320 {y - 30} V {y - 4}", arrow=True)
            f.node(56, y, 528, 110, title, subtitle, accent, size=32)
        f.footer("Clear context. Concrete outcomes.")
    else:
        f.text(56, 295, "A connected workflow, from a clear goal to reviewed work.", 25, "muted")
        f.path("M 300 525 H 338 Q 350 525 350 537 V 543 H 380", arrow=True)
        f.path("M 590 447 V 478", arrow=True)
        f.path("M 800 543 H 876", arrow=True)
        f.path("M 590 646 V 612", arrow=True)
        f.node(56, 470, 244, 110, "Intent", "Goal + acceptance", size=31)
        f.node(380, 347, 420, 100, "Context", "Sources + constraints + skills", "teal")
        f.rect(380, 482, 420, 126, "raised")
        f.dot(411, 519)
        f.text(434, 528, "Agent execution", 32, weight=600)
        f.text(411, 572, "Plan + build + review", 25, "muted")
        f.node(880, 488, 264, 110, "Delivery", "Change + evidence", "peach")
        f.text(590, 680, "Tools via MCP", 24, "teal", anchor="middle")
        f.footer("Context in. Verified work out. Reviewed lessons back.")
    return f.finish()


STAGES = [
    ("Scope", "Goal + constraints", "Acceptance criteria", "teal"),
    ("Build", "Isolated branch", "A concrete change", "blue"),
    ("Verify", "Tests + review", "Evidence to inspect", "blue"),
    ("Deliver", "Pull request", "Result + evidence", "peach"),
]


def execution(theme, mobile):
    f = Figure(theme, mobile, 1250 if mobile else 690,
               "One task, end to end",
               "Scope, build, verify, deliver. Failed checks return to build. "
               "Release and real-world acceptance are separate checks.")
    f.text(56, 86, "One task, end to end.", 46 if mobile else 44, weight=600)
    f.text(56, 138, "Every handoff carries an artifact." if mobile else
           "Every handoff carries a concrete artifact.", 27 if mobile else 25, "muted")
    for i, (title, a, b, accent) in enumerate(STAGES):
        x, y, w, h = (76, 194 + i * 232, 508, 174) if mobile else (56 + i * 284, 210, 236, 190)
        if i:
            f.path(f"M 330 {y - 58} V {y - 5}" if mobile else f"M {x - 48} 303 H {x - 5}", arrow=True)
        f.rect(x, y, w, h)
        f.text(x + 24, y + 38, f"0{i + 1}", 23, accent, weight=600)
        f.text(x + (80 if mobile else 24), y + (41 if mobile else 88), title,
               34 if mobile else 32, weight=600)
        f.text(x + 24, y + (98 if mobile else 130), a, 28 if mobile else 23, "muted")
        f.text(x + 24, y + (139 if mobile else 164), b, 28 if mobile else 23, "muted")
    if mobile:
        f.path("M 76 745 H 32 V 513 H 71", arrow=True, dashed=True)
        f.text(56, 1118, "Failed check? Return to build.", 27, "muted")
        f.text(56, 1161, "Release + real-world acceptance", 26, "muted")
        f.text(56, 1198, "are checked separately.", 26, "muted")
    else:
        f.path("M 742 400 V 458 H 458 V 406", arrow=True, dashed=True)
        f.text(600, 501, "Failed check? Return to build.", 24, "muted", anchor="middle")
        f.rect(56, 548, 1088, 68, "raised", radius=12)
        f.dot(84, 583, "teal", 4)
        f.text(104, 590, "A passing check applies to the revision and surface it tested.", 24)
        f.text(56, 654, "Release and real-world acceptance stay explicit.", 23, "muted")
    return f.finish()


def context(theme, mobile):
    f = Figure(theme, mobile, 960 if mobile else 720,
               "Context that compounds",
               "Sources, skills and reviewed memory supply relevant context to an agent. "
               "MCP connects tools. Verified work feeds reviewed lessons back into memory.")
    f.text(56, 86, "Context compounds." if mobile else "Context that gets better with use.",
           46 if mobile else 44, weight=600)
    f.text(56, 139, "Retrieve what matters. Review what stays.", 25, "muted")
    if mobile:
        for i, (title, sub) in enumerate([("Sources", "Docs + code"), ("Skills", "How to work"),
                                        ("Memory", "Reviewed lessons")]):
            y = 200 + i * 126
            f.rect(56, y, 240, 96)
            f.text(76, y + 38, title, 29, weight=600)
            f.text(76, y + 73, sub, 23, "muted")
            f.path(f"M 296 {y + 48} H 344")
        f.path("M 344 248 V 500 M 344 409 H 377", arrow=True)
        f.rect(382, 200, 202, 96, "raised")
        f.text(402, 238, "MCP tools", 27, "teal", weight=600)
        f.text(402, 273, "Read + act", 24, "muted")
        f.path("M 483 296 V 331", arrow=True)
        f.rect(382, 336, 202, 146, "raised")
        f.text(402, 380, "Agent", 32, weight=600)
        f.text(402, 422, "Execute", 25, "muted")
        f.text(402, 457, "with context", 25, "muted")
        f.path("M 483 482 V 610 H 320 V 665", arrow=True)
        f.node(56, 670, 528, 110, "Verified work", "Code + review + evidence", "peach", 32)
        f.path("M 56 725 H 28 V 500 H 51", arrow=True, dashed=True)
        f.text(56, 851, "Review the outcome before", 28, "muted")
        f.text(56, 893, "saving a lesson for the next task.", 28, "muted")
    else:
        for i, (title, sub) in enumerate([("Sources", "Docs + repository"), ("Skills", "Reusable methods"),
                                        ("Memory", "Reviewed lessons")]):
            y = 204 + i * 110
            f.node(56, y, 320, 90, title, sub, "teal", 28)
            f.path(f"M 376 {y + 45} H 422")
        f.path("M 422 249 V 469 M 422 378 H 467", arrow=True)
        f.rect(472, 204, 672, 72, "raised")
        f.text(496, 250, "MCP", 27, "teal", weight=600)
        f.text(580, 250, "Connected tools to read, build and check", 25, "muted")
        f.path("M 600 276 V 305", arrow=True)
        f.rect(472, 310, 256, 136, "raised")
        f.text(500, 363, "Agent", 34, weight=600)
        f.text(500, 407, "Execute with context", 23, "muted")
        f.path("M 728 378 H 819", arrow=True)
        f.node(824, 323, 320, 110, "Verified work", "Code + review + evidence", "peach", 30)
        f.path("M 984 433 V 594 H 216 V 520", arrow=True, dashed=True)
        f.rect(390, 569, 548, 49, "bg", radius=8)
        f.text(664, 601, "Review outcomes. Keep what holds up.", 25, "muted", anchor="middle")
        f.footer("Skills define the method. Tools act. Memory keeps reviewed lessons.")
    return f.finish()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify committed assets without writing")
    args = parser.parse_args()
    stale = []
    for name, render in [("overview", overview), ("execution", execution), ("context", context)]:
        for mobile in (False, True):
            for theme in THEMES:
                path = OUT / f'{name}{"-mobile" if mobile else ""}-{theme}.svg'
                svg = render(theme, mobile)
                ET.fromstring(svg)
                if args.check:
                    if not path.exists() or path.read_text(encoding="utf-8") != svg:
                        stale.append(str(path.relative_to(ROOT)))
                else:
                    OUT.mkdir(parents=True, exist_ok=True)
                    path.write_text(svg, encoding="utf-8")
    if stale:
        print("Out-of-date assets:\n" + "\n".join(stale), file=sys.stderr)
        return 1
    print("12 workflow SVGs verified." if args.check else "Rendered 12 workflow SVGs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
