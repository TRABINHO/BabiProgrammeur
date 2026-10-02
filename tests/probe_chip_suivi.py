"""Sonde des puces de langage : l'appui suffit-il à sélectionner ?

Trois chemins de toucher réels sont rejoués (pipeline kivy/base.py :
on_touch_down par la fenêtre, rejeu aux widgets grabbés avec transformation
des coordonnées — matrice g_translate du ScrollView) :

  1. appui rapide (le ScrollView délivre l'appui des enfants en différé :
     ButtonBehavior remet state à 'normal' 35 ms après on_release)
  2. bascule : appui sur la puce déjà sélectionnée (désélection) puis
     changement de langage
  3. appui long (>= 0,35 s : _change_touch_mode rend le toucher aux
     enfants pendant l'appui)

Chaque vérification a lieu 0,15 s après l'appui — APRÈS le _do_release
planifié — pour prouver que la sélection tient. Un contrôle identique est
fait sur l'onglet Formation.

    python tests/probe_chip_suivi.py

Données redirigées vers un fichier temporaire.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.input.motionevent import MotionEvent  # noqa: E402
from kivy.metrics import dp  # noqa: E402

os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402

REPORT: list[str] = []
TMP: str | None = None
DONE = {"flag": False}
RETRY = {"tab": 0}
CTX: dict = {}  # contexte de la phase en cours


def _trace(fn):
    def wrap(*_args):
        try:
            fn(*_args)
        except Exception as exc:  # noqa: BLE001
            import traceback
            REPORT.append(f"[ERREUR] {fn.__name__}: {exc!r}")
            REPORT.append(traceback.format_exc())
            Clock.schedule_once(finish, 0.1)
    return wrap


# ----------------------------------------------------------------- toucher --
class Touch(MotionEvent):
    def __init__(self, x: float, y: float):
        super().__init__("mouse", "chip-tap", ())
        self.profile = ["pos"]
        self.ud = {}
        self.set_pos(x, y)
        self.dx = self.dy = 0.0
        self.dsx = self.dsy = 0.0

    def set_pos(self, x: float, y: float) -> None:
        self.x = self.px = x
        self.y = self.py = y
        self.pos = (x, y)
        sx = x / max(Window.width, 1)
        sy = y / max(Window.height, 1)
        self.sx = self.psx = sx
        self.sy = self.psy = sy
        self.ox = self.osx = sx
        self.oy = self.osy = sy


def replay(touch: Touch, etype: str) -> None:
    for ref in list(touch.grab_list):
        wid = ref() if callable(ref) else ref
        if wid is None:
            continue
        touch.push()
        try:
            touch.apply_transform_2d(wid.to_widget)
            touch.grab_current = wid
            wid.dispatch(f"on_touch_{etype}", touch)
        finally:
            touch.grab_current = None
            touch.pop()


def down(x: float, y: float) -> Touch:
    t = Touch(x, y)
    Window.dispatch("on_touch_down", t)
    return t


def up(t: Touch) -> int:
    grabs = len(t.grab_list)
    Window.dispatch("on_touch_up", t)
    replay(t, "up")
    return grabs


def tap(x: float, y: float) -> int:
    return up(down(x, y))


# ------------------------------------------------------------------ helpers --
def chip_pos(screen, i: int):
    if i >= len(screen.chips):
        return None, None
    chip = screen.chips[i]
    cx, cy = chip.to_window(*chip.center)
    if not (0 < cx < Window.width - 1 and 0 < cy < Window.height - 1):
        return chip, None
    return chip, (cx, cy)


def reset_chips(screen) -> None:
    for c in screen.chips:
        c.state = "normal"
        c.locked = False


def check(tag: str, screen, chip, attendu: bool, champ: str) -> bool:
    ok = (chip.state == "down") == attendu and \
         chip.locked == attendu and \
         screen.lang_field.text.strip() == champ
    REPORT.append(
        f"[{tag}] {chip.text!r} : state={chip.state!r} "
        f"locked={chip.locked} champ={screen.lang_field.text!r} "
        f"(attendu selection={attendu}, champ={champ!r}) : "
        f"{'OK' if ok else 'ECHEC'}"
    )
    return ok


def wait_ready(_dt: float) -> None:
    timer = app.screens["timer"]
    app.switch_tab("timer")
    if abs(timer.x) >= 1 or timer.width < dp(200) or not timer.chips:
        RETRY["tab"] += 1
        if RETRY["tab"] <= 30:
            Clock.schedule_once(wait_ready, 0.3)
            return
    Clock.schedule_once(phase_fast, 0.4)


# --------------------------------------------------------------- phases ----
def phase_fast(_dt: float) -> None:
    """1. Appui rapide : la sélection doit tenir APRÈS le _do_release (+35 ms)."""
    timer = app.screens["timer"]
    timer.lang_field.text = ""
    reset_chips(timer)
    chip, pos = chip_pos(timer, 0)
    if pos is None:
        REPORT.append("[rapide] puce 0 hors fenêtre")
        Clock.schedule_once(phase_switch, 0.2)
        return
    CTX.update(screen=timer, chip=chip, champ=chip.text)
    CTX["grabs"] = tap(*pos)
    Clock.schedule_once(verify_fast, 0.15)


def verify_fast(_dt: float) -> None:
    check(f"rapide grabs={CTX['grabs']}", CTX["screen"], CTX["chip"], True,
          CTX["champ"])
    Clock.schedule_once(phase_switch, 0.2)


def phase_switch(_dt: float) -> None:
    """2a. Appui sur une autre puce : la sélection doit basculer."""
    timer = app.screens["timer"]
    chip, pos = chip_pos(timer, 1)
    if pos is None:
        REPORT.append("[bascule] puce 1 hors fenêtre")
        Clock.schedule_once(phase_toggle, 0.2)
        return
    CTX.update(screen=timer, chip=chip, champ=chip.text)
    CTX["grabs"] = tap(*pos)
    Clock.schedule_once(verify_switch, 0.15)


def verify_switch(_dt: float) -> None:
    check(f"bascule grabs={CTX['grabs']}", CTX["screen"], CTX["chip"], True,
          CTX["champ"])
    Clock.schedule_once(phase_toggle, 0.2)


def phase_toggle(_dt: float) -> None:
    """2b. Appui sur la puce DÉJÀ sélectionnée : désélection."""
    timer = app.screens["timer"]
    sel_idx = next((i for i, c in enumerate(timer.chips)
                    if c.text == timer.lang_field.text.strip()), None)
    if sel_idx is None:
        REPORT.append("[desel] aucune puce sélectionnée")
        Clock.schedule_once(phase_hold, 0.2)
        return
    chip, pos = chip_pos(timer, sel_idx)
    if pos is None:
        REPORT.append("[desel] puce hors fenêtre")
        Clock.schedule_once(phase_hold, 0.2)
        return
    CTX.update(screen=timer, chip=chip, champ="")
    CTX["grabs"] = tap(*pos)
    Clock.schedule_once(verify_toggle, 0.15)


def verify_toggle(_dt: float) -> None:
    check(f"desel grabs={CTX['grabs']}", CTX["screen"], CTX["chip"], False, "")
    Clock.schedule_once(phase_hold, 0.2)


HOLD: dict = {}


def phase_hold(_dt: float) -> None:
    """3. Appui long (0,35 s) : _change_touch_mode rend le toucher aux
    enfants pendant l'appui — la sélection doit aussi tenir."""
    timer = app.screens["timer"]
    timer.lang_field.text = ""
    reset_chips(timer)
    chip, pos = chip_pos(timer, 2)
    if pos is None:
        REPORT.append("[long] puce 2 hors fenêtre")
        Clock.schedule_once(phase_learn, 0.2)
        return
    CTX.update(screen=timer, chip=chip, champ=chip.text)
    HOLD["t"] = down(*pos)
    Clock.schedule_once(hold_up, 0.35)


def hold_up(_dt: float) -> None:
    CTX["grabs"] = up(HOLD["t"])
    Clock.schedule_once(verify_hold, 0.15)


def verify_hold(_dt: float) -> None:
    check(f"long grabs={CTX['grabs']}", CTX["screen"], CTX["chip"], True,
          CTX["champ"])
    Clock.schedule_once(phase_learn, 0.2)


def phase_learn(_dt: float) -> None:
    """Contrôle identique sur Formation (autre onglet, même structure)."""
    learn = app.screens["learn"]
    app.switch_tab("learn")
    if abs(learn.x) >= 1 or not learn.chips:
        RETRY["tab"] += 1
        if RETRY["tab"] <= 30:
            Clock.schedule_once(phase_learn, 0.3)
            return
    chip, pos = chip_pos(learn, 3)
    if pos is None:
        REPORT.append("[formation] puce 3 hors fenêtre")
        Clock.schedule_once(finish, 0.2)
        return
    grabs = tap(*pos)
    Clock.schedule_once(lambda dt, c=chip, g=grabs: verify_learn(dt, c, g),
                        0.15)


def verify_learn(_dt: float, chip, grabs: int) -> None:
    learn = app.screens["learn"]
    ok = chip.state == "down" and chip.locked and learn.lang == chip.text
    REPORT.append(
        f"[formation] {chip.text!r} grabs={grabs} : state={chip.state!r} "
        f"locked={chip.locked} lang={learn.lang!r} "
        f"(attendu {chip.text!r}) : {'OK' if ok else 'ECHEC'}"
    )
    Clock.schedule_once(finish, 0.3)


def finish(_dt: float = 0.0) -> None:
    if DONE["flag"]:
        return
    DONE["flag"] = True
    print("\n".join(REPORT))
    bad = [r for r in REPORT if "ECHEC" in r or r.startswith("[ERREUR]")]
    if not any(r.startswith("[rapide") for r in REPORT):
        bad.append("aucune phase terminee")
    print("-" * 70)
    print("SONDE PUCES SUIVI : " + ("PROBLEMES DETECTES" if bad else "OK"))
    if TMP:
        shutil.rmtree(TMP, ignore_errors=True)
    app.stop()


app = BabiProgrammeur()


def start(_dt: float) -> None:
    global TMP
    TMP = tempfile.mkdtemp(prefix="babi-chip-")
    app.store.path = os.path.join(TMP, "data.json")
    app.store.clear_all()
    wait_ready(None)


start = _trace(start)
wait_ready = _trace(wait_ready)
phase_fast = _trace(phase_fast)
verify_fast = _trace(verify_fast)
phase_switch = _trace(phase_switch)
verify_switch = _trace(verify_switch)
phase_toggle = _trace(phase_toggle)
verify_toggle = _trace(verify_toggle)
phase_hold = _trace(phase_hold)
hold_up = _trace(hold_up)
verify_hold = _trace(verify_hold)
phase_learn = _trace(phase_learn)
verify_learn = _trace(verify_learn)
Clock.schedule_once(start, 2.0)
Clock.schedule_once(finish, 45.0)
app.run()
_bad = [r for r in REPORT if "ECHEC" in r or r.startswith("[ERREUR]")]
if not any(r.startswith("[rapide") for r in REPORT):
    _bad.append("aucune phase terminee")
sys.exit(1 if _bad else 0)
