"""Timeline de la splash : qui deplace le titre (centre, tailles, evenements)?

    python tests/probe_splash_timeline.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402

AGE = [0.0]
LIGNES: list[str] = []
ETAT = {"prec": None}


def sonde(_dt: float) -> None:
    AGE[0] += min(_dt, 0.1)
    age = AGE[0]
    if age < 0.15 or age > 1.45:
        return
    from kivy.core.window import Window

    splash = [w for w in Window.children if type(w).__name__ == "SplashScreen"]
    if not splash:
        LIGNES.append(f"t={age:.2f} splash ABSENT")
        return
    sp = splash[0]
    t = sp._titre
    etat = (
        f"t={age:.2f} win={Window.width:.0f}x{Window.height:.0f} "
        f"sp={sp.width:.0f}x{sp.height:.0f}@({sp.x:.0f},{sp.y:.0f}) "
        f"titre ctr=({t.center_x:.0f},{t.center_y:.0f}) box={t.width:.0f}x{t.height:.0f} "
        f"logo=({sp.logo.center_x:.0f},{sp.logo.center_y:.0f})"
    )
    # n'imprime que les CHANGEMENTS pour garder une trace lisible
    if etat.split(" ", 1)[1] != ETAT["prec"]:
        LIGNES.append(etat)
        ETAT["prec"] = etat.split(" ", 1)[1]
    if age >= 1.4:
        app.stop()


def partir(_dt: float) -> None:
    Clock.schedule_interval(sonde, 0)


from main import BabiProgrammeur  # noqa: E402

app = BabiProgrammeur()
app.bind(on_start=lambda *_a: partir(0))
app.run()
print("\n".join(LIGNES))
sys.exit(0)
