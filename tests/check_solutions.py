"""Contrôle des corrections (onglet Correction) : couverture du curriculum,
en-têtes dans l'ordre, longueur et caractères interdits.

Usage : python tests/check_solutions.py [langage ...]   (défaut : tous)
Sortie : 0 si tout est conforme, 1 sinon.
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import curriculum, solutions  # noqa: E402

SEUIL_MIN = 700            # longueur absolue minimale (caractères)
SEUIL_CIBLE = (900, 1400)  # fourchette visée (information)
AVERTIR_LONGUE = 1500      # au-delà : signalé, non bloquant

TETES = ("SOLUTION", "EXPLICATION", "POINTS DE VÉRIFICATION",
         "POUR ALLER PLUS LOIN")

FLECHES = {
    "\u2190": "flèche gauche",
    "\u2191": "flèche vers le haut",
    "\u2192": "flèche droite",
    "\u2193": "flèche vers le bas",
    "\u2194": "flèche bidirectionnelle",
    "\u21d0": "flèche double gauche",
    "\u21d2": "flèche double droite",
    "\u27f6": "flèche longue",
}


def contient_emoji(text: str) -> bool:
    """Détecte les jetons des plages emoji usuelles."""
    for c in text:
        o = ord(c)
        if 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF \
                or 0x2B00 <= o <= 0x2BFF or 0xFE00 <= o <= 0xFE0F:
            return True
    return False


langs = sys.argv[1:] or curriculum.langs()
inconnus = [l for l in langs if not curriculum.has_lang(l)]
if inconnus:
    print(f"LANGAGE INCONNU : {inconnus}")
    print("RESULTAT : PROBLEMES")
    sys.exit(1)

# somme des lots avant fusion (contrôle de fusion)
from core.solutions_1 import CONTENT as L1  # noqa: E402
from core.solutions_2 import CONTENT as L2  # noqa: E402
from core.solutions_3 import CONTENT as L3  # noqa: E402
from core.solutions_4 import CONTENT as L4  # noqa: E402
from core.solutions_5 import CONTENT as L5  # noqa: E402

total_lots = 0
for lot in (L1, L2, L3, L4, L5):
    for kinds in lot.values():
        for _kind, fiches in kinds.items():
            total_lots += len(fiches)

probs = []
nb = 0
longueurs = []
for lang in langs:
    for _slug, title, _desc in curriculum.items(lang, "exercises"):
        if not solutions.has_solution(lang, title):
            probs.append(f"{lang} / {title} : correction absente")
            continue
        text = solutions.solution_for(lang, title)
        nb += 1
        longueurs.append(len(text))

        if len(text) < SEUIL_MIN:
            probs.append(f"{lang} / {title} : trop courte "
                         f"({len(text)} < {SEUIL_MIN})")
        elif len(text) > AVERTIR_LONGUE:
            print(f"  [info] {lang} / {title} : longue ({len(text)})")

        lignes = [l.strip() for l in text.splitlines()]
        entetes = [l for l in lignes if l in TETES]
        if entetes != list(TETES):
            probs.append(f"{lang} / {title} : en-têtes {entetes} "
                         f"au lieu de {list(TETES)}")
        if not lignes or lignes[0] != "SOLUTION":
            probs.append(f"{lang} / {title} : la première ligne doit être "
                         "SOLUTION")

        for c, nom in FLECHES.items():
            if c in text:
                probs.append(f"{lang} / {title} : {nom} {c!r} interdite")
        if contient_emoji(text):
            probs.append(f"{lang} / {title} : emoji interdit")
        if "```" in text or "**" in text:
            probs.append(f"{lang} / {title} : markdown interdit")
        if any(l.startswith("# ") for l in lignes):
            probs.append(f"{lang} / {title} : titre markdown « # » interdit")

manquants = [(l, t) for l, t in solutions.missing() if l in langs]

print(f"corrections  : {solutions.coverage()} rédigées "
      f"({total_lots} avant fusion)")
print(f"vérifiées    : {nb} sur {len(langs)} langage(s)")
if longueurs:
    print(f"longueurs    : min {min(longueurs)} · "
          f"moy {sum(longueurs) // len(longueurs)} · max {max(longueurs)} "
          f"(cible {SEUIL_CIBLE[0]}-{SEUIL_CIBLE[1]}, min {SEUIL_MIN})")
if manquants:
    print(f"SANS CORRECTION ({len(manquants)}) :")
    for lang, title in manquants:
        print(f"  - {lang} / {title}")
if probs:
    print(f"PROBLEMES ({len(probs)}) :")
    for p in probs:
        print(f"  - {p}")
if total_lots != solutions.coverage():
    print(f"ATTENTION : fusion != somme des lots "
          f"({solutions.coverage()} vs {total_lots})")

ok = not probs and not manquants and total_lots == solutions.coverage()
print("RESULTAT :", "OK" if ok else "PROBLEMES")
sys.exit(0 if ok else 1)
