"""Contrôle des fiches de contenu : couverture du curriculum, unicité des clés."""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import curriculum, content

miss = content.missing()
print(f"curriculum : {curriculum.grand_total()} elements, "
      f"{len(curriculum.langs())} langages")
print(f"fiches     : {content.coverage()}")

# Doublons de titres écrasés à la fusion ? on compare par lot
from core.content_1 import CONTENT as C1
from core.content_2 import CONTENT as C2
from core.content_3 import CONTENT as C3
from core.content_4 import CONTENT as C4
from core.content_5 import CONTENT as C5
total_lots = 0
for lot in (C1, C2, C3, C4, C5):
    for kinds in lot.values():
        for kind, fiches in kinds.items():
            total_lots += len(fiches)
print(f"lots       : {total_lots} fiches avant fusion")

if miss:
    print(f"SANS FICHE ({len(miss)}):")
    for lang, kind, title in miss:
        print(f"  - {lang} / {kind} / {title}")
else:
    print("couverture : COMPLETE (0 manquante)")

if total_lots != content.coverage():
    print(f"ATTENTION : fusion != somme des lots ({content.coverage()} vs {total_lots})")

# contrôle syntaxe basique : chaque fiche a un en-tete + lignes
bad = []
for lang, kinds in content.CONTENT.items():
    for kind, fiches in kinds.items():
        for title, text in fiches.items():
            if "\n" not in text.strip() or len(text) < 120:
                bad.append((lang, kind, title))
            if kind == "lessons" and not text.lstrip().startswith("OBJECTIFS"):
                bad.append((lang, kind, title, "tete"))
            if kind == "exercises" and not text.lstrip().startswith("ÉNONCÉ"):
                bad.append((lang, kind, title, "tete"))
if bad:
    print(f"FICHES ANORMALES ({len(bad)}) :")
    for b in bad:
        print("  ", b)

print("RESULTAT :", "OK" if not miss and not bad and total_lots == content.coverage() else "PROBLEMES")
