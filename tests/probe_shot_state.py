"""Etat de la splash AU MOMENT de la capture + analyse PIL de la meme image.

    python tests/probe_shot_state.py
L'objectif : relier la geometrie lue (centre, boite, texture) aux pixels
blancs du titre rendus, pour comprendre ou Kivy dessine reellement le texte.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import time  # noqa: E402

from kivy.clock import Clock  # noqa: E402

T0 = time.monotonic()
OUT_DIR = os.path.join(os.environ.get("TEMP", "."), "opencode")
OUT = os.path.join(OUT_DIR, "shot_state.png")
AGE = [0.0]
CAPTURE = [False]


def _t() -> float:
    return time.monotonic() - T0


def capturer(_dt: float) -> None:
    AGE[0] += min(_dt, 0.1)
    if AGE[0] < 0.7 or CAPTURE[0]:
        return
    from kivy.core.window import Window

    splash = [w for w in Window.children if type(w).__name__ == "SplashScreen"]
    if not splash:
        app.stop()
        return False
    sp = splash[0]
    t = sp._titre
    print(f"AVANT_CAPTURE win=({Window.width:.0f},{Window.height:.0f}) "
          f"sp=({sp.width:.0f},{sp.height:.0f})@({sp.x:.0f},{sp.y:.0f})", flush=True)
    print(f"AVANT_CAPTURE titre ctr=({t.center_x:.1f},{t.center_y:.1f}) "
          f"box={t.width:.0f}x{t.height:.0f} pos=({t.x:.1f},{t.y:.1f}) "
          f"tex={t.texture_size} text_size={t.text_size}", flush=True)
    print(f"AVANT_CAPTURE logo ctr=({sp.logo.center_x:.1f},{sp.logo.center_y:.1f}) "
          f"size=({sp.logo.width:.1f},{sp.logo.height:.1f}) "
          f"plaque={sp._plaque.pos}+{sp._plaque.size}", flush=True)
    Window.screenshot(name=OUT)
    print(f"AVANT_CAPTURE age={AGE[0]:.2f} t={_t():.2f} png={OUT}", flush=True)
    CAPTURE[0] = True
    Clock.schedule_interval(arret, 0.1)
    return False


def arret(_dt: float) -> None:
    for _ in range(50):
        if os.path.exists(OUT) and time.time() - os.path.getmtime(OUT) < 2:
            break
    app.stop()


def partir(_dt: float) -> None:
    Clock.schedule_interval(capturer, 0)


from main import BabiProgrammeur  # noqa: E402

app = BabiProgrammeur()
app.bind(on_start=lambda *_a: partir(0))
app.run()

# ---- analyse PIL de la capture produite -----------------------------------
import glob  # noqa: E402

from PIL import Image  # noqa: E402

fichiers = sorted(glob.glob(os.path.join(OUT_DIR, "shot_state*.png")))
if not fichiers:
    print("PIL: aucune capture")
    sys.exit(1)
im = Image.open(fichiers[-1]).convert("L")
w, h = im.size
print(f"PIL image {w}x{h}")

bandes = []
for y in range(h):
    blancs = sum(1 for x in range(0, w, 3) if im.getpixel((x, y)) > 205)
    if blancs > 25:
        bandes.append(y)
if bandes:
    y0, y1 = bandes[0], bandes[-1]
    ym = (y0 + y1) // 2
    xs = [x for x in range(w) if im.getpixel((x, ym)) > 205]
    print(f"PIL titre pixels y={y0}..{y1} (centre {(y0 + y1) / 2:.0f}) "
          f"x={xs[0]}..{xs[-1]} (centre {(xs[0] + xs[-1]) / 2:.0f})")
else:
    print("PIL: aucun texte blanc trouve")
sys.exit(0)
