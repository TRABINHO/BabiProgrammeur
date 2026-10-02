"""Capture l'interface de BabiProgrammeur directement depuis le framebuffer Kivy
(aucune capture d'écran, aucun problème de DPI).

    python tests/capture.py <onglet> <sortie.png> [--demo] [--dialog] [--fiche] [--seed]

--seed : injecte les données de démonstration dans un fichier TEMPORAIRE
(la vraie données reste intacte) — pratique pour voir les états cochés/lus.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Argument parsing AVANT l'import de main, qui nettoie sys.argv.
argv = sys.argv[1:]
FLAGS = {"--demo", "--dialog", "--fiche", "--seed"}
tab = next((a for a in argv if a not in FLAGS and not a.endswith(".png")), "timer")
out = next((a for a in argv if a.endswith(".png")), "capture.png")
DEMO = "--demo" in argv
DIALOG = "--dialog" in argv
FICHE = "--fiche" in argv
SEED = "--seed" in argv

from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402

# --seed : détourner le magasin vers un fichier temporaire AVANT construction
if SEED:
    from core import storage as _storage

    _seed_dir = tempfile.mkdtemp(prefix="babi-capture-seed-")
    _storage.default_file = lambda: os.path.join(_seed_dir, "data.json")

import main as main_mod  # noqa: E402
os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402

# ------------------------------------------------------------------ #
# Arguments
# ------------------------------------------------------------------ #

# main.py lit ces globales avant la construction de l'interface
main_mod.DEMO_MODE = DEMO
main_mod.START_TAB = tab

out_path = os.path.abspath(out)
print(f"[capture] onglet={tab} demo={DEMO} fichier={out_path}")
workdir = tempfile.mkdtemp(prefix="babiprogrammeur-capture-")
os.chdir(workdir)  # Window.screenshot() écrit dans le répertoire courant

app = BabiProgrammeur()


def capture(_dt: float) -> None:
    if SEED:
        # données de démonstration dans le magasin temporaire (--seed)
        from core.seed import seed

        seed(app.store)
        for scr in app.screens.values():
            scr.refresh()
    if FICHE:
        # Fiche plein écran du premier cours Python (bouton « Lire »)
        from core import content as fiches
        from core import curriculum
        from ui.dialogs import ContentFiche

        _slug, _title, _desc = curriculum.items("Python", "lessons")[0]
        ContentFiche(
            title=_title,
            meta="Python · Cours",
            desc=_desc,
            text=fiches.content_for("Python", "lessons", _title),
        ).open()
    elif DIALOG:
        from ui.dialogs import AppDialog

        AppDialog(
            "Arrêter la session ?",
            "App mobile\nDurée : 42 min",
            actions=[("Annuler", False, lambda: None), ("Arrêter", True, lambda: None)],
        ).open()

    Clock.schedule_once(_save, 1.0)


EXIT_OK = False


def _save(_dt: float) -> None:
    global EXIT_OK
    colors_nav = {k: tuple(round(c, 2) for c in v.color[:3]) for k, v in app.nav_buttons.items()}
    chrono = app.screens["timer"].timer_label.text
    print(f"[capture] sm.current={app.sm.current!r} ecran_courant={app.sm.current_screen.name!r} "
          f"chrono={chrono!r} boutons={colors_nav}")
    path = Window.screenshot(name="capture.png")
    ok = bool(path) and os.path.exists(path)
    if ok:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        shutil.move(path, out_path)
        print(f"CAPTURE OK -> {out_path}")
        EXIT_OK = True
    else:
        print("CAPTURE ECHEC")
    app.stop()


Clock.schedule_once(capture, 2.5)
app.run()
shutil.rmtree(workdir, ignore_errors=True)
if SEED:
    shutil.rmtree(_seed_dir, ignore_errors=True)
sys.exit(0 if EXIT_OK else 1)
