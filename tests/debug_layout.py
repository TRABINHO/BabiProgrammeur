"""Affiche la géométrie réelle de l'interface (debug de mise en page).

    python tests/debug_layout.py [onglet]
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402

import main as main_mod  # noqa: E402
os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402

tab = sys.argv[1] if len(sys.argv) > 1 else "timer"
main_mod.DEMO_MODE = True
main_mod.START_TAB = tab

app = BabiProgrammeur()


def dump(widget, indent=0, depth=4):
    pad = "  " * indent
    print(f"{pad}{type(widget).__name__:>18}  pos=({widget.x:7.1f},{widget.y:7.1f}) "
          f"size=({widget.width:7.1f}x{widget.height:7.1f}) "
          f"hint={widget.size_hint} pos_hint={getattr(widget, 'pos_hint', {})} "
          f"txt={getattr(widget, 'text', '')[:28]!r}")
    if indent >= depth:
        return
    for child in reversed(widget.children):
        dump(child, indent + 1, depth)


def report(_dt: float) -> None:
    screen = app.screens.get(tab)
    root_widget = screen.children[0] if screen.children else None
    print("avant do_layout :", root_widget.pos, "screen:", screen.pos, "pos_hint:", root_widget.pos_hint)
    screen.do_layout()
    print("après do_layout:", root_widget.pos)
    screen.pos = (0, screen.y + 5)
    print("après déplacement screen:", root_widget.pos, screen.pos)
    app.stop()


Clock.schedule_once(report, 2.5)
app.run()
