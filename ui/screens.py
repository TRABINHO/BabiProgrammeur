"""Les six écrans de BabiProgrammeur."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import List, Tuple

from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from core import content
from core import curriculum
from core import export as exporter
from core import solutions
from core import stats as st
from core import notify as notifier
from core.models import Session
from ui import colors
from ui.dialogs import ContentFiche, confirm, show_message
from ui.widgets import (BarChart, BarRow, Card, CheckRow, Chip, LineChart,
                         LinkRow, RingWidget, StatTile)

# Langages proposés (identiques à ceux du parcours cours/exercices).
LANGUAGES = curriculum.LANGUAGES


# --------------------------------------------------------------------------- #
# Utilitaires d'interface
# --------------------------------------------------------------------------- #
def section(text: str) -> Label:
    lbl = Label(
        text=text.upper(),
        font_size=sp(11),
        bold=True,
        color=colors.ACCENT,
        size_hint_y=None,
        height=dp(22),
        halign="left",
    )
    lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
    return lbl


def hard_bounds(sv: ScrollView) -> ScrollView:
    """Reborde scroll_x/scroll_y dans [0, 1] quoi qu'il arrive.

    Au relâchement d'un glisser rapide, l'inertie de l'effet peut faire
    dériver le défilement bien en dessous de 0 : du vide sous le contenu,
    et la molette « vers le bas » devient sans effet (bornée à 0) —
    d'où l'impression d'un défilement bloqué. On reborde immédiatement et
    on resynchronise l'effet pour stopper la dérive.
    """
    def _clamp(attr: str, eff_attr: str):
        def _on(s: ScrollView, value: float) -> None:
            if 0.0 <= value <= 1.0:
                return
            c = 0.0 if value < 0.0 else 1.0
            setattr(s, attr, c)
            eff = getattr(s, eff_attr, None)
            if eff is not None and not getattr(eff, "is_manual", False):
                # même formule que _update_effect_y_bounds (value = max * scroll)
                eff.reset(eff.max * c)
        sv.bind(**{attr: _on})

    _clamp("scroll_y", "effect_y")
    _clamp("scroll_x", "effect_x")
    return sv


def scroll_column(spacing=dp(12), padding=dp(16)) -> Tuple[ScrollView, BoxLayout]:
    # pos_hint obligatoire : Screen hérite de FloatLayout qui ne positionne
    # ses enfants que s'ils portent un pos_hint.
    # - scroll_type ["bars", "content"] : la barre visible est un vrai curseur
    #   prenable (sinon seul le glisser du contenu fonctionnait) ;
    # - always_overscroll False : le défilement reste borné [0, 1], on ne peut
    #   plus se coincer en dessous du bas (du vide + molette bloquée).
    sv = ScrollView(do_scroll_x=False, bar_width=dp(6), bar_color=colors.LINE,
                    pos_hint={"x": 0, "y": 0},
                    scroll_type=["bars", "content"], always_overscroll=False)
    hard_bounds(sv)
    col = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=spacing,
        padding=padding,
    )
    col.bind(minimum_height=col.setter("height"))
    sv.add_widget(col)
    return sv, col


def small_label(text="", color=None, size=12, bold=False, height=None) -> Label:
    lbl = Label(
        text=text,
        font_size=sp(size),
        bold=bold,
        color=color or colors.TEXT,
        size_hint_y=None,
        height=height or dp(18),
        halign="left",
        valign="middle",
    )
    lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
    return lbl


def make_card(*widgets, spacing=dp(10)) -> Card:
    card = Card(spacing=spacing)
    for w in widgets:
        card.add_widget(w)
    return card


def primary_button(text, on_release=None, disabled=False) -> MDRaisedButton:
    btn = MDRaisedButton(
        text=text,
        size_hint_y=None,
        height=dp(46),
        font_size=sp(14),
        disabled=disabled,
    )
    if on_release:
        btn.bind(on_release=on_release)
    return btn


def ghost_button(text, on_release=None) -> MDRaisedButton:
    btn = MDRaisedButton(
        text=text,
        size_hint_y=None,
        height=dp(46),
        font_size=sp(14),
        md_bg_color=colors.CARD_HI,
        text_color=colors.TEXT,
    )
    if on_release:
        btn.bind(on_release=on_release)
    return btn


def lang_color(name: str) -> tuple:
    """Couleur exclusive d'un langage (délègue à ui.colors.LANG_COLORS)."""
    return colors.lang_color(name)


# --------------------------------------------------------------------------- #
class BaseScreen(Screen):
    app = ObjectProperty(None)

    def store(self):
        return self.app.store

    def refresh(self) -> None:  # à surcharger
        pass


# =========================================================================== #
# 1. Suivi / chronomètre
# =========================================================================== #
class TimerScreen(BaseScreen):
    def __init__(self, app, **kw):
        self.app = app
        super().__init__(**kw)
        self._save_ev = None
        self._build()

    # ------------------------------------------------------------------ #
    def _build(self) -> None:
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12),
                         pos_hint={"x": 0, "y": 0})

        # --- chrono ---------------------------------------------------- #
        chrono = Card(spacing=dp(4), size_hint_y=None, height=dp(140))
        chrono.add_widget(small_label("CHRONOMÈTRE", colors.MUTED, size=11, height=dp(16)))
        self.timer_label = Label(
            text="00:00:00",
            font_size=sp(46),
            bold=True,
            color=colors.TEXT,
            size_hint_y=None,
            height=dp(62),
        )
        self.status_label = small_label("Prêt à démarrer", colors.ACCENT, size=12, height=dp(20))
        chrono.add_widget(self.timer_label)
        chrono.add_widget(self.status_label)
        root.add_widget(chrono)

        # --- formulaire ------------------------------------------------ #
        form = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))
        root.add_widget(form)

        self.project_field = MDTextField(hint_text="Nom du projet", mode="rectangle")
        self.project_field.bind(text=self._on_field_change)
        form.add_widget(self.project_field)

        # puces de langage
        chips_scroll = ScrollView(do_scroll_y=False, do_scroll_x=True, size_hint_y=None,
                                  height=dp(44), always_overscroll=False)
        hard_bounds(chips_scroll)
        chips = BoxLayout(size_hint_x=None, spacing=dp(8), padding=(0, dp(4), 0, dp(4)))
        chips.bind(minimum_width=chips.setter("width"))
        self.chips = []
        for name in LANGUAGES:
            chip = Chip(text=name, width=dp(30) + len(name) * dp(7.6), height=dp(32),
                        accent=list(colors.lang_color(name)))
            chip.bind(on_release=self._on_chip)
            self.chips.append(chip)
            chips.add_widget(chip)
        chips.add_widget(Label(size_hint_x=None, width=dp(4)))
        chips_scroll.add_widget(chips)
        form.add_widget(chips_scroll)

        self.lang_field = MDTextField(hint_text="Langage", mode="rectangle")
        self.lang_field.bind(text=self._on_field_change)
        form.add_widget(self.lang_field)

        self.notes_field = MDTextField(hint_text="Notes (optionnel)", mode="rectangle", multiline=True)
        self.notes_field.bind(text=self._on_field_change)
        form.add_widget(self.notes_field)

        # --- boutons ---------------------------------------------------- #
        btns = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(10))
        self.toggle_btn = primary_button("Démarrer", self._on_toggle)
        self.cancel_btn = ghost_button("Abandonner", self._on_cancel)
        self.cancel_btn.disabled = True
        btns.add_widget(self.toggle_btn)
        btns.add_widget(self.cancel_btn)
        root.add_widget(btns)

        # Espace flexible : le chronomètre reste collé en haut, l'astuce en bas.
        root.add_widget(Label(size_hint_y=1))

        hint = small_label(
            "Astuce : les sessions en cours sont conservées si l'application est fermée.",
            colors.FAINT, size=11, height=dp(30),
        )
        hint.valign = "top"
        root.add_widget(hint)

        self.add_widget(root)

    # ------------------------------------------------------------------ #
    def _on_chip(self, chip) -> None:
        # On ne lit JAMAIS chip.state ici : le ScrollView horizontal délivre
        # l'appui des enfants en différé et ButtonBehavior a déjà remis
        # state à 'normal' avant on_release sur un appui rapide — la
        # bascule partirait du mauvais état et déselectionnerait à chaque
        # fois. On décide d'après le champ Langage, qui porte l'état réel.
        if self.lang_field.text.strip() == chip.text:
            self.lang_field.text = ""
        else:
            self.lang_field.text = chip.text
        self._on_field_change()

    def _on_field_change(self, *_args) -> None:
        # Synchronisation puces <-> champ langage
        lang = self.lang_field.text.strip()
        for c in self.chips:
            sel = bool(lang) and c.text == lang
            c.state = "down" if sel else "normal"
            c.locked = sel  # anti-rebond : bloque le _do_release planifié
        # Sauvegarde différée si une session tourne
        if self.store().is_running and not self._save_ev:
            self._save_ev = Clock.schedule_once(self._flush_active, 1.0)

    def _flush_active(self, *_args) -> None:
        self._save_ev = None
        if self.store().is_running:
            self.store().update_active(
                project=self.project_field.text,
                language=self.lang_field.text,
                notes=self.notes_field.text,
            )

    # ------------------------------------------------------------------ #
    def _on_toggle(self, *_args) -> None:
        if self.store().is_running:
            elapsed = self.store().active_elapsed
            project = self.store().active.get("project", "") or "Sans projet"
            confirm(
                "Arrêter la session ?",
                f"{project}\nDurée : {st.format_duration(elapsed)}",
                on_yes=self._do_stop,
                yes_label="Arrêter",
            )
        else:
            project = self.project_field.text.strip()
            if not project:
                show_message("Projet manquant", "Indiquez le nom du projet à travailler.")
                return
            self.store().start(project, self.lang_field.text.strip(), self.notes_field.text.strip())
            self.refresh()
            self.app.refresh_chrome()

    def _do_stop(self) -> None:
        session = self.store().stop()
        if not session:
            return
        self.refresh()
        self.app.refresh_chrome()
        show_message(
            "Session enregistrée",
            f"{session.project or 'Sans projet'}\n"
            f"{st.format_duration(session.duration)}"
            + (f"  ·  {session.language}" if session.language else ""),
        )

    def _on_cancel(self, *_args) -> None:
        if not self.store().is_running:
            return
        confirm(
            "Abandonner la session ?",
            "Le temps écoulé ne sera pas enregistré.",
            on_yes=lambda: (self.store().cancel_active(), self.refresh(), self.app.refresh_chrome()),
            yes_label="Abandonner",
        )

    # ------------------------------------------------------------------ #
    def tick(self) -> None:
        """Appelé chaque seconde par l'application."""
        if self.store().is_running:
            self.timer_label.text = st.format_clock(self.store().active_elapsed)
            started = datetime.fromtimestamp(float(self.store().active["started_at"]))
            self.status_label.text = f"En cours depuis {started.strftime('%H:%M')}"
            self.status_label.color = colors.ORANGE
        else:
            self.timer_label.text = "00:00:00"
            self.status_label.text = "Prêt à démarrer"
            self.status_label.color = colors.ACCENT

    def refresh(self) -> None:
        running = self.store().is_running
        active = self.store().active or {}
        if running:
            self.project_field.text = active.get("project", "")
            self.lang_field.text = active.get("language", "")
            # on n'écrase pas les notes pendant la frappe
            if not self.notes_field.focus:
                self.notes_field.text = active.get("notes", "")
        for f in (self.project_field, self.lang_field):
            f.disabled = running
        self.toggle_btn.text = "Arrêter" if running else "Démarrer"
        self.cancel_btn.disabled = not running
        self.tick()


# =========================================================================== #
# 2. Statistiques
# =========================================================================== #
class StatsScreen(BaseScreen):
    def __init__(self, app, **kw):
        self.app = app
        super().__init__(**kw)
        self._build()

    def _build(self) -> None:
        sv, col = scroll_column()
        self.add_widget(sv)

        # indicateurs
        tiles = BoxLayout(size_hint_y=None, height=dp(76), spacing=dp(8))
        self.tile_today = StatTile()
        self.tile_week = StatTile()
        self.tile_streak = StatTile()
        for t in (self.tile_today, self.tile_week, self.tile_streak):
            tiles.add_widget(t)
        col.add_widget(tiles)

        # graphe 14 jours
        chart_card = Card(size_hint_y=None, height=dp(240), spacing=dp(6))
        chart_card.add_widget(small_label("14 DERNIERS JOURS", colors.ACCENT, size=11))
        self.chart = BarChart(size_hint_y=None, height=dp(180))
        chart_card.add_widget(self.chart)
        self.chart_legend = small_label("", colors.MUTED, size=11, height=dp(20))
        chart_card.add_widget(self.chart_legend)
        col.add_widget(chart_card)

        # langages
        lang_card = Card(size_hint_y=None, spacing=dp(4))
        lang_card.add_widget(small_label("LANGAGES · 30 JOURS", colors.ACCENT, size=11))
        self.lang_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
        self.lang_box.bind(minimum_height=self.lang_box.setter("height"))
        lang_card.add_widget(self.lang_box)
        lang_card.bind(minimum_height=lambda *_: setattr(lang_card, "height", lang_card.minimum_height + dp(26)))
        col.add_widget(lang_card)

        # projets
        proj_card = Card(size_hint_y=None, spacing=dp(4))
        proj_card.add_widget(small_label("TOP PROJETS", colors.ACCENT, size=11))
        self.proj_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
        self.proj_box.bind(minimum_height=self.proj_box.setter("height"))
        proj_card.add_widget(self.proj_box)
        proj_card.bind(minimum_height=lambda *_: setattr(proj_card, "height", proj_card.minimum_height + dp(26)))
        col.add_widget(proj_card)

        # évolution de l'apprentissage (cumul des cours/exercices terminés)
        learn_card = Card(size_hint_y=None, spacing=dp(6))
        learn_card.add_widget(small_label("APPRENTISSAGE · 14 JOURS", colors.ACCENT, size=11))
        self.learn_chart = LineChart(size_hint_y=None, height=dp(140))
        learn_card.add_widget(self.learn_chart)
        self.learn_legend = small_label("", colors.MUTED, size=11, height=dp(32))
        learn_card.add_widget(self.learn_legend)
        learn_card.bind(minimum_height=lambda *_: setattr(learn_card, "height", learn_card.minimum_height + dp(26)))
        col.add_widget(learn_card)

        # résumé
        summary_card = Card(size_hint_y=None, spacing=dp(6))
        summary_card.add_widget(small_label("RÉSUMÉ", colors.ACCENT, size=11))
        self.summary_lbl = Label(
            text="", font_size=sp(13), color=colors.TEXT, halign="left", valign="top",
            size_hint_y=None,
        )
        self.summary_lbl.bind(
            size=lambda l, s: (setattr(l, "text_size", s), setattr(l, "height", max(dp(60), l.texture_size[1] + dp(6))))
        )
        summary_card.add_widget(self.summary_lbl)
        summary_card.bind(minimum_height=lambda *_: setattr(summary_card, "height", summary_card.minimum_height))
        col.add_widget(summary_card)
        col.add_widget(Label(size_hint_y=None, height=dp(8)))

    def _fill_rows(self, box: BoxLayout, rows: List[Tuple[str, float]]) -> None:
        box.clear_widgets()
        if not rows:
            box.add_widget(small_label("Aucune donnée pour l'instant.", colors.FAINT, size=12))
            return
        total = max((v for _, v in rows), default=0.0) or 1.0
        for name, value in rows:
            row = BarRow(
                label=name,
                value_text=st.format_duration(value),
                fraction=value / total,
                color=list(lang_color(name)),
            )
            box.add_widget(row)

    def refresh(self) -> None:
        sessions = self.store().sessions
        goals = self.store().goals
        daily_goal = int(goals.get("daily_minutes", 0)) * 60
        weekly_goal = int(goals.get("weekly_minutes", 0)) * 60

        today = st.seconds_today(sessions)
        week = st.seconds_this_week(sessions)
        self.tile_today.set("Aujourd'hui", st.format_duration(today))
        self.tile_week.set("Cette semaine", st.format_duration(week))
        self.tile_streak.set("Série", f"{st.streak(sessions)} j")

        series = st.daily_series(sessions, 14)
        self.chart.data = [
            (d.strftime("%d"), v, d == date.today()) for d, v in series
        ]
        self.chart.target = daily_goal
        pct = (today / daily_goal * 100) if daily_goal else 0.0
        self.chart_legend.text = (
            f"Objectif quotidien : {st.format_duration(daily_goal)}  ·  aujourd'hui {pct:.0f} %"
            if daily_goal
            else "Objectif quotidien non défini"
        )

        cutoff = datetime.now().timestamp() - 30 * 86400
        last30 = [s for s in sessions if s.started_at >= cutoff]
        self._fill_rows(self.lang_box, st.totals_by_language(last30)[:7])
        self._fill_rows(self.proj_box, st.totals_by_project(sessions, limit=5))

        # évolution de l'apprentissage : cumul daté des éléments terminés
        events = self.store().learning_events()
        self.learn_chart.data = [(d.strftime("%d"), v) for d, v in st.learning_series(events, 14)]
        done_lessons, done_exercises = self.store().learning_counts()
        n_done = len(events)
        if n_done:
            plural = "s" if n_done > 1 else ""
            self.learn_legend.text = (
                f"{n_done} élément{plural} terminé{plural} · "
                f"{done_lessons} cours · {done_exercises} exercices"
            )
        else:
            self.learn_legend.text = (
                "Aucun cours ni exercice terminé pour l'instant —\n"
                "voir l'onglet « Formation »."
            )

        total = st.total_seconds(sessions)
        best_day, best = st.best_day(sessions)
        days = max(1, st.active_days(sessions))
        avg = total / days if sessions else 0
        week_pct = (week / weekly_goal * 100) if weekly_goal else 0.0
        self.summary_lbl.text = (
            f"Sessions : {len(sessions)}\n"
            f"Temps total : {st.format_duration(total)}\n"
            f"Moyenne par jour actif : {st.format_duration(avg)}\n"
            f"Meilleure journée : "
            + (f"{best_day.strftime('%d/%m/%Y')} ({st.format_duration(best)})" if best_day else "—")
            + f"\nObjectif hebdomadaire : {week_pct:.0f} % de {st.format_duration(weekly_goal)}"
        )


# =========================================================================== #
# 3. Objectifs & rappels
# =========================================================================== #
class GoalsScreen(BaseScreen):
    def __init__(self, app, **kw):
        self.app = app
        super().__init__(**kw)
        self._build()

    def _build(self) -> None:
        sv, col = scroll_column()
        self.add_widget(sv)

        # anneau du jour
        ring_card = Card(size_hint_y=None, height=dp(220), spacing=dp(4))
        ring_card.add_widget(small_label("OBJECTIF DU JOUR", colors.ACCENT, size=11))
        self.ring = RingWidget(size_hint_y=None, height=dp(170))
        ring_card.add_widget(self.ring)
        col.add_widget(ring_card)

        # objectifs chiffrés
        goal_card = Card(size_hint_y=None, spacing=dp(10))
        goal_card.add_widget(small_label("MES OBJECTIFS", colors.ACCENT, size=11))
        self.daily_field = MDTextField(hint_text="Objectif quotidien (minutes)", mode="rectangle", input_filter="int")
        self.weekly_field = MDTextField(hint_text="Objectif hebdomadaire (minutes)", mode="rectangle", input_filter="int")
        goal_card.add_widget(self.daily_field)
        goal_card.add_widget(self.weekly_field)
        goal_card.add_widget(primary_button("Enregistrer les objectifs", self._save_goals))
        goal_card.bind(minimum_height=lambda *_: setattr(goal_card, "height", goal_card.minimum_height + dp(26)))
        col.add_widget(goal_card)

        # rappel
        rem_card = Card(size_hint_y=None, spacing=dp(10))
        rem_card.add_widget(small_label("RAPPEL QUOTIDIEN", colors.ACCENT, size=11))
        rem_card.add_widget(
            small_label(
                "Une notification locale vous invite à coder à l'heure choisie.",
                colors.MUTED, size=12, height=dp(34),
            )
        )
        self.time_field = MDTextField(hint_text="Heure (HH:MM)", mode="rectangle")
        rem_card.add_widget(self.time_field)

        row = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(10))
        self.reminder_btn = primary_button("Activer le rappel", self._toggle_reminder)
        row.add_widget(self.reminder_btn)
        row.add_widget(ghost_button("Tester", self._test_reminder))
        rem_card.add_widget(row)
        self.reminder_state = small_label("", colors.MUTED, size=12, height=dp(20))
        rem_card.add_widget(self.reminder_state)
        rem_card.bind(minimum_height=lambda *_: setattr(rem_card, "height", rem_card.minimum_height + dp(26)))
        col.add_widget(rem_card)

        col.add_widget(
            small_label(
                "Les notifications sont envoyées par le système Android/Windows ; "
                "aucune donnée ne quitte votre appareil.",
                colors.FAINT, size=11, height=dp(40),
            )
        )
        col.add_widget(Label(size_hint_y=None, height=dp(8)))

    # ------------------------------------------------------------------ #
    def _save_goals(self, *_args) -> None:
        try:
            daily = int(self.daily_field.text or 0)
            weekly = int(self.weekly_field.text or 0)
        except ValueError:
            show_message("Valeur invalide", "Saisis des nombres entiers de minutes.")
            return
        if daily < 0 or weekly < 0:
            show_message("Valeur invalide", "Les objectifs doivent être positifs.")
            return
        self.store().set_goals(daily, weekly)
        self.refresh()
        self.app.refresh_chrome()
        show_message("Objectifs enregistrés",
                     f"Quotidien : {st.format_duration(daily * 60)}\n"
                     f"Hebdomadaire : {st.format_duration(weekly * 60)}")

    def _toggle_reminder(self, *_args) -> None:
        enabled = not self.store().settings.get("reminder_enabled", False)
        time_txt = (self.time_field.text or "").strip()
        if enabled and not self._valid_time(time_txt):
            show_message("Heure invalide", "Format attendu : HH:MM (ex. 20:00).")
            return
        self.store().set_settings(reminder_enabled=enabled, reminder_time=time_txt or "20:00",
                                  last_reminder_day="")
        self.refresh()

    @staticmethod
    def _valid_time(text: str) -> bool:
        try:
            datetime.strptime(text, "%H:%M")
            return True
        except ValueError:
            return False

    def _test_reminder(self, *_args) -> None:
        ok = notifier.notify("BabiProgrammeur", "Temps de coder ! 🧑‍💻")
        if ok:
            show_message("Rappel envoyé", "La notification système est partie.")
        else:
            show_message(
                "Notifications indisponibles",
                "Cette plateforme ne fournit pas de notifications.\n"
                "Le rappel restera visible dans l'application.",
            )

    def refresh(self) -> None:
        goals = self.store().goals
        settings = self.store().settings
        if not self.daily_field.focus:
            self.daily_field.text = str(int(goals.get("daily_minutes", 0)))
        if not self.weekly_field.focus:
            self.weekly_field.text = str(int(goals.get("weekly_minutes", 0)))
        if not self.time_field.focus:
            self.time_field.text = settings.get("reminder_time", "20:00")

        daily_goal = int(goals.get("daily_minutes", 0)) * 60
        today = st.seconds_today(self.store().sessions)
        self.ring.progress = (today / daily_goal) if daily_goal else 0.0
        self.ring.center_text = f"{min(today / daily_goal, 9.99):.1f} h" if daily_goal else st.format_duration(today)
        if daily_goal:
            self.ring.caption = f"objectif {st.format_duration(daily_goal)}"
        else:
            self.ring.caption = "aucun objectif"

        enabled = bool(settings.get("reminder_enabled"))
        self.reminder_btn.text = "Désactiver le rappel" if enabled else "Activer le rappel"
        self.reminder_state.text = (
            f"Rappel actif à {settings.get('reminder_time', '20:00')}"
            if enabled
            else "Rappel inactif"
        )
        self.reminder_state.color = colors.GREEN if enabled else colors.MUTED


# =========================================================================== #
# 4. Historique & export
# =========================================================================== #
class HistoryScreen(BaseScreen):
    def __init__(self, app, **kw):
        self.app = app
        super().__init__(**kw)
        self._build()

    def _build(self) -> None:
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10),
                         pos_hint={"x": 0, "y": 0})

        head = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        self.count_lbl = Label(
            text="0 session", font_size=sp(15), bold=True, color=colors.TEXT,
            halign="left", valign="middle",
        )
        self.count_lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
        head.add_widget(self.count_lbl)
        export_json_btn = ghost_button("JSON", self._export_json)
        export_json_btn.width = dp(76)
        export_csv_btn = ghost_button("CSV", self._export_csv)
        export_csv_btn.width = dp(76)
        head.add_widget(export_json_btn)
        head.add_widget(export_csv_btn)
        root.add_widget(head)

        self.total_lbl = small_label("", colors.MUTED, size=12, height=dp(20))
        root.add_widget(self.total_lbl)

        sv = ScrollView(do_scroll_x=False, bar_width=dp(6), bar_color=colors.LINE,
                        pos_hint={"x": 0, "y": 0},
                        scroll_type=["bars", "content"], always_overscroll=False)
        hard_bounds(sv)
        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        sv.add_widget(self.list_box)
        root.add_widget(sv)

        clear_btn = ghost_button("Effacer toutes les données", self._clear_all)
        root.add_widget(clear_btn)

        self.add_widget(root)

    # ------------------------------------------------------------------ #
    def _row(self, s: Session) -> Card:
        row = Card(orientation="horizontal", size_hint_y=None, height=dp(64),
                   padding=(dp(12), dp(8), dp(12), dp(8)), spacing=dp(10))

        left = BoxLayout(orientation="vertical", spacing=dp(2))
        title = small_label(s.project or "Sans projet", colors.TEXT, size=14, bold=True, height=dp(22))
        started = datetime.fromtimestamp(s.started_at)
        meta = small_label(
            f"{started.strftime('%d/%m/%Y · %H:%M')}"
            + (f"  ·  {s.language}" if s.language else ""),
            colors.MUTED, size=11, height=dp(18),
        )
        if s.notes:
            note = small_label(s.notes[:60] + ("…" if len(s.notes) > 60 else ""),
                               colors.FAINT, size=11, height=dp(16))
            left.add_widget(title)
            left.add_widget(meta)
            left.add_widget(note)
        else:
            left.add_widget(title)
            left.add_widget(meta)
            left.add_widget(Label(size_hint_y=None, height=0))
        row.add_widget(left)

        right = BoxLayout(size_hint_x=None, width=dp(116), spacing=dp(6))
        dur = Label(
            text=st.format_duration(s.duration),
            font_size=sp(14), bold=True, color=colors.ACCENT,
            halign="right", valign="middle", size_hint_x=None, width=dp(76),
        )
        dur.bind(size=lambda l, _s: setattr(l, "text_size", l.size))
        right.add_widget(dur)

        del_btn = Button(
            text="✕",
            font_size=sp(15),
            color=colors.FAINT,
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            size_hint_x=None,
            width=dp(30),
        )
        del_btn.bind(on_release=lambda *_: self._delete(s))
        right.add_widget(del_btn)
        row.add_widget(right)
        return row

    def _delete(self, session: Session) -> None:
        confirm(
            "Supprimer cette session ?",
            f"{session.project or 'Sans projet'} · {st.format_duration(session.duration)}",
            on_yes=lambda: (self.store().delete(session.id), self.refresh(), self.app.refresh_chrome()),
            yes_label="Supprimer",
            danger=True,
        )

    def _export_json(self, *_args) -> None:
        self._run_export(exporter.export_json, "JSON")

    def _export_csv(self, *_args) -> None:
        self._run_export(exporter.export_csv, "CSV")

    def _run_export(self, fn, fmt: str) -> None:
        sessions = self.store().sessions
        if not sessions:
            show_message("Rien à exporter", "Aucune session enregistrée pour le moment.")
            return
        try:
            path = fn(sessions)
        except OSError as exc:
            show_message("Export impossible", str(exc))
            return
        show_message(f"Export {fmt}", f"{len(sessions)} sessions exportées.\n\n{path}")

    def _clear_all(self, *_args) -> None:
        confirm(
            "Effacer toutes les données ?",
            "Toutes les sessions, objectifs et réglages seront supprimés.\n"
            "Pense à exporter avant.",
            on_yes=lambda: (self.store().clear_all(), self.refresh(), self.app.refresh_chrome()),
            yes_label="Tout effacer",
            danger=True,
        )

    # ------------------------------------------------------------------ #
    def refresh(self) -> None:
        sessions = self.store().sessions
        total = st.total_seconds(sessions)
        self.count_lbl.text = f"{len(sessions)} session" + ("s" if len(sessions) > 1 else "")
        self.total_lbl.text = f"Temps total cumulé : {st.format_duration(total)}"

        self.list_box.clear_widgets()
        if not sessions:
            empty = Card(size_hint_y=None, height=dp(120))
            empty.add_widget(
                small_label(
                    "Aucune session pour le moment.\n\n"
                    "Passe onglet « Suivi » et lance un chronomètre pour commencer.",
                    colors.MUTED, size=13, height=dp(90),
                )
            )
            self.list_box.add_widget(empty)
        else:
            for s in sessions:
                self.list_box.add_widget(self._row(s))
        self.list_box.add_widget(Label(size_hint_y=None, height=dp(4)))


# =========================================================================== #
# 5. Formation : cours & exercices de chaque langage
# =========================================================================== #
class LearningScreen(BaseScreen):
    """Parcours prédéfini par langage : progression cochable, jalons datés
    et comparaison entre langages."""

    def __init__(self, app, **kw):
        self.app = app
        self.lang = curriculum.langs()[0]
        super().__init__(**kw)
        self._build()

    # ------------------------------------------------------------------ #
    def _build(self) -> None:
        sv, col = scroll_column()
        self.add_widget(sv)

        # --- choix du langage (puces) ----------------------------------- #
        chips_scroll = ScrollView(do_scroll_y=False, do_scroll_x=True, size_hint_y=None,
                                  height=dp(44), always_overscroll=False)
        hard_bounds(chips_scroll)
        chips = BoxLayout(size_hint_x=None, spacing=dp(8), padding=(0, dp(4), 0, dp(4)))
        chips.bind(minimum_width=chips.setter("width"))
        self.chips = []
        for name in curriculum.langs():
            chip = Chip(text=name, width=dp(30) + len(name) * dp(7.6), height=dp(32),
                        accent=list(colors.lang_color(name)))
            chip.bind(on_release=self._on_chip)
            self.chips.append(chip)
            chips.add_widget(chip)
        chips.add_widget(Label(size_hint_x=None, width=dp(4)))
        chips_scroll.add_widget(chips)
        col.add_widget(chips_scroll)

        # --- progression du langage sélectionné ------------------------- #
        prog_card = Card(size_hint_y=None, spacing=dp(6))
        prog_card.add_widget(small_label("PROGRESSION", colors.ACCENT, size=11))
        self.prog_head = small_label("", colors.TEXT, size=14, bold=True, height=dp(24))
        prog_card.add_widget(self.prog_head)
        self.row_lessons = BarRow(label="Cours", value_text="0 / 0")
        self.row_exercises = BarRow(label="Exercices", value_text="0 / 0")
        prog_card.add_widget(self.row_lessons)
        prog_card.add_widget(self.row_exercises)
        self.prog_detail = small_label("", colors.MUTED, size=11, height=dp(18))
        prog_card.add_widget(self.prog_detail)
        prog_card.bind(minimum_height=lambda *_: setattr(prog_card, "height", prog_card.minimum_height + dp(26)))
        col.add_widget(prog_card)

        # --- listes cochables -------------------------------------------- #
        self.lessons_section = section("Cours")
        col.add_widget(self.lessons_section)
        self.lessons_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self.lessons_box.bind(minimum_height=self.lessons_box.setter("height"))
        col.add_widget(self.lessons_box)

        self.exercises_section = section("Exercices")
        col.add_widget(self.exercises_section)
        self.exercises_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self.exercises_box.bind(minimum_height=self.exercises_box.setter("height"))
        col.add_widget(self.exercises_box)

        # --- jalons récents ---------------------------------------------- #
        jalon_card = Card(size_hint_y=None, spacing=dp(4))
        jalon_card.add_widget(small_label("DERNIERS JALONS", colors.ACCENT, size=11))
        self.jalons_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4))
        self.jalons_box.bind(minimum_height=self.jalons_box.setter("height"))
        jalon_card.add_widget(self.jalons_box)
        jalon_card.bind(minimum_height=lambda *_: setattr(jalon_card, "height", jalon_card.minimum_height + dp(26)))
        col.add_widget(jalon_card)

        # --- comparaison entre langages ----------------------------------- #
        all_card = Card(size_hint_y=None, spacing=dp(4))
        all_card.add_widget(small_label("PROGRESSION PAR LANGAGE", colors.ACCENT, size=11))
        self.all_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
        self.all_box.bind(minimum_height=self.all_box.setter("height"))
        all_card.add_widget(self.all_box)
        all_card.bind(minimum_height=lambda *_: setattr(all_card, "height", all_card.minimum_height + dp(26)))
        col.add_widget(all_card)

        col.add_widget(Label(size_hint_y=None, height=dp(8)))

    # ------------------------------------------------------------------ #
    def _on_chip(self, chip) -> None:
        for c in self.chips:
            sel = c is chip
            c.state = "down" if sel else "normal"
            c.locked = sel  # anti-rebond : bloque le _do_release planifié
        self.lang = chip.text
        self.refresh()

    def _fill_items(self, box: BoxLayout, kind: str) -> None:
        box.clear_widgets()
        store = self.store()
        for slug, title, desc in curriculum.items(self.lang, kind):
            done = store.item_done(self.lang, kind, slug)
            # lu = fiche déjà ouverte ; un élément déjà coché est réputé lu
            lu = store.item_read(self.lang, kind, slug) or done
            row = CheckRow(
                title=title,
                subtitle=desc,
                done=done,
                read=lu,
            )
            row.toggle_callback = (
                lambda _row, k=kind, s=slug, t=title, d=desc:
                self._toggle_or_read(k, s, t, d))
            row.read_callback = (
                lambda _row, k=kind, s=slug, t=title, d=desc:
                self._open_fiche(k, s, t, d))
            box.add_widget(row)

    def _toggle_or_read(self, kind: str, slug: str, title: str, desc: str) -> None:
        """Coche l'élément — sauf si sa fiche n'a jamais été ouverte : l'appui
        ouvre alors la fiche. La lecture précède la validation."""
        store = self.store()
        allowed = store.item_read(self.lang, kind, slug) or store.item_done(
            self.lang, kind, slug)
        if not allowed:
            self._open_fiche(kind, slug, title, desc)
            return
        done = not store.item_done(self.lang, kind, slug)
        store.set_item(self.lang, kind, slug, title, done)
        self.refresh()

    def _open_fiche(self, kind: str, slug: str, title: str, desc: str) -> None:
        """Fiche plein écran : contenu détaillé du cours ou de l'exercice.
        Son ouverture enregistre la lecture qui débloque la coche.
        Les exercices ouvrent en plus l'espace « Mon essai » (brouillon
        enregistré automatiquement) et le bouton « Voir la correction »."""
        if self.store().set_item_read(self.lang, kind, slug):
            self.refresh()  # la ligne passe en « lu » (pastille, résumé)
        ContentFiche(
            title=title,
            meta=f"{self.lang} · {'Cours' if kind == 'lessons' else 'Exercice'}",
            desc=desc,
            text=content.content_for(self.lang, kind, title),
            draft=(self.store(), self.lang, slug) if kind == "exercises" else None,
        ).open()

    # ------------------------------------------------------------------ #
    def refresh(self) -> None:
        if not curriculum.has_lang(self.lang):
            self.lang = curriculum.langs()[0]
        for chip in self.chips:
            sel = chip.text == self.lang
            chip.state = "down" if sel else "normal"
            chip.locked = sel  # anti-rebond : bloque le _do_release planifié
        store = self.store()

        # progression du langage
        tot_l = curriculum.total(self.lang, "lessons")
        tot_e = curriculum.total(self.lang, "exercises")
        done_l, done_e = store.learning_counts(self.lang)
        done_l, done_e = min(done_l, tot_l), min(done_e, tot_e)
        total = tot_l + tot_e
        finished = done_l + done_e
        pct = (finished / total * 100) if total else 0.0

        self.prog_head.text = f"{self.lang}  ·  {pct:.0f} %"
        accent = list(lang_color(self.lang))
        self.row_lessons.color = accent
        self.row_lessons.fraction = (done_l / tot_l) if tot_l else 0.0
        self.row_lessons.value_text = f"{done_l} / {tot_l}"
        self.row_exercises.color = accent
        self.row_exercises.fraction = (done_e / tot_e) if tot_e else 0.0
        self.row_exercises.value_text = f"{done_e} / {tot_e}"
        if total and finished >= total:
            self.prog_detail.text = f"Parcours terminé !  🎉  ({total} éléments)"
            self.prog_detail.color = colors.GREEN
        else:
            plural = "s" if finished > 1 else ""
            self.prog_detail.text = f"{finished} élément{plural} terminé{plural} sur {total}"
            self.prog_detail.color = colors.MUTED

        # listes cochables
        self.lessons_section.text = f"Cours · {self.lang}".upper()
        self.exercises_section.text = f"Exercices · {self.lang}".upper()
        self._fill_items(self.lessons_box, "lessons")
        self._fill_items(self.exercises_box, "exercises")

        # jalons récents, du plus récent au plus ancien
        self.jalons_box.clear_widgets()
        events = store.learning_events()
        if events:
            for ev in reversed(events[-5:]):
                try:
                    day = datetime.strptime(ev.get("date", ""), "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError:
                    day = ev.get("date", "")
                self.jalons_box.add_widget(small_label(
                    f"✓  {ev.get('title', '')}  ·  {ev.get('lang', '')}  ·  {day}",
                    colors.MUTED, size=12, height=dp(20),
                ))
        else:
            self.jalons_box.add_widget(small_label(
                "Coche un cours ou un exercice pour ouvrir le feu.",
                colors.FAINT, size=12, height=dp(20),
            ))

        # comparaison : langages avec au moins un élément terminé
        self.all_box.clear_widgets()
        rows = []
        for name in curriculum.langs():
            tl = curriculum.total(name, "lessons")
            te = curriculum.total(name, "exercises")
            dl, de = store.learning_counts(name)
            tot = tl + te
            fin = min(dl, tl) + min(de, te)
            if fin and tot:
                rows.append((name, fin, tot))
        rows.sort(key=lambda r: r[1] / r[2], reverse=True)
        for name, fin, tot in rows:
            self.all_box.add_widget(BarRow(
                label=name,
                value_text=f"{fin / tot:.0%}",
                fraction=fin / tot,
                color=list(lang_color(name)),
            ))
        if not rows:
            self.all_box.add_widget(small_label(
                "Aucun élément terminé pour l'instant.",
                colors.FAINT, size=12, height=dp(20),
            ))


# =========================================================================== #
# 7. Corrections des exercices
# =========================================================================== #
class CorrectionScreen(BaseScreen):
    """Corrections commentées des exercices, par langage : solution,
    explication du raisonnement, points de vérification. Lecture seule :
    aucun état de progression n'est lu ni modifié ici."""

    def __init__(self, app, **kw):
        self.app = app
        self.lang = curriculum.langs()[0]
        super().__init__(**kw)
        self._build()

    # ------------------------------------------------------------------ #
    def _build(self) -> None:
        sv, col = scroll_column()
        self.add_widget(sv)

        # --- choix du langage (puces) ------------------------------------ #
        chips_scroll = ScrollView(do_scroll_y=False, do_scroll_x=True, size_hint_y=None,
                                  height=dp(44), always_overscroll=False)
        hard_bounds(chips_scroll)
        chips = BoxLayout(size_hint_x=None, spacing=dp(8), padding=(0, dp(4), 0, dp(4)))
        chips.bind(minimum_width=chips.setter("width"))
        self.chips = []
        for name in curriculum.langs():
            chip = Chip(text=name, width=dp(30) + len(name) * dp(7.6), height=dp(32),
                        accent=list(colors.lang_color(name)))
            chip.bind(on_release=self._on_chip)
            self.chips.append(chip)
            chips.add_widget(chip)
        chips.add_widget(Label(size_hint_x=None, width=dp(4)))
        chips_scroll.add_widget(chips)
        col.add_widget(chips_scroll)

        # --- en-tête ------------------------------------------------------ #
        head = Card(size_hint_y=None, spacing=dp(6))
        head.add_widget(small_label("CORRECTIONS", colors.ACCENT, size=11))
        self.head_line = Label(
            text="", font_size=sp(14), bold=True, color=colors.TEXT,
            size_hint_y=None, height=dp(22), halign="left", valign="middle",
        )
        self.head_line.bind(size=lambda l, s: setattr(l, "text_size", s))
        head.add_widget(self.head_line)
        head.add_widget(small_label(
            "Compare ta réponse à la correction : code complet commenté, "
            "explication du raisonnement et points de vérification.",
            colors.MUTED, size=12, height=dp(34)))
        head.bind(minimum_height=lambda *_: setattr(head, "height",
                                                    head.minimum_height + dp(26)))
        col.add_widget(head)

        # --- liste des exercices ------------------------------------------ #
        col.add_widget(section("Exercices"))
        self.rows_box = BoxLayout(orientation="vertical", size_hint_y=None,
                                  spacing=dp(6))
        self.rows_box.bind(minimum_height=self.rows_box.setter("height"))
        col.add_widget(self.rows_box)
        col.add_widget(Label(size_hint_y=None, height=dp(8)))

        self.refresh()

    # ------------------------------------------------------------------ #
    def _on_chip(self, chip) -> None:
        for c in self.chips:
            sel = c is chip
            c.state = "down" if sel else "normal"
            c.locked = sel  # anti-rebond : bloque le _do_release planifié
        self.lang = chip.text
        self.refresh()

    def refresh(self, *_args) -> None:
        if not curriculum.has_lang(self.lang):
            self.lang = curriculum.langs()[0]
        for c in self.chips:
            sel = c.text == self.lang
            c.state = "down" if sel else "normal"
            c.locked = sel  # anti-rebond : bloque le _do_release planifié

        items = curriculum.items(self.lang, "exercises")
        pret = sum(1 for _slug, t, _d in items
                   if solutions.has_solution(self.lang, t))
        self.head_line.text = (f"{self.lang} · {pret}/{len(items)} "
                               "exercices corrigés")

        self.rows_box.clear_widgets()
        for _slug, title, desc in items:
            row = LinkRow(title=title, subtitle=desc)
            row.action = (lambda _row, l=self.lang, t=title, d=desc:
                          self._open_correction(l, t, d))
            self.rows_box.add_widget(row)

    def _open_correction(self, lang: str, title: str, desc: str) -> None:
        """Correction plein écran : solution commentée de l'exercice.
        Lecture seule — contrairement à la fiche Formation, l'ouverture
        n'enregistre aucune lecture ni coche."""
        ContentFiche(
            title=title,
            meta=f"{lang} · Correction d'exercice",
            desc=desc,
            text=solutions.solution_for(lang, title),
        ).open()
