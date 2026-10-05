"""Capture des 6 onglets pour inspection visuelle (charte SoloLearn).

Fenêtre réduite (390 x 610 dp) pour tenir dans l'écran de la machine de
test ; la mise en page se ré-adapte (colonne flexible, nav toujours en bas).

Usage : python tests/shot_ui.py [dossier_de_sortie]
Produit <sortie>/<onglet>.png pour chaque onglet de main.TABS.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main as m  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    r"C:\Users\USER\AppData\Local\Temp\opencode", "shots"
)
os.makedirs(OUT, exist_ok=True)

TABS = [k for k, _ in m.TABS]

_app = m.BabiProgrammeur()
_orig_build = _app.build


def _build():
    root = _orig_build()
    Window.size = (390, 610)  # dp — rentre dans l'ecran de la machine
    return root


_app.build = _build

from PIL import ImageGrab  # noqa: E402


def _detecte_bandeau(img):
    """(x0, x1, y0) du bandeau bleu = bornes de la fenetre."""
    px = img.load()
    w, h = img.size
    y0 = None
    for y in range(h):
        n = 0
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            if abs(r - 46) < 16 and abs(g - 167) < 16 and abs(b - 255) < 16:
                n += 1
        if n > 40:
            y0 = y
            break
    if y0 is None:
        raise RuntimeError("bandeau bleu introuvable")
    ymid = min(y0 + 30, h - 1)
    xs = [x for x in range(w)
          if abs(px[x, ymid][0] - 46) < 16
          and abs(px[x, ymid][1] - 167) < 16
          and abs(px[x, ymid][2] - 255) < 16]
    return min(xs), max(xs), y0


def _capture(key, reste, *_):
    img = ImageGrab.grab()
    x0, x1, y0 = _detecte_bandeau(img)
    hh = int(round(Window.size[1]))
    img.crop((x0, y0, x1 + 1, min(y0 + hh, img.size[1]))).save(
        os.path.join(OUT, key + ".png")
    )
    print("CAPTURE", key, "x", x0, x1, "y0", y0)
    Clock.schedule_once(lambda dt: _suite(reste), 0.15)


def _suite(restant, *_):
    if not restant:
        print("TOUTES LES CAPTURES OK ->", OUT)
        _app.stop()
        return
    key = restant[0]
    _app.switch_tab(key)
    Clock.schedule_once(lambda dt: _capture(key, restant[1:]), 1.0)


# 5 s : splash (1,2 s + fondu 0,45 s) + premier rendu stabilise.
Clock.schedule_once(lambda dt: _suite(TABS), 5.0)
_app.run()
sys.exit(0)
