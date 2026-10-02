"""Alignement du titre de l'ecran d'accueil : logo et titre co-centres.

    python tests/probe_splash_center.py

Deux phases :
  A. splash reel de l'application a 0,5 s (avec la pulsation en cours) ;
  B. splash FRAIS cree quand la fenetre est stable (cas du telephone : aucun
     evenement de resize ne viendra corriger une position fausse).
BABI_SPLASH volontairement non defini : le splash doit s'afficher.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402

PROBLEMES: list[str] = []
INFOS: list[str] = []
AGE = [0.0]
PHASE = {"b": False}


def _controle(prefixe: str, sp, cx: float, cy: float, tol: float = 1.5) -> None:
    """Verifie co-centrage horizontal + titre sous la plaque (coords Kivy)."""
    titre = sp._titre
    tex_h = titre.texture_size[1] if titre.texture_size else 0
    INFOS.append(
        f"{prefixe} titre ctr=({titre.center_x:.1f},{titre.center_y:.1f}) "
        f"box={titre.width:.0f}x{titre.height:.0f} tex={titre.texture_size} | "
        f"logo ctr=({sp.logo.center_x:.1f},{sp.logo.center_y:.1f}) "
        f"centre_attendu=({cx:.1f},{cy:.1f})"
    )
    # 1) titre centre horizontalement sur la fenetre
    ecart_t = titre.center_x - cx
    if abs(ecart_t) > tol:
        PROBLEMES.append(
            f"{prefixe} titre decale de {ecart_t:+.1f}px "
            f"(centre {titre.center_x:.1f} vs {cx:.1f})"
        )
    # 2) logo centre horizontalement (la pulsation ne doit pas le faire
    #    derivement : il doit rester aligne sous le titre)
    ecart_l = sp.logo.center_x - cx
    if abs(ecart_l) > tol:
        PROBLEMES.append(
            f"{prefixe} logo derive de {ecart_l:+.1f}px "
            f"(centre {sp.logo.center_x:.1f} vs {cx:.1f})"
        )
    # 3) le texte visible (texture) passe SOUS la plaque
    if tex_h:
        from kivy.metrics import dp

        haut_texte = titre.center_y + tex_h / 2          # bord haut (Kivy, y croit)
        bas_plaque = sp.logo.y - dp(36) / 2              # plaque = logo + 36dp
        if haut_texte > bas_plaque + 1.5:
            PROBLEMES.append(
                f"{prefixe} titre CHEVAUCHE la plaque "
                f"(haut texte {haut_texte:.1f} > bas plaque {bas_plaque:.1f})"
            )
    # 4) le titre tient dans la largeur de la fenetre
    if titre.texture_size and titre.texture_size[0] > cx * 2 + 1.5:
        PROBLEMES.append(
            f"{prefixe} titre plus large que la fenetre "
            f"({titre.texture_size[0]:.0f} > {cx * 2:.0f})"
        )


def phase_a(_dt: float) -> None:
    """Mesure le splash reel a 0,5 s d'age (pulsation en cours)."""
    AGE[0] += min(_dt, 0.1)
    if AGE[0] < 0.5 or PHASE["b"]:
        return
    from kivy.core.window import Window

    splash = [w for w in Window.children if type(w).__name__ == "SplashScreen"]
    if not splash:
        PROBLEMES.append("splash absent de la fenetre a 0,5 s")
        print_resultat()
        app.stop()
        return False
    PHASE["b"] = True
    _controle("A (0,5s, pulsation):", splash[0],
              Window.width / 2, Window.height / 2)

    # --- phase B : splash frais, fenetre stable (cas telephone) -------------
    from ui.splash import SplashScreen

    frais = SplashScreen()
    _controle("B (frais, sans resize):", frais,
              Window.width / 2, Window.height / 2)
    try:
        frais.arreter()
    except Exception:  # noqa: BLE001 — jamais ajoute a la fenetre
        pass

    print_resultat()
    app.stop()
    return False


def print_resultat() -> None:
    print("\n".join(INFOS))
    print("-" * 60)
    if PROBLEMES:
        print("PROBLEMES D'ALIGNEMENT (splash) :")
        for p in PROBLEMES:
            print("  -", p)
    else:
        print("SPLASH CENTRE : AUCUN PROBLEME")


def partir(_dt: float) -> None:
    """Planifie en on_start : meme origine horloge que le splash."""
    Clock.schedule_interval(phase_a, 0)


from main import BabiProgrammeur  # noqa: E402

app = BabiProgrammeur()
app.bind(on_start=lambda *_a: partir(0))
app.run()
sys.exit(1 if PROBLEMES else 0)
