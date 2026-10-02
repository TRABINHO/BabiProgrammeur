"""Mesure précise de l'overscroll après un glisser rapide (et de sa récupération).

    python tests/probe_overscroll.py
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.input.motionevent import MotionEvent  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402

import main as main_mod  # noqa: E402
os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402

main_mod.DEMO_MODE = True

REPORT: list[str] = []


class MouseTouch(MotionEvent):
    def __init__(self, btn: str, x: float, y: float):
        super().__init__("mouse", "probe-mouse", ())
        self.button = btn
        self.profile = ["button"]
        self._set(x, y)
        self.px, self.py = x, y
        self.dx = self.dy = 0.0

    def _set(self, x, y):
        self.x, self.y = x, y
        self.pos = (x, y)
        sx = x / max(Window.width, 1)
        sy = y / max(Window.height, 1)
        self.sx, self.sy = sx, sy
        self.ox, self.oy = sx, sy

    def goto(self, x, y):
        self.px, self.py = self.x, self.y
        self.dx, self.dy = x - self.x, y - self.y
        self._set(x, y)


def dispatch_grabbed(etype: str, touch) -> None:
    Window.dispatch(f"on_touch_{etype}", touch)
    if etype in ("move", "up"):
        for ref in list(touch.grab_list):
            wid = ref() if callable(ref) else ref
            if wid is None:
                continue
            touch.grab_current = wid
            try:
                wid.dispatch(f"on_touch_{etype}", touch)
            finally:
                touch.grab_current = None


def find_sv(widget) -> ScrollView | None:
    if isinstance(widget, ScrollView) and widget.do_scroll_y:
        return widget
    for child in widget.children:
        found = find_sv(child)
        if found:
            return found
    return None


SV: dict = {}
SAMPLES: list[float] = []


def start(_dt: float) -> None:
    app.switch_tab("stats")
    Clock.schedule_once(drag_phase, 0.8)


def drag_phase(_dt: float) -> None:
    sv = find_sv(app.screens["stats"])
    SV["sv"] = sv
    e = sv.effect_y
    REPORT.append(
        f"avant : scroll_y={sv.scroll_y:.3f} eff(value={e.value:.1f}, "
        f"scroll={e.scroll:.1f}, min={e.min:.1f}, max={e.max:.1f}, "
        f"vel={e.velocity:.1f}, manual={e.is_manual})"
    )
    # glisser rapide vers le haut depuis le milieu -> fuite sous le bas
    cx, cy = sv.center
    t = MouseTouch("left", cx, cy)
    dispatch_grabbed("down", t)
    for i in range(1, 7):
        t.goto(cx, cy + 70.0 * i)
        dispatch_grabbed("move", t)
    dispatch_grabbed("up", t)
    # échantillonner scroll_y + effet pendant 3 s
    schedule_samples(0)


def schedule_samples(n: int) -> None:
    if n >= 12:
        finish()
        return
    Clock.schedule_once(lambda dt, n=n: sample(n), 0.25 * (n + 1))


def sample(n: int) -> None:
    sv = SV["sv"]
    e = sv.effect_y
    REPORT.append(
        f"t+{0.25 * (n + 1):.2f}s scroll_y={sv.scroll_y:+.3f} "
        f"eff(value={e.value:+.1f}, scroll={e.scroll:+.1f}, vel={e.velocity:+.1f}, "
        f"manual={e.is_manual})"
    )
    schedule_samples(n + 1)


def finish() -> None:
    print("\n".join(REPORT))
    app.stop()


app = BabiProgrammeur()
Clock.schedule_once(start, 1.5)
app.run()
