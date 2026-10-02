"""Corrections commentées des exercices (onglet Correction).

Contenu rédigé par exercice du curriculum, structuré en texte brut :
SOLUTION (code complet commenté) / EXPLICATION / POINTS DE VÉRIFICATION /
POUR ALLER PLUS LOIN. Clé : SOLUTIONS[langage]["exercises"][titre exact] —
le titre est la référence humaine du curriculum ; un repli générique
couvre tout titre manquant (dérive éventuelle après réécriture d'une
liste d'exercices).

Les lots solutions_1 … solutions_5 sont fusionnés à l'import.
"""
from __future__ import annotations

from typing import Dict

from core.solutions_1 import CONTENT as _LOT1
from core.solutions_2 import CONTENT as _LOT2
from core.solutions_3 import CONTENT as _LOT3
from core.solutions_4 import CONTENT as _LOT4
from core.solutions_5 import CONTENT as _LOT5

SOLUTIONS: Dict[str, Dict[str, Dict[str, str]]] = {}
for _lot in (_LOT1, _LOT2, _LOT3, _LOT4, _LOT5):
    for _lang, _kinds in _lot.items():
        _bucket = SOLUTIONS.setdefault(_lang, {})
        for _kind, _fiches in _kinds.items():
            _bucket.setdefault(_kind, {}).update(_fiches)

_FALLBACK = """CORRECTION EN PRÉPARATION

La correction commentée de cet exercice est en cours de rédaction.

En attendant, revenez à la fiche de l'exercice (onglet Formation) :
ses étapes et son indice suffisent souvent pour trouver la solution.
Cette page affichera ensuite le code complet accompagné de son
explication et de ses points de vérification."""


def has_solution(lang: str, title: str) -> bool:
    """Vrai si une correction existe pour cet exercice du curriculum."""
    return title in SOLUTIONS.get(lang, {}).get("exercises", {})


def solution_for(lang: str, title: str) -> str:
    """Texte de la correction ; repli générique si le titre est inconnu."""
    return SOLUTIONS.get(lang, {}).get("exercises", {}).get(title, _FALLBACK)


def missing() -> "list[tuple[str, str]]":
    """Exercices du curriculum sans correction : [(langage, titre)]."""
    from core import curriculum

    out = []
    for lang in curriculum.langs():
        for _slug, title, _desc in curriculum.items(lang, "exercises"):
            if not has_solution(lang, title):
                out.append((lang, title))
    return out


def coverage() -> int:
    """Nombre total de corrections rédigées (tous langages confondus)."""
    return sum(len(kinds.get("exercises", {})) for kinds in SOLUTIONS.values())
