"""Cycle de vie complet de l'écran d'accueil (splash ACTIF, sans bypass).

    python tests/shot_splash.py

Tous les rappels sont planifiés depuis on_start (même origine horloge que
le splash lui-même) : capture à 0,7 s — en pleine pluie binaire — puis
attente de la disparition réelle de l'overlay (fondu + retrait), avec un
délai maximum de sécurité.
"""
from __future__ import annotations

import glob
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# BABI_SPLASH volontairement non défini : l'écran d'accueil doit s'afficher
from kivy.clock import Clock  # noqa: E402

T0 = time.monotonic()
OUT_DIR = os.path.join(os.environ.get("TEMP", "."), "opencode")
OUT = os.path.join(OUT_DIR, "splash_demo.png")
DELAI_MAX = 8.0    # secondes murales avant abandon
RESULTAT = {"ok": False, "capture": "", "fini_a": None}


def _t() -> float:
    return time.monotonic() - T0


def _presence():
    from kivy.core.window import Window

    return [w for w in Window.children if type(w).__name__ == "SplashScreen"]


AGE_SHOT = [0.0]


def shot(_dt: float):
    """Capture à 0,7 s d'âge réel : accumule dt (origine horloge ignorée)."""
    AGE_SHOT[0] += min(_dt, 0.1)
    if AGE_SHOT[0] < 0.7:
        return
    from kivy.core.window import Window

    if not _presence():
        RESULTAT["ok"] = False
        print(f"[t={_t():.2f}] capture : le splash a disparu trop tot",
              flush=True)
        app.stop()
        return False
    for vieux in glob.glob(os.path.join(OUT_DIR, "splash_demo*.png")):
        os.remove(vieux)
    Window.screenshot(name=OUT)
    trouves = glob.glob(os.path.join(OUT_DIR, "splash_demo*.png"))
    RESULTAT["capture"] = trouves[0] if trouves else ""
    print(f"[t={_t():.2f}] capture -> {RESULTAT['capture'] or 'ECHEC'} "
          f"(age={AGE_SHOT[0]:.2f})", flush=True)
    return False


def attendre_fin(_dt: float) -> None:
    """Sonde jusqu'à ce que l'overlay ait disparu (ou délai max)."""
    if not _presence():
        if RESULTAT["fini_a"] is None:
            RESULTAT["fini_a"] = _t()
            print(f"[t={_t():.2f}] splash retire", flush=True)
            app.stop()
        return
    if _t() > T_DEPART[0] + DELAI_MAX:
        print(f"[t={_t():.2f}] ECHEC : toujours la apres {DELAI_MAX}s",
              flush=True)
        app.stop()


T_DEPART = [0.0]


def demarrer(_dt: float) -> None:
    """Planifié en on_start : mêmes origines horloge que le splash."""
    T_DEPART[0] = _t()
    print(f"[t={_t():.2f}] demarrer abs={time.monotonic():.3f}", flush=True)
    Clock.schedule_interval(shot, 0)
    Clock.schedule_interval(attendre_fin, 0.1)


from main import BabiProgrammeur  # noqa: E402

app = BabiProgrammeur()
app.bind(on_start=lambda *_a: demarrer(0))
app.run()

RESULTAT["ok"] = (
    bool(RESULTAT["capture"])
    and RESULTAT["fini_a"] is not None
    and RESULTAT["fini_a"] - T_DEPART[0] <= DELAI_MAX
)
print(f"RESULTAT capture={bool(RESULTAT['capture'])} "
      f"retire_apres={RESULTAT['fini_a']}", flush=True)
sys.exit(0 if RESULTAT["ok"] else 1)
