"""Fiches détaillées des cours et exercices (onglet Formation).

Contenu rédigé par élément du curriculum, structuré en texte brut :
en-têtes en capitales (OBJECTIFS / POINTS CLÉS / EXEMPLE pour les cours,
ÉNONCÉ / ÉTAPES / RÉSULTAT ATTENDU / INDICE pour les exercices).
Clé : CONTENT[langage][kind][titre exact] — le titre est la référence
humaine du curriculum ; un repli générique couvre tout titre manquant
(dérive éventuelle après réécriture d'une liste de cours).

Les lots content_1 … content_5 sont fusionnés à l'import.
"""
from __future__ import annotations

from typing import Dict

from core.content_1 import CONTENT as _LOT1
from core.content_2 import CONTENT as _LOT2
from core.content_3 import CONTENT as _LOT3
from core.content_4 import CONTENT as _LOT4
from core.content_5 import CONTENT as _LOT5

CONTENT: Dict[str, Dict[str, Dict[str, str]]] = {}
for _lot in (_LOT1, _LOT2, _LOT3, _LOT4, _LOT5):
    for _lang, _kinds in _lot.items():
        _bucket = CONTENT.setdefault(_lang, {})
        for _kind, _fiches in _kinds.items():
            _bucket.setdefault(_kind, {}).update(_fiches)

_FALLBACK = """FICHE EN PRÉPARATION

Le contenu détaillé de cet élément sera ajouté prochainement.

En attendant, le résumé de la ligne donne l'essentiel :
relisez-le et essayez d'appliquer la notion dans un petit
programme de votre côté."""


def has_content(lang: str, kind: str, title: str) -> bool:
    """Vrai si une fiche existe pour cet élément du curriculum."""
    return title in CONTENT.get(lang, {}).get(kind, {})


def content_for(lang: str, kind: str, title: str) -> str:
    """Texte de la fiche ; repli générique si le titre est inconnu."""
    return CONTENT.get(lang, {}).get(kind, {}).get(title, _FALLBACK)


def missing() -> "list[tuple[str, str, str]]":
    """Éléments du curriculum sans fiche : [(langage, kind, titre)]."""
    from core import curriculum

    out = []
    for lang in curriculum.langs():
        for kind in ("lessons", "exercises"):
            for _slug, title, _desc in curriculum.items(lang, kind):
                if not has_content(lang, kind, title):
                    out.append((lang, kind, title))
    return out


def coverage() -> int:
    """Nombre total de fiches rédigées (tous langages confondus)."""
    return sum(
        len(kinds.get(kind, {}))
        for kinds in CONTENT.values()
        for kind in ("lessons", "exercises")
    )
