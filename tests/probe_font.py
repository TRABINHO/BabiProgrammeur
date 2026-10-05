"""Vérifie que Fira Sans a remplacé Roboto dans le slot par défaut Kivy."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import install_fonts  # noqa: E402

install_fonts()

from kivy.core.text import LabelBase  # noqa: E402
from kivy.uix.label import CoreLabel  # noqa: E402

fonts = getattr(LabelBase, "_fonts", {})
roboto = fonts.get("Roboto", [])
# ordre interne de LabelBase : regular, italic, bold, bolditalic
reg = str(roboto[0]) if len(roboto) > 0 else ""
bold = str(roboto[2]) if len(roboto) > 2 else ""
print("slot Roboto regular =", reg)
print("slot Roboto bold    =", bold)

if "FiraSans-Regular" not in reg or "FiraSans-Bold" not in bold:
    print("ECHEC : Fira Sans non enregistre sur le slot Roboto")
    sys.exit(1)

# La texture doit se construire avec la police (et non un repli muet).
lbl = CoreLabel(text="BabiProgrammeur 0123456789", font_size=32, bold=True)
lbl.refresh()
if not lbl.texture or lbl.texture.width <= 0:
    print("ECHEC : texture vide")
    sys.exit(1)
print("texture bold =", tuple(lbl.texture.size))
print("FIRA SANS : OK")
