# -*- coding: utf-8 -*-
"""Verifie que LES ECRITS TIENNENT : chaque texte mesure face a sa boite.

Pour chaque libellé des 6 onglets (hors widgets KivyMD natifs) :
  - texte naturel (sans habillage) : texture <= boite (sinon debordement) ;
  - texte cadré (text_size) : hauteur texture (non bornée, mesurée au
    CoreLabel) <= hauteur boite (sinon derniere ligne rogne) ;
  - puces / boutons : texture <= largeur (sinon libellé ecrase).
Le raccourci « … » (shorten) est reproduit à la mesure pour ne pas
signaler un texte déjà tronqué volontairement.

    python tests/probe_text_fit.py [largeur_dp]   # défaut 390
Code 0 = tout tient.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.metrics import dp  # noqa: E402
from kivy.uix.label import CoreLabel, Label  # noqa: E402

import main as main_mod  # noqa: E402
os.environ.setdefault("BABI_SPLASH", "0")
from main import BabiProgrammeur  # noqa: E402

main_mod.DEMO_MODE = True

LARGEUR = int(sys.argv[1]) if len(sys.argv) > 1 else 390
PROBLEMS: list[str] = []
TABS = ["timer", "stats", "learn", "corrections", "goals", "history"]
ALPHA_CACHE: dict = {}


def walk(widget, path=""):
    name = f"{path}/{type(widget).__name__}"
    yield widget, name
    for child in reversed(widget.children):
        yield from walk(child, name)


def measure(lbl) -> tuple:
    """Texture réelle du texte (largeur contrainte, hauteur non bornée)."""
    cl = CoreLabel(
        text=lbl.text,
        font_name=getattr(lbl, "font_name", "Roboto"),
        font_size=lbl.font_size,
        bold=bool(getattr(lbl, "bold", False)),
        color=(1, 1, 1, 1),
    )
    ts = getattr(lbl, "text_size", None)
    if ts and ts[0]:
        cl.text_size = (float(ts[0]), None)
    if getattr(lbl, "shorten", False):
        cl.shorten = True
        cl.shorten_from = getattr(lbl, "shorten_from", "right")
        cl.max_lines = getattr(lbl, "max_lines", 0) or 0
    cl.refresh()
    tex = getattr(cl, "texture", None)
    return (float(tex.size[0]), float(tex.size[1])) if tex else (0.0, 0.0)


def check_screen(key: str, app: BabiProgrammeur) -> None:
    screen = app.screens[key]
    for widget, path in walk(screen):
        cls = type(widget).__name__
        if cls.startswith("MD"):            # widgets KivyMD natifs
            continue
        w, h = widget.width, widget.height
        if w <= 1 or h <= 1:                # masqué / à dimensionner
            continue
        text = getattr(widget, "text", "")
        if text:
            col = getattr(widget, "color", (1, 1, 1, 1))
            if len(col) >= 4 and col[3] == 0:   # invisible
                continue
            tw, th = measure(widget)
            ts = getattr(widget, "text_size", None)
            wrapped = bool(ts and ts[0])
            if wrapped:
                if th > h + 1:
                    PROBLEMS.append(
                        f"{key}: {path} ROGNE en Y ({th:.0f} > {h:.0f}) "
                        f"texte={text[:38]!r}"
                    )
            else:
                if tw > w + 1 or th > h + 1:
                    PROBLEMS.append(
                        f"{key}: {path} DEBORDE ({tw:.0f}x{th:.0f} vs "
                        f"{w:.0f}x{h:.0f}) texte={text[:38]!r}"
                    )
        # boutons à fond transparent (puces, nav) : texture propre
        if isinstance(widget, Label) and cls in ("Chip", "NavButton"):
            tex = getattr(widget, "texture_size", None) or (0, 0)
            if tex[0] > w - 2:
                PROBLEMS.append(
                    f"{key}: {path} libellé trop large "
                    f"({tex[0]:.0f} > {w - 2:.0f}) texte={text[:38]!r}"
                )


INDEX = {"i": 0}
WAIT = {"n": 0}
app = BabiProgrammeur()


def step(_dt: float) -> None:
    if INDEX["i"] == 0:
        if app.sm.height <= 101.0:
            WAIT["n"] += 1
            if WAIT["n"] <= 40:
                Clock.schedule_once(step, 0.3)
                return
            PROBLEMS.append("layout racine jamais posé")
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
    print(f"--- texte tenu, fenetre {LARGEUR} dp ---")
    if PROBLEMS:
        print(f"TEXTES QUI NE TIENNENT PAS : {len(PROBLEMS)}")
        for p in PROBLEMS:
            print("  -", p)
    else:
        print("TOUTS LES ECRITS TIENNENT")
    app.stop()


# fenêtre au format téléphone demandé
_orig_build = app.build


def _build():
    root = _orig_build()
    Window.size = (LARGEUR, 610)
    return root


app.build = _build

Clock.schedule_once(step, 2.0)
app.run()
sys.exit(1 if PROBLEMS else 0)
