"""Sonde d'entrées réelles : glisser (avec grab) + vraie molette SDL.

    python tests/probe_realinput.py

Reproduit les deux méthodes de l'utilisateur :
  1. glisser-déposer sur le contenu / la barre (passe par la boucle « grab »
     de kivy/base.py, exactement comme un vrai toucher) ;
  2. vrais événements molette injectés dans la file SDL (SDL_PushEvent),
     avec le curseur réel positionné sur la fenêtre — même chemin que le
     matériel : gate _collide_and_dispatch_cursor_enter -> fournisseur souris
     -> touch -> ScrollView.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes  # noqa: F401
import os
import sys
import time
import weakref

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
GATE: list[tuple] = []
MOUSE: list[str] = []

# ---------------------------------------------------------------- spies ----
_orig_gate = Window._collide_and_dispatch_cursor_enter


def _gate_spy(x, y):
    r = _orig_gate(x, y)
    GATE.append((round(x), round(y), bool(r)))
    return r


Window._collide_and_dispatch_cursor_enter = _gate_spy
Window.bind(
    on_mouse_down=lambda _w, _x, _y, btn, _m: MOUSE.append(str(btn))
)


# ------------------------------------------------------------- touches ----
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
    """Émule kivy/base.py : fenêtre, puis widgets « grabbés » avec grab_current."""
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


# ----------------------------------------------------------------- SDL -----
def find_sdl() -> str | None:
    import kivy

    base = os.path.dirname(os.path.dirname(kivy.__file__))  # site-packages
    for p in (
        os.path.join(base, "share", "sdl2", "bin", "SDL2.dll"),
        os.path.join(base, "kivy_deps", "sdl2", "SDL2.dll"),
    ):
        if os.path.exists(p):
            return p
    return None


SDL = None


def push_wheel(y_delta: int, times: int) -> None:
    global SDL
    if SDL is None:
        # 1) module deja charge par Kivy dans ce processus (le bon !)
        h = ctypes.windll.kernel32.GetModuleHandleW("SDL2.dll")
        try:
            SDL = ctypes.WinDLL("SDL2.dll") if h else None
        except OSError:
            SDL = None
        # 2) repli : chemin disque
        if SDL is None:
            path = find_sdl()
            if not path:
                REPORT.append("!! SDL2.dll introuvable")
                return
            SDL = ctypes.WinDLL(path)
    ev = (ctypes.c_uint32 * 14)()
    ev[0] = 0x403  # SDL_MOUSEWHEEL
    ev[1] = int(time.time() * 1000) & 0xFFFFFFFF
    ev[4] = 0  # x (scroll horizontal)
    ev[5] = y_delta & 0xFFFFFFFF  # y signé
    ok = 0
    for _ in range(times):
        ok += int(SDL.SDL_PushEvent(ctypes.byref(ev)))
    REPORT.append(f"   (SDL_PushEvent y={y_delta} x{times} -> {ok} acceptes)")


def move_cursor_ratio(sv, rx: float, ry: float) -> None:
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    hwnd = user32.FindWindowW(None, "BabiProgrammeur")
    if not hwnd:
        REPORT.append("!! fenêtre introuvable")
        return
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    cx = int(rect.left + (rect.right - rect.left) * rx)
    cy = int(rect.top + (rect.bottom - rect.top) * ry)
    user32.SetCursorPos(cx, cy)


# --------------------------------------------------------------- état ------
def find_sv(widget) -> ScrollView | None:
    if isinstance(widget, ScrollView) and widget.do_scroll_y:
        return widget
    for child in widget.children:
        found = find_sv(child)
        if found:
            return found
    return None


def later(fn, delay=0.45):
    Clock.schedule_once(lambda dt: fn(), delay)


def snap(label: str, sv, extra: str = "") -> float:
    REPORT.append(f"{label}: scroll_y={sv.scroll_y:.3f} {extra}")
    return sv.scroll_y


SV = {"sv": None}


def start(_dt: float) -> None:
    app.switch_tab("stats")
    later(phase_drag, 0.8)


def phase_drag() -> None:
    sv = find_sv(app.screens["stats"])
    SV["sv"] = sv
    REPORT.append(
        f"fenetre={Window.size} sv=({sv.x:.0f},{sv.y:.0f},{sv.width:.0f}x{sv.height:.0f}) "
        f"scroll_type={tuple(sv.scroll_type)} bar_width={sv.bar_width}"
    )
    before = snap("avant glisser", sv)
    # glisser le contenu vers le haut -> doit défiler vers le bas
    cx, cy = sv.center
    t = MouseTouch("left", cx, cy)
    dispatch_grabbed("down", t)
    steps = 10
    for i in range(1, steps + 1):
        t.goto(cx, cy + (300.0 * i / steps))
        dispatch_grabbed("move", t)
    dispatch_grabbed("up", t)
    later(lambda: after_drag(before), 0.5)


def after_drag(before: float) -> None:
    sv = SV["sv"]
    after = snap("apres glisser contenu", sv,
                 f"(delta={sv.scroll_y - before:+.3f})")
    # glisser sur la barre (bande de 4px a droite)
    bar_before = sv.scroll_y
    bx = sv.right - 2
    by = sv.top - sv.height * 0.25
    t = MouseTouch("left", bx, by)
    dispatch_grabbed("down", t)
    for i in range(1, 11):
        t.goto(bx, by + 30.0 * i)
        dispatch_grabbed("move", t)
    dispatch_grabbed("up", t)
    later(lambda: after_bar(bar_before), 0.5)


def after_bar(before: float) -> None:
    sv = SV["sv"]
    REPORT.append(
        f"apres glisser barre: scroll_y={sv.scroll_y:.3f} "
        f"(delta={sv.scroll_y - before:+.3f})"
    )
    phase_wheel("center", 0.5, 0.5)


def phase_wheel(label: str, rx: float, ry: float) -> None:
    move_cursor_ratio(SV["sv"], rx, ry)
    SV["sv"].scroll_y = 0.5  # point de depart net au milieu
    _wheel1.last = 0.5
    GATE.clear()
    MOUSE.clear()
    later(lambda: _wheel1(label), 0.35)


def _wheel1(label: str) -> None:
    push_wheel(+1, 8)  # y>0 -> 'mousewheeldown' -> btn 'scrolldown'
    later(lambda: _wheel1_done(label), 0.5)


def _wheel1_done(label: str) -> None:
    sv = SV["sv"]
    d1 = sv.scroll_y - _wheel1.last
    REPORT.append(
        f"molette[{label}] y=+1: scroll_y={sv.scroll_y:.3f} (delta={d1:+.3f}) "
        f"boutons={MOUSE[:4]} gate={GATE[:3]}"
    )
    _wheel1.last = sv.scroll_y
    push_wheel(-1, 8)  # y<0 -> 'mousewheelup' -> btn 'scrollup'
    later(lambda: _wheel2_done(label), 0.5)


_wheel1.last = 0.0


def _wheel2_done(label: str) -> None:
    sv = SV["sv"]
    d2 = sv.scroll_y - _wheel1.last
    REPORT.append(
        f"molette[{label}] y=-1: scroll_y={sv.scroll_y:.3f} (delta={d2:+.3f}) "
        f"boutons={MOUSE[:4]} gate={GATE[:3]}"
    )
    _wheel1.last = sv.scroll_y
    if label == "center":
        # tester aussi dans le coin bas-droite (gate potentiellement sensible)
        phase_wheel("coin-bas-droite", 0.9, 0.85)
    else:
        finish()


def finish() -> None:
    print("\n".join(REPORT))
    print("-" * 70)
    print("SONDE ENTREES REELLES : terminee")
    app.stop()


app = BabiProgrammeur()
Clock.schedule_once(start, 1.5)
app.run()
