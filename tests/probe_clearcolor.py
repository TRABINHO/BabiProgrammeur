"""Trace qui définit Window.clearcolor et quand (fond navy vs #121212 KivyMD)."""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main as m  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402

# --- instrumentation de KivyMD ------------------------------------------
from kivymd.theming import ThemeManager  # noqa: E402

_orig = ThemeManager.set_clearcolor_by_theme_style


def _traced(self, theme_style):
    print(f">>> KivyMD set_clearcolor_by_theme_style({theme_style!r})")
    traceback.print_stack(limit=6)
    return _orig(self, theme_style)


ThemeManager.set_clearcolor_by_theme_style = _traced

# --- suivi periodique de la valeur ---------------------------------------
_revele = set()


def _log(dt):
    val = tuple(round(c, 4) for c in Window.clearcolor)
    if val not in _revele:
        _revele.add(val)
        print(f"[t={dt:.2f}s] Window.clearcolor = {val}")
    return False


_app = m.BabiProgrammeur()
_orig_build = _app.build


def _build():
    root = _orig_build()
    print("[fin build] clearcolor =", tuple(round(c, 4) for c in Window.clearcolor))
    return root


_app.build = _build

for t in (0.0, 0.3, 1.0, 2.0, 3.0, 5.0):
    Clock.schedule_once(_log, t)
Clock.schedule_once(lambda dt: _app.stop(), 6.0)
_app.run()
final = tuple(round(c, 6) for c in Window.clearcolor)
attendu = tuple(round(c, 6) for c in m.colors.BG)
print("FINAL =", final, "attendu =", attendu)
if final != attendu:
    print("ECHEC : le fond de fenetre n'est pas celui de la palette")
    sys.exit(1)
print("FOND NAVY VERROUILLE : OK")
