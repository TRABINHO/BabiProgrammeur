"""Responsivité des onglets du bas : balaye un ensemble de largeurs d'ecran
(et reunit les libelles dans chaque bouton, sans chevauchement ni trou).

    python tests/probe_nav.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("BABI_SPLASH", "0")

from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.metrics import Metrics  # noqa: E402

import main as main_mod  # noqa: E402

main_mod.DEMO_MODE = True
from main import BabiProgrammeur  # noqa: E402

# largeurs cibles en dp (logiques) : telephones etroits -> tablette legere
WIDTHS_DP = [320, 360, 390, 414, 480, 600, 768]

PROBLEMS: list[str] = []
INFOS: list[str] = []
STEP = {"i": 0, "retry": 0, "h_log": 0}


def nav_of(app):
    root = app.root
    boxes = [w for w in root.children if type(w).__name__ == "BoxLayout"]
    return min(boxes, key=lambda w: w.y)


def ask_width(_dt: float) -> None:
    if STEP["i"] >= len(WIDTHS_DP):
        finish()
        return
    # Window.size s'exprime en dp (le getter rend des px physiques) :
    # on fige la hauteur logique initiale puis on balaie les largeurs logiques.
    if not STEP["h_log"]:
        STEP["h_log"] = round(Window.height / Metrics.density)
    w_dp = WIDTHS_DP[STEP["i"]]
    Window.size = (w_dp, STEP["h_log"])
    STEP["retry"] = 0
    Clock.schedule_once(measure, 0.8)


def measure(_dt: float) -> None:
    i = STEP["i"]
    w_dp = WIDTHS_DP[i]
    attendu = round(w_dp * Metrics.density)
    if abs(Window.width - attendu) > 2:
        # SDL livre le redimensionnement avec un certain retard
        STEP["retry"] += 1
        if STEP["retry"] <= 20:
            Clock.schedule_once(measure, 0.3)
            return
        PROBLEMS.append(f"{w_dp}dp: fenetre jamais passee a {attendu}px (est {Window.width}px)")

    app = app_ref["app"]
    nav = nav_of(app)
    btns = sorted(app.nav_buttons.values(), key=lambda b: b.x)

    INFOS.append(
        f"[{w_dp:4}dp / fenetre {Window.width}px] barre {nav.width:.0f}px "
        f"bouton {btns[0].width:.1f}px"
    )

    # 1) chaque libelle tient dans son bouton (marge 4px)
    for b in btns:
        tex = b.texture_size or (0, 0)
        INFOS.append(f"      « {b.text} » texture {tex[0]:.0f}px / dispo {b.width - 4:.0f}px")
        if tex[0] > b.width - 4:
            PROBLEMS.append(
                f"{w_dp}dp: libellé « {b.text} » déborde ({tex[0]:.0f} > {b.width - 4:.0f})"
            )

    # 2) pas de chevauchement entre boutons adjacents
    for a, c in zip(btns, btns[1:]):
        if a.right - c.x > 0.5:
            PROBLEMS.append(f"{w_dp}dp: chevauchement {a.text!r}/{c.text!r} ({a.right - c.x:.1f}px)")

    # 3) la barre couvre toute la largeur (aucun trou aux extremites)
    if abs(btns[0].x - nav.x) > 0.5 or abs(btns[-1].right - nav.right) > 0.5:
        PROBLEMS.append(
            f"{w_dp}dp: boutons [{btns[0].x:.1f}..{btns[-1].right:.1f}] "
            f"≠ barre [{nav.x:.1f}..{nav.right:.1f}]"
        )

    # 4) la barre reste dans la fenetre
    if nav.y < -0.5 or nav.top > Window.height + 0.5 or nav.x < -0.5 or nav.right > Window.width + 0.5:
        PROBLEMS.append(f"{w_dp}dp: barre hors fenetre (y={nav.y:.1f}, x={nav.x:.1f}, right={nav.right:.1f})")

    STEP["i"] += 1
    Clock.schedule_once(ask_width, 0.3)


def finish() -> None:
    print("\n".join(INFOS))
    print("-" * 70)
    if PROBLEMS:
        print("PROBLEMES DE RESPONSIVITE (navigation du bas) :")
        for p in PROBLEMS:
            print("  -", p)
    else:
        print("NAVIGATION RESPONSIVE : AUCUN PROBLEME")
    app_ref["app"].stop()


app_ref = {"app": None}

_app = BabiProgrammeur()
app_ref["app"] = _app
Clock.schedule_once(ask_width, 2.5)
_app.run()
sys.exit(1 if PROBLEMS else 0)
