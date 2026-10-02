"""Sonde de position de défilement : quelles opérations déplacent la liste ?

    python tests/probe_scroll_pos.py

Protocole : ouvrir Formation (données vidées → éléments NON lus), placer le
défilement à 0,500, puis mesurer après CHAQUE étape du flux « appui sur une
ligne → fiche → fermeture → rafraîchissement ». Rafraîchissement simple et
changement de langue servent de témoin. Données redirigées vers un fichier
temporaire (aucune donnée réelle n'est touchée).
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
from kivy.uix.scrollview import ScrollView  # noqa: E402

os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402
from ui.widgets import CheckRow  # noqa: E402

REPORT: list[str] = []
TMP: str | None = None
KEEP: dict = {}
DONE = {"flag": False}


# ------------------------------------------------------------- toucher réel --
class Touch(MotionEvent):
    """Toucher injecté par la fenêtre, pipeline réel de kivy/base.py."""

    def __init__(self, x: float, y: float):
        super().__init__("mouse", "scroll-tap", ())
        self.profile = ["pos"]
        self.ud = {}
        self.x = self.px = x
        self.y = self.py = y
        self.pos = (x, y)
        sx = x / max(Window.width, 1)
        sy = y / max(Window.height, 1)
        self.sx = self.psx = sx
        self.sy = self.psy = sy
        self.ox = self.osx = sx
        self.oy = self.osy = sy
        self.dx = self.dy = 0.0
        self.dsx = self.dsy = 0.0


def replay_up(touch: Touch) -> None:
    for ref in list(touch.grab_list):
        wid = ref() if callable(ref) else ref
        if wid is None:
            continue
        touch.push()
        try:
            touch.apply_transform_2d(wid.to_widget)
            touch.grab_current = wid
            wid.dispatch("on_touch_up", touch)
        finally:
            touch.grab_current = None
            touch.pop()


def tap(x: float, y: float) -> int:
    from kivy.core.window import Window

    t = Touch(x, y)
    Window.dispatch("on_touch_down", t)
    grabs = len(t.grab_list)
    Window.dispatch("on_touch_up", t)
    replay_up(t)
    return grabs


def scroll_sv(screen) -> ScrollView | None:
    """Le ScrollView vertical principal d'un écran (do_scroll_y=True)."""
    found: list[ScrollView] = []

    def walk(w):
        if isinstance(w, ScrollView) and getattr(w, "do_scroll_y", False):
            found.append(w)
        for child in w.children:
            walk(child)

    walk(screen)
    return found[0] if found else None


def measure(label: str) -> float:
    sv = scroll_sv(app.screens["learn"])
    val = sv.scroll_y
    base = KEEP.get("base", val)
    tag = "" if KEEP.get("base") is None else (
        f" (vs base {base:.3f})" +
        (" ECHEC" if abs(val - base) >= 0.05 else " OK"))
    REPORT.append(f"{label} : scroll_y={val:.3f}{tag}")
    KEEP.setdefault("base", val)
    return val


def first_row() -> CheckRow | None:
    """Première ligne des cours du langage courant (par titre exact)."""
    from core import curriculum

    learn = app.screens["learn"]
    title = curriculum.items(learn.lang, "lessons")[0][1]
    found: list[CheckRow] = []

    def walk(w):
        if isinstance(w, CheckRow) and w.title == title:
            found.append(w)
        for child in w.children:
            walk(child)

    walk(learn)
    return found[0] if found else None


def s1(_dt: float) -> None:
    global TMP
    TMP = tempfile.mkdtemp(prefix="babi-scroll-")
    app.store.path = os.path.join(TMP, "data.json")
    app.store.clear_all()
    app.switch_tab("learn")
    Clock.schedule_once(s2, 1.5)


def s2(_dt: float) -> None:
    sv = scroll_sv(app.screens["learn"])
    if sv is None:
        REPORT.append("ECHEC : pas de ScrollView sur Formation")
        Clock.schedule_once(finish, 0.2)
        return
    # position naturelle (haut de liste) — comme dans la sonde d'apprentissage
    measure("base (ouverture Formation)")
    Clock.schedule_once(s3, 0.5)


def s3(_dt: float) -> None:
    row = first_row()
    if row is None:
        REPORT.append("ECHEC : aucune ligne de cours")
        Clock.schedule_once(finish, 0.2)
        return
    wx, wy = row.to_window(*row.center)
    grabs = tap(wx, wy)  # VRAI toucher : la ligne ouvre la fiche (non lue)
    measure(f"apres TAP reel ({wx:.0f},{wy:.0f}) grabs={grabs}")
    Clock.schedule_once(s4, 0.5)


def s4(_dt: float) -> None:
    measure("apres appui (fiche ouverte)")
    from kivy.core.window import Window
    for w in list(Window.children):
        if type(w).__name__ == "ContentFiche":
            w.dismiss()
    Clock.schedule_once(s5, 0.5)


def s5(_dt: float) -> None:
    measure("apres fermeture de la fiche")
    app.screens["learn"].refresh()
    Clock.schedule_once(s6, 0.5)


def s6(_dt: float) -> None:
    measure("apres rafraichissement")
    for chip in app.screens["learn"].chips:
        if chip.text == "JavaScript":
            chip.dispatch("on_release")
            break
    Clock.schedule_once(s7, 0.5)


def s7(_dt: float) -> None:
    measure("apres changement de langue")
    Clock.schedule_once(finish, 0.3)


def finish(_dt: float) -> None:
    if DONE["flag"]:
        return
    DONE["flag"] = True
    if not REPORT:
        REPORT.append("ECHEC : aucune mesure (chaîne interrompue)")
    print("\n".join(REPORT))
    bad = [r for r in REPORT if "ECHEC" in r]
    print("-" * 70)
    print("SONDE DEFILEMENT : " + ("PROBLEMES DETECTES" if bad else "OK"))
    if TMP:
        shutil.rmtree(TMP, ignore_errors=True)
    app.stop()


app = BabiProgrammeur()
Clock.schedule_once(s1, 2.0)
Clock.schedule_once(finish, 45.0)  # fin garantie
app.run()
sys.exit(1 if [r for r in REPORT if "ECHEC" in r] else 0)
