"""BabiProgrammeur — application mobile de suivi d'activité de programmation.

Lancement :
    python main.py            # démarrage normal
    python main.py --demo     # injecte des données de démonstration
"""
from __future__ import annotations

import os
import sys

# Kivy analyse argv au moment de l'import : on retire nos propres options.
DEMO_MODE = "--demo" in sys.argv
if DEMO_MODE:
    sys.argv = [a for a in sys.argv if a != "--demo"]

# Onglet ouvert au démarrage (utilitaire de test : --tab stats)
START_TAB = None
if "--tab" in sys.argv:
    _i = sys.argv.index("--tab")
    START_TAB = sys.argv[_i + 1] if _i + 1 < len(sys.argv) else None
    del sys.argv[_i:_i + 2]

from datetime import datetime

from kivy.clock import Clock
from kivy.metrics import Metrics, dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp


def ensure_readable_metrics(*_args) -> None:
    """DPI remonté à 0 par la plateforme (fenêtre masquée, pilote exotique,
    session distante...) rendrait dp(0) et ferait planter KivyMD au premier
    trait : on pose des valeurs raisonnables par défaut."""
    if Metrics.dpi <= 0:
        Metrics.dpi = 96.0
    if Metrics.density <= 0:
        Metrics.density = 1.0
    if Metrics.fontscale <= 0:
        Metrics.fontscale = 1.0

from core import notify as notifier
from core import stats as st
from core.seed import seed
from core.storage import SessionStore
from ui import colors
from ui.screens import (CorrectionScreen, GoalsScreen, HistoryScreen,
                         LearningScreen, StatsScreen, TimerScreen)
from ui.widgets import NavButton


def install_fonts() -> None:
    """Fira Sans (SIL OFL, dépôt mozilla/Fira) en place de Roboto.

    Le slot « Roboto » est réenregistré sur nos fichiers TTF : tous les
    libellés par défaut — application et KivyMD — basculent sur Fira Sans,
    la police de SoloLearn, sans toucher aux milliers de Label existants.
    En cas de pépin (fichier absent…), l'application reste en Roboto.
    """
    try:
        from kivy.core.text import LabelBase

        base = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "assets", "fonts"
        )
        for name in ("Roboto", "Fira Sans"):
            LabelBase.register(
                name=name,
                fn_regular=os.path.join(base, "FiraSans-Regular.ttf"),
                fn_bold=os.path.join(base, "FiraSans-Bold.ttf"),
                fn_italic=os.path.join(base, "FiraSans-Italic.ttf"),
                fn_bolditalic=os.path.join(base, "FiraSans-BoldItalic.ttf"),
            )
    except Exception:
        pass


TABS = [
    ("timer", "Suivi"),
    ("stats", "Stats"),
    ("learn", "Formation"),
    ("corrections", "Correction"),
    ("goals", "Objectifs"),
    ("history", "Historique"),
]


class BabiProgrammeur(MDApp):
    def build(self):
        install_fonts()
        ensure_readable_metrics()
        from kivy.core.window import Window

        Window.bind(dpi=ensure_readable_metrics)
        self.title = "BabiProgrammeur"
        # Logo « Babi Programmez » : icône de la fenêtre / barre des tâches
        # (Kivy l'applique via Window.set_icon) et référence du projet.
        self.icon = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png"
        )
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.disabled_alpha = "0.5"
        # Fond de fenêtre de la palette (navy SoloLearn) : KivyMD impose le
        # sien au changement de thème (#121212), puis LE REPASSE au premier
        # tick (Clock.schedule_once de son ThemeManager.__init__). On
        # verrouille la valeur par une liaison auto-limitée sur clearcolor :
        # toute tentative étrangère est annulée dans la foulée.
        Window.clearcolor = colors.BG

        def _keep_bg(*_):
            if tuple(Window.clearcolor) != tuple(colors.BG):
                Window.clearcolor = colors.BG

        Window.bind(clearcolor=_keep_bg)

        if platform not in ("android", "ios"):
            # Fenêtre « format téléphone » ; on la cale en haut à gauche pour
            # rester visible même sur un écran de faible hauteur.
            Window.size = (390, 760)
            Window.left = 80
            Window.top = 45

        self.store = SessionStore()
        if DEMO_MODE and not self.store.sessions:
            seed(self.store)

        root = BoxLayout(orientation="vertical")
        # Conteneur racine + compteur de retentes pour apply_system_insets.
        self.root_box = root
        self._insets_tries = 0

        # ---------------------------------------------------------- #
        # Barre d'état
        # ---------------------------------------------------------- #
        header = BoxLayout(size_hint_y=None, height=dp(54),
                           padding=(dp(16), dp(3)), spacing=dp(2),
                           orientation="vertical")
        # Bandeau bleu SoloLearn (#2EA7FF) : titre blanc, date à 88 %.
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle

            Color(*colors.ACCENT)
            Rectangle(pos=header.pos, size=header.size)
        header.bind(
            pos=lambda *_: None,
            size=lambda *_: None,
        )
        # redessin simple du fond
        def _draw_header(*_):
            header.canvas.before.clear()
            with header.canvas.before:
                Color(*colors.ACCENT)
                Rectangle(pos=header.pos, size=header.size)

        header.bind(pos=_draw_header, size=_draw_header)

        # titre pleine largeur, toujours sur UNE ligne (au sommet de l'app)
        title = Label(
            text="BabiProgrammeur",
            font_size=sp(19),
            bold=True,
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
            size_hint_y=0.58,
            max_lines=1,
            shorten=True,
            shorten_from="right",
        )
        title.bind(size=lambda l, s: setattr(l, "text_size", (s[0], None)))
        header.add_widget(title)

        self.today_lbl = Label(
            text="",
            font_size=sp(12),
            color=(1, 1, 1, 0.88),
            halign="right",
            valign="middle",
            size_hint_y=0.42,
            shorten=True,
        )
        self.today_lbl.bind(size=lambda l, s: setattr(l, "text_size", (s[0], None)))
        header.add_widget(self.today_lbl)
        root.add_widget(header)

        # ---------------------------------------------------------- #
        # Écrans
        # ---------------------------------------------------------- #
        self.screens = {
            "timer": TimerScreen(self, name="timer"),
            "stats": StatsScreen(self, name="stats"),
            "learn": LearningScreen(self, name="learn"),
            "corrections": CorrectionScreen(self, name="corrections"),
            "goals": GoalsScreen(self, name="goals"),
            "history": HistoryScreen(self, name="history"),
        }
        self.sm = ScreenManager()
        for screen in self.screens.values():
            self.sm.add_widget(screen)
        root.add_widget(self.sm)

        # ---------------------------------------------------------- #
        # Navigation du bas
        # ---------------------------------------------------------- #
        nav = BoxLayout(size_hint_y=None, height=dp(62))
        self.nav_buttons = {}
        for key, label in TABS:
            btn = NavButton(text=label)
            btn.bind(on_release=lambda _b, k=key: self.switch_tab(k))
            self.nav_buttons[key] = btn
            nav.add_widget(btn)

        def _draw_nav(*_):
            nav.canvas.before.clear()
            with nav.canvas.before:
                Color(*colors.BG_ALT)
                Rectangle(pos=nav.pos, size=nav.size)
                Color(*colors.LINE)
                Rectangle(pos=(nav.x, nav.top - dp(1)), size=(nav.width, dp(1)))

        nav.bind(pos=_draw_nav, size=_draw_nav)
        _draw_nav()
        root.add_widget(nav)

        # ---------------------------------------------------------- #
        # Boucles
        # ---------------------------------------------------------- #
        Clock.schedule_interval(self._tick, 1.0)
        Clock.schedule_interval(self._check_reminder, 20.0)

        self.switch_tab(START_TAB if START_TAB in self.screens else "timer")
        self.refresh_chrome()
        return root

    # ------------------------------------------------------------------ #
    def switch_tab(self, key: str) -> None:
        self.sm.current = key
        for name, btn in self.nav_buttons.items():
            btn.set_active(name == key)
        screen = self.screens.get(key)
        if screen:
            screen.refresh()

    def refresh_chrome(self) -> None:
        today = st.seconds_today(self.store.sessions)
        goal = int(self.store.goals.get("daily_minutes", 0)) * 60
        if goal:
            self.today_lbl.text = f"Aujourd'hui  {st.format_duration(today)}  ({today / goal:.0%})"
        else:
            self.today_lbl.text = f"Aujourd'hui  {st.format_duration(today)}"

    # ------------------------------------------------------------------ #
    def _tick(self, _dt: float) -> None:
        self.screens["timer"].tick()
        if datetime.now().second % 10 == 0:
            self.refresh_chrome()

    def _check_reminder(self, _dt: float) -> None:
        settings = self.store.settings
        if not settings.get("reminder_enabled"):
            return
        now = datetime.now()
        today_key = now.strftime("%Y-%m-%d")
        if settings.get("last_reminder_day") == today_key:
            return
        if now.strftime("%H:%M") != settings.get("reminder_time", "20:00"):
            return
        notifier.notify("BabiProgrammeur", "Temps de coder ! Votre session de ce jour vous attend.")
        self.store.set_settings(last_reminder_day=today_key)

    # ------------------------------------------------------------------ #
    def apply_system_insets(self, *_args) -> None:
        """Réserve la place des barres système (Android 15+, API 35+).

        Avec une cible 35 ou plus, Android dessine l'application bord à
        bord : la barre d'état OS recouvre notre en-tête et la barre de
        navigation nos onglets du bas. On padde le conteneur racine de la
        hauteur réelle des insets — la mise en page reste alors identique
        à la version fenêtrée actuelle. Hors Android 15+, rien ne bouge.
        """
        if platform != "android" or not getattr(self, "root_box", None):
            return
        try:
            from jnius import autoclass

            if int(autoclass("android.os.Build$VERSION").SDK_INT) < 35:
                return
            from android import mActivity

            insets = mActivity.getWindow().getDecorView().getRootWindowInsets()
            top = bottom = 0
            if insets is not None:
                try:
                    wint = autoclass("android.view.WindowInsets$Type")
                    box = insets.getInsets(wint.systemBars())
                    top, bottom = int(box.top), int(box.bottom)
                except Exception:
                    # Repli sur l'API d'origine (deprecated mais vivante).
                    top = int(insets.getSystemWindowInsetTop())
                    bottom = int(insets.getSystemWindowInsetBottom())
            if top or bottom:
                # VariableListProperty : [gauche, haut, droite, bas].
                self.root_box.padding = [0, top, 0, bottom]
                return
        except Exception:
            return
        # Insets pas encore fournies (fenêtre pas encore posée) : on retente.
        self._insets_tries = getattr(self, "_insets_tries", 0) + 1
        if self._insets_tries <= 10:
            Clock.schedule_once(self.apply_system_insets, 0.5)

    def on_start(self) -> None:
        # Android 15+ : décalage de l'UI sous les barres système
        # (edge-to-edge) — deux amorces, plus les retentes internes.
        Clock.schedule_once(self.apply_system_insets, 0)
        Clock.schedule_once(self.apply_system_insets, 1.0)
        for screen in self.screens.values():
            screen.refresh()
        # Écran d'accueil : logo au centre sur fond de binaire vert qui
        # défile — désactivable pour les tests avec BABI_SPLASH=0.
        if os.environ.get("BABI_SPLASH", "1") != "0":
            from ui.splash import show_splash

            show_splash()

    def on_stop(self) -> None:
        self.store.save()

    def on_pause(self) -> bool:
        self.store.save()
        return True

    def on_resume(self) -> None:
        for screen in self.screens.values():
            screen.refresh()


if __name__ == "__main__":
    BabiProgrammeur().run()
