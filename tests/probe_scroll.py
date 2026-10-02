"""Sonde de défilement : la molette atteint-elle le bas dans chaque onglet ?

    python tests/probe_scroll.py

Simule de vrais événements molette à travers la fenêtre (comme le ferait
l'utilisateur), puis vérifie que le dernier élément de contenu est bien
atteignable et que rien ne déborde de la colonne scrollée.
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

TABS = ["stats", "goals", "history", "learn"]
NOTCHES = 60
REPORT: list[str] = []


class WheelTouch(MotionEvent):
    """Événement molette semblable à celui du fournisseur souris."""

    def __init__(self, btn: str, x: float, y: float):
        super().__init__("mouse", "wheel-probe", ())
        self.button = btn
        self.profile = ["button"]
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


def find_vertical_svs(widget) -> list[ScrollView]:
    found: list[ScrollView] = []
    if isinstance(widget, ScrollView) and widget.do_scroll_y:
        found.append(widget)
    for child in widget.children:
        found.extend(find_vertical_svs(child))
    return found


def wheel_through_window(sv: ScrollView, btn: str, notches: int) -> None:
    cx, cy = sv.center
    for _ in range(notches):
        touch = WheelTouch(btn, cx, cy)
        Window.dispatch("on_touch_down", touch)
        Window.dispatch("on_touch_up", touch)


def geometry(tab: str, sv: ScrollView) -> dict:
    col = sv._viewport
    kids = list(reversed(col.children))  # ordre visuel (haut -> bas)
    overflow = max((k.y + k.height for k in kids), default=0.0) - col.height
    info = {
        "tab": tab,
        "sv_h": sv.height,
        "col_h": col.height,
        "scrollable": col.height - sv.height,
        "overflow": overflow,
        "last": kids[-1] if kids else None,
        "initial": sv.scroll_y,
    }
    return info


INDEX = {"i": 0}
PENDING: list[tuple] = []


def step(_dt: float) -> None:
    tab = TABS[INDEX["i"]]
    app.switch_tab(tab)
    Clock.schedule_once(lambda dt, tab=tab: after_switch(tab), 0.6)


def after_switch(tab: str) -> None:
    svs = find_vertical_svs(app.screens[tab])
    if not svs:
        REPORT.append(f"[{tab}] AUCUNE ScrollView verticale trouvee !")
        next_tab()
        return
    sv = svs[0]
    info = geometry(tab, sv)
    PENDING.append((info, sv))
    # molette vers le bas (scrolldown = onglette 1)
    wheel_through_window(sv, "scrolldown", NOTCHES)
    Clock.schedule_once(lambda dt, i=len(PENDING) - 1: measure(i), 0.5)


def measure(idx: int) -> None:
    info, sv = PENDING[idx]
    info["after_wheel"] = sv.scroll_y
    # si la molette n'a rien fait, essayer l'autre nom de bouton
    if abs(info["after_wheel"] - info["initial"]) < 1e-6:
        wheel_through_window(sv, "scrollup", NOTCHES)
        Clock.schedule_once(lambda dt, i=idx: measure2(i), 0.5)
    else:
        measure2(idx)


def measure2(idx: int) -> None:
    info, sv = PENDING[idx]
    info["after_wheel2"] = sv.scroll_y
    # atteindre le bas par la programmation pour isoler le problème
    sv.scroll_y = 0
    Clock.schedule_once(lambda dt, i=idx: verify(i), 0.3)


def verify(idx: int) -> None:
    info, sv = PENDING[idx]
    col = sv._viewport
    scroll = sv.scroll_y
    last = info["last"]
    # position fenetre du dernier element (origine du contenu via scroll_y)
    sh = max(col.height - sv.height, 0.0)
    content_y = sv.y - scroll * sh
    last_bottom = content_y + (last.y + last.height) if last is not None else 0.0
    last_top = content_y + (last.y) if last is not None else 0.0
    visible = last_bottom <= sv.top + 1 and last_top >= sv.y - 1

    wheel_ok = abs(info["after_wheel"] - info["initial"]) > 1e-6 or abs(
        info["after_wheel2"] - info["initial"]
    ) > 1e-6
    reached_bottom = scroll <= 0.01

    REPORT.append(
        f"[{info['tab']}] contenu={info['col_h']:.0f} fenetre={info['sv_h']:.0f} "
        f"defilable={info['scrollable']:.0f} | molette: {info['initial']:.2f} -> "
        f"{info['after_wheel']:.2f} -> {info['after_wheel2']:.2f} | scroll_y bas={scroll:.2f} | "
        f"dernier element visible={visible} | debordement contenu={info['overflow']:.1f}px"
    )
    if info["overflow"] > 1:
        REPORT.append(f"    !! contenu deborde de {info['overflow']:.1f}px (bas couperait)")
    if not wheel_ok:
        REPORT.append("    !! la molette via la fenetre N'AUCUN effet (evenement bloque ?)")
    if not visible:
        REPORT.append(
            f"    !! dernier element NON visible en bas (fenetre y={sv.y:.0f}..{sv.top:.0f}, "
            f"element y={last_top:.0f}..{last_bottom:.0f})"
        )
    next_tab()


def next_tab() -> None:
    INDEX["i"] += 1
    if INDEX["i"] < len(TABS):
        Clock.schedule_once(step, 0.2)
    else:
        finish()


def finish() -> None:
    print("\n".join(REPORT))
    bad = [r for r in REPORT if r.strip().startswith("!!")]
    print("-" * 70)
    print("SONDE DE DEFILEMENT : " + ("PROBLEMES DETECTES" if bad else "OK"))
    app.stop()


app = BabiProgrammeur()
Clock.schedule_once(step, 1.5)
app.run()
sys.exit(1 if [r for r in REPORT if r.strip().startswith("!!")] else 0)
