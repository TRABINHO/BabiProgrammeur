"""Palette de couleurs commune à toute l'interface.

Thème sombre inspiré de SoloLearn : fond navy profond, cartes bleu-nuit,
bleu primaire #2EA7FF pour les actions et accents, couleurs vives réservées
aux données (progression, langages).
"""

BG = (0.047, 0.067, 0.110, 1.0)      # #0C111C fond général (navy profond)
BG_ALT = (0.067, 0.094, 0.153, 1.0)  # #111827 fond des barres / alterné
CARD = (0.106, 0.145, 0.220, 1.0)    # #1B2538 cartes
CARD_HI = (0.145, 0.192, 0.282, 1.0)  # #25314A cartes surélevées / sélectionnées

LINE = (0.204, 0.255, 0.349, 1.0)    # #344159 séparateurs

TEXT = (0.949, 0.961, 0.980, 1.0)    # #F2F5FA texte principal
MUTED = (0.600, 0.659, 0.753, 1.0)   # #99A8C0 texte secondaire
FAINT = (0.380, 0.435, 0.533, 1.0)   # #61708A texte très discret

ACCENT = (0.180, 0.655, 1.000, 1.0)  # #2EA7FF bleu SoloLearn (actions)
ACCENT_DIM = (0.180, 0.655, 1.000, 0.35)
GREEN = (0.298, 0.851, 0.392, 1.0)   # #4CD964 objectif atteint
ORANGE = (1.000, 0.651, 0.188, 1.0)  # #FFA630 en cours / alerte
RED = (1.000, 0.353, 0.373, 1.0)     # #FF5A5F erreur / suppression

# Nuances utilisées pour les barres et les langages
SERIES = [
    ACCENT,
    GREEN,
    ORANGE,
    (0.640, 0.470, 0.980, 1.0),
    (0.980, 0.400, 0.640, 1.0),
    (0.200, 0.820, 0.850, 1.0),
    (0.980, 0.840, 0.300, 1.0),
    (0.550, 0.640, 0.760, 1.0),
]


def series_color(index: int) -> tuple:
    return SERIES[index % len(SERIES)]


# --------------------------------------------------------------------------- #
# Couleur unique de chaque langage (barres de répartition, progression et
# puces de sélection). Teintes distinctes : deux langages voisins dans la
# barre de puces sont fortement contrastés, et toutes se lisent sur fond
# sombre. Une couleur par langage, jamais réutilisée.
# --------------------------------------------------------------------------- #
LANG_COLORS = {
    "Python":     (0.235, 0.600, 0.949, 1.0),  # bleu ciel
    "JavaScript": (0.961, 0.851, 0.157, 1.0),  # jaune
    "TypeScript": (0.306, 0.361, 0.898, 1.0),  # bleu roi
    "Java":       (0.941, 0.290, 0.290, 1.0),  # rouge
    "C++":        (0.114, 0.749, 0.827, 1.0),  # cyan
    "C#":         (0.769, 0.408, 0.851, 1.0),  # magenta
    "Go":         (0.122, 0.827, 0.624, 1.0),  # menthe
    "Rust":       (0.949, 0.435, 0.235, 1.0),  # orange brique
    "SQL":        (0.294, 0.784, 0.333, 1.0),  # vert
    "HTML/CSS":   (0.969, 0.588, 0.235, 1.0),  # orange ambré
    "PHP":        (0.557, 0.588, 0.831, 1.0),  # indigo doux
    "Swift":      (1.000, 0.404, 0.478, 1.0),  # corail rosé
    "Kotlin":     (0.663, 0.361, 1.000, 1.0),  # violet vif
    "Flutter":    (0.290, 0.788, 0.949, 1.0),  # azur clair
    "Autre":      (0.604, 0.663, 0.741, 1.0),  # gris bleuté
}


def lang_color(name: str) -> tuple:
    """Couleur unique d'un langage. Repli haché sur les 8 nuances pour les
    noms libres (noms de projets dans les répartitions)."""
    if name in LANG_COLORS:
        return LANG_COLORS[name]
    return series_color(sum(ord(c) for c in name) % len(SERIES))


def luminance(color) -> float:
    """Luminance relative approximative (0..1), pour choisir un texte lisible."""
    return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]


def chip_bg(accent, active: bool) -> list:
    """Fond d'une puce : couleur pleine si sélectionnée, sinon la couleur du
    langage à 30 % sur le fond sombre — la teinte reste visible même au repos."""
    if active:
        return [accent[0], accent[1], accent[2], 1.0]
    return [
        accent[0] * 0.30 + BG[0] * 0.70,
        accent[1] * 0.30 + BG[1] * 0.70,
        accent[2] * 0.30 + BG[2] * 0.70,
        1.0,
    ]


def text_on(bg) -> tuple:
    """Noir ou blanc, selon ce qui se lit le mieux sur ce fond (un seul
    regard suffit : pas de texte gris sur couleur)."""
    return (0.0, 0.0, 0.0, 1.0) if luminance(bg) > 0.18 else (1.0, 1.0, 1.0, 1.0)
