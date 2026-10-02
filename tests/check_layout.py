"""Vérifie la géométrie des 5 écrans : débordements hors écran, chrome,
libellés de la navigation du bas.

    python tests/check_layout.py
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

main_mod.DEMO_MODE = True

PROBLEMS: list[str] = []
INFOS: list[str] = []
TABS = ["timer", "stats", "learn", "corrections", "goals", "history"]


def walk(widget, path=""):
    name = f"{path}/{type(widget).__name__}"
    yield widget, name
    for child in reversed(widget.children):
        yield from walk(child, name)


def check_screen(key: str, app: BabiProgrammeur) -> None:
    screen = app.screens[key]
    top = screen.y + screen.height
    INFOS.append(f"[{key}] écran {screen.width:.0f}x{screen.height:.0f} @ y={screen.y:.0f}..{top:.0f}")

    for widget, path in walk(screen):
        if widget is screen:
            continue
        # l'intérieur d'une ScrollView défile volontairement : on le tolère
        if "ScrollView" in path:
            continue
        y0 = screen.y + widget.y
        y1 = y0 + widget.height
        if y0 < screen.y - 1 or y1 > top + 1:
            PROBLEMS.append(
                f"{key}: {path} en Y [{y0:.1f}..{y1:.1f}] hors écran [{screen.y:.1f}..{top:.1f}]"
            )

    for widget, path in walk(screen, ""):
        if path.count("/") == 2:
            INFOS.append(
                f"     {type(widget).__name__:>14} y={screen.y + widget.y:6.1f}"
                f"->{screen.y + widget.y + widget.height:6.1f} h={widget.height:6.1f} "
                f"{getattr(widget, 'text', '')[:22]!r}"
            )


def check_chrome(app: BabiProgrammeur) -> None:
    root = app.root
    parts = {type(w).__name__: w for w in root.children}
    # enfants racine : en-tête (BoxLayout y max), ScreenManager, navigation
    boxes = [w for w in root.children if type(w).__name__ == "BoxLayout"]
    nav = min(boxes, key=lambda w: w.y)
    header = max(boxes, key=lambda w: w.y)
    sm = app.sm
    INFOS.append(f"[chrome] en-tête y={header.y:.1f}..{header.top:.1f} | "
                 f"écran y={sm.y:.1f}..{sm.top:.1f} | nav y={nav.y:.1f}..{nav.top:.1f} | "
                 f"fenêtre {root.width:.0f}x{root.height:.0f}")
    if nav.y < -0.5 or nav.top > root.height + 0.5:
        PROBLEMS.append("chrome: navigation hors fenêtre")
    if sm.top > header.y + 0.5:
        PROBLEMS.append(f"chrome: écrans (jusqu'à {sm.top:.1f}) recouvrent l'en-tête ({header.y:.1f})")
    if abs(sm.top - header.y) > 0.5:
        PROBLEMS.append(f"chrome: trou entre en-tête et écrans ({header.y:.1f} vs {sm.top:.1f})")
    if abs(sm.y - nav.top) > 0.5:
        PROBLEMS.append(f"chrome: trou entre écrans et navigation ({nav.top:.1f} vs {sm.y:.1f})")

    # libellés des onglets : le texte doit tenir dans chaque bouton (5 onglets)
    for key, btn in app.nav_buttons.items():
        tex = getattr(btn, "texture_size", None) or (0, 0)
        if tex[0] > btn.width - 4:
            PROBLEMS.append(
                f"nav: libellé « {btn.text} » déborde ({tex[0]:.0f} > {btn.width - 4:.0f})"
            )


INDEX = {"i": 0}
WAIT = {"n": 0}


def step(_dt: float) -> None:
    if INDEX["i"] == 0:
        # La fenêtre passe en « format téléphone » de façon asynchrone au
        # démarrage (SDL livre le redimensionnement avec un certain délai) :
        # tant que le ScreenManager n'est pas dimensionné, le chrome est
        # encore en vrac — on attend que le layout racine se pose.
        if app.sm.height <= 101.0:
            WAIT["n"] += 1
            if WAIT["n"] <= 40:  # ~12 s maximum
                Clock.schedule_once(step, 0.3)
                return
            PROBLEMS.append("chrome: layout racine jamais posé (délai dépassé)")
        check_chrome(app)
    key = TABS[INDEX["i"]]
    app.switch_tab(key)
    Clock.schedule_once(after, 0.8)


def after(_dt: float) -> None:
    key = TABS[INDEX["i"]]
    check_screen(key, app)
    INDEX["i"] += 1
    if INDEX["i"] < len(TABS):
        Clock.schedule_once(step, 0.2)
    else:
        finish()


def finish() -> None:
    print("\n".join(INFOS))
    print("-" * 70)
    if PROBLEMS:
        print("PROBLEMES DE MISE EN PAGE :")
        for p in PROBLEMS:
            print("  -", p)
    else:
        print("AUCUN PROBLEME DE MISE EN PAGE")
    app.stop()


app = BabiProgrammeur()
Clock.schedule_once(step, 2.0)
app.run()
sys.exit(1 if PROBLEMS else 0)
