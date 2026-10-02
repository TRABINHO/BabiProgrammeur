"""Écran d'accueil de BabiProgrammeur.

Fond de nombres binaires verts qui défilent (style pluie Matrix), logo de
l'application pulsé au centre sur une plaque sombre, puis fondu de sortie.
Remplace le splash par défaut de Kivy au démarrage — voir main.on_start.
"""
from __future__ import annotations

import os
import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "assets", "icon.png")

DUREE = 1.2     # secondes d'animation avant le fondu
FONDU = 0.45    # durée du fondu
LIGNES = 80     # lignes de chiffres par colonne (doit couvrir la fenêtre)
TAILLE_LOGO = dp(150)

# verts du « plateau » : les colonnes piochent dedans
VERTS = [
    (0.05, 0.30, 0.12, 0.55),
    (0.10, 0.55, 0.22, 0.80),
    (0.25, 0.95, 0.45, 1.00),
    (0.06, 0.42, 0.17, 0.65),
    (0.15, 0.75, 0.30, 0.90),
]


def _binaire() -> str:
    """Colonne de LIGNES chiffres 0/1, un par ligne."""
    return "\n".join(random.choice("01") for _ in range(LIGNES))


class SplashScreen(Widget):
    """Overlay plein écran posé sur la fenêtre pendant le démarrage.

    Inerte côté toucher : aucun enfant ne grabbe le pointeur, les appuis
    traversent vers l'application en dessous.
    """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.pos = (0, 0)
        self.size = Window.size
        self._cols: list[Label] = []
        self._vits: list[float] = []
        self._events = []
        self._fini = False
        self._age = 0.0        # âge de l'écran, accumulé image par image
        self._fading = False
        self._puls = None      # pulsation du logo (annulée au retrait)
        self._fade = None      # fondu de sortie (annulé au retrait)

        with self.canvas.before:
            Color(0.01, 0.03, 0.02, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)

        # --- colonnes de chiffres (les premières ajoutées = dessinées en bas) --
        ncol = max(6, int(Window.width // dp(30)))
        pas = Window.width / ncol
        for i in range(ncol):
            col = Label(
                text=_binaire(),
                font_size=sp(16),
                color=random.choice(VERTS),
                size_hint=(None, None),
                halign="center",
            )
            col.x = i * pas + pas / 2
            col.y = random.uniform(-dp(200), 0)
            self._cols.append(col)
            self._vits.append(random.uniform(dp(90), dp(220)))
            self.add_widget(col)

        # --- plaque sombre + logo au centre -------------------------------- #
        self._plaque = Widget(size_hint=(None, None))
        with self._plaque.canvas:
            Color(0, 0, 0, 0.55)
            self._plaque_rect = RoundedRectangle(radius=[dp(24)])
        self.add_widget(self._plaque)

        self.logo = Image(
            source=LOGO,
            size=(TAILLE_LOGO, TAILLE_LOGO),
            size_hint=(None, None),
        )
        self.add_widget(self.logo)

        self._titre = Label(
            text="BabiProgrammeur",
            font_size=sp(22),
            bold=True,
            color=(0.85, 1.0, 0.90, 1),
            size_hint=(None, None),
        )
        self.add_widget(self._titre)

        self._recalc()
        self.bind(size=self._on_resize, pos=self._on_resize)
        self.bind(opacity=self._sur_opacite)
        self.logo.bind(size=self._on_logo, center=self._on_logo)

    # ------------------------------------------------------------------ #
    def _recalc(self) -> None:
        """Dimensions/positions de base selon la fenêtre courante."""
        w, h = self.size
        ncol = len(self._cols)
        pas = w / max(ncol, 1)
        for i, col in enumerate(self._cols):
            col.x = i * pas + pas / 2
            hauteur = col.texture.height if col.texture else dp(LIGNES * 22)
            # le haut de la colonne dépasse la fenêtre : on borne le
            # défilement pour que [y ; y+hauteur] couvre toujours [0 ; h]
            col.y = min(col.y, 0.0)
            if col.y + hauteur < h:
                col.y = h - hauteur
        self.logo.center = (w / 2, h / 2 + dp(14))
        # la LARGEUR d'abord : `center` est calculé depuis la largeur courante,
        # la définir après laisserait la boîte décalée (centre = w - w0/2).
        # Sur téléphone aucune correction ne vient plus tard : sans cet ordre
        # le titre reste aligné à droite pendant tout le splash.
        self._titre.width = w
        self._titre.center = (w / 2, h / 2 - TAILLE_LOGO / 2 - dp(22))
        self._on_logo()

    def _on_resize(self, *_args) -> None:
        self._bg.pos = self.pos
        self._bg.size = self.size
        w, h = self.size
        ncol = len(self._cols)
        pas = w / max(ncol, 1)
        for i, col in enumerate(self._cols):
            col.x = i * pas + pas / 2
        self.logo.center = (w / 2, h / 2 + dp(14))
        self._titre.width = w
        self._titre.center = (w / 2, h / 2 - TAILLE_LOGO / 2 - dp(22))

    def _on_logo(self, *_args) -> None:
        # La pulsation anime `size` avec un coin fixe : le centre dériverait
        # de ±5 px et l'icône se désalignerait du titre « pendant l'animation ».
        # On recalcule donc le centre de l'icône sur la fenêtre à chaque pas.
        self.logo.center = (self.width / 2, self.height / 2 + dp(14))
        self._plaque.center = self.logo.center
        self._plaque.size = (self.logo.width + dp(36), self.logo.height + dp(36))
        self._plaque_rect.pos = self._plaque.pos
        self._plaque_rect.size = self._plaque.size

    # ------------------------------------------------------------------ #
    def _step(self, dt: float) -> None:
        """Moteur image par image : pluie binaire ET cycle de vie.

        L'âge est accumulé ici plutôt que par schedule_once : les rappels
        planifiés avant la première image partagent une origine erronée (la
        création de l'horloge) et pourraient tomber dans la même image.
        """
        dt = min(dt, 0.1)   # première image très lente : ne pas exploser l'âge
        self._age += dt
        h = self.height
        for col, v in zip(self._cols, self._vits):
            col.y -= v * dt
            hauteur = col.texture.height if col.texture else dp(LIGNES * 22)
            if col.y + hauteur < h:
                col.y = 0.0
        if not self._fading and self._age >= DUREE:
            self._fading = True
            self._fade = Animation(opacity=0.0, duration=FONDU)
            self._fade.start(self)
        if self._age >= DUREE + FONDU + 0.3:
            self.arreter()

    def _twinkle(self, _dt: float) -> None:
        """Régénère les chiffres de quelques colonnes : scintillement discret."""
        for col in self._cols:
            if random.random() < 0.34:
                col.text = _binaire()
                col.color = random.choice(VERTS)

    # ------------------------------------------------------------------ #
    def start(self) -> None:
        """Démarre l'animation ; le cycle de vie est piloté par _step."""
        self._events.append(Clock.schedule_interval(self._step, 0))
        self._events.append(Clock.schedule_interval(self._twinkle, 0.25))
        # pulsation douce du logo (aller-retour)
        puls = (Animation(size=(TAILLE_LOGO * 1.05, TAILLE_LOGO * 1.05),
                          duration=0.7, t="in_out_sine")
                + Animation(size=(TAILLE_LOGO, TAILLE_LOGO),
                            duration=0.7, t="in_out_sine"))
        puls.repeat = True
        self._puls = puls
        puls.start(self.logo)

    def _sur_opacite(self, _instance, value: float) -> None:
        if value <= 0.0:
            self.arreter()

    def arreter(self) -> None:
        """Annule les animations/horloges et retire l'overlay de la fenêtre."""
        if self._fini:
            return
        self._fini = True
        if self._puls is not None:
            self._puls.cancel(self.logo)
            self._puls = None
        if self._fade is not None:
            self._fade.cancel(self)
            self._fade = None
        for ev in self._events:
            ev.cancel()
        self._events.clear()
        Clock.unschedule(self._twinkle)
        if self.parent is not None:
            self.parent.remove_widget(self)


def show_splash() -> SplashScreen:
    """Pose l'écran d'accueil au-dessus de tout et lance son animation."""
    splash = SplashScreen()
    Window.add_widget(splash)
    splash.start()
    return splash
