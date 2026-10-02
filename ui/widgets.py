"""Widgets personnalisés de BabiProgrammeur (canvas maison, indépendants de la
version de KivyMD)."""
from __future__ import annotations

from kivy.graphics import Color, Ellipse, Line, RoundedRectangle, Rectangle, Triangle
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import CoreLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from ui import colors


class Card(BoxLayout):
    """Conteneur arrondi avec fond opaque."""

    def __init__(self, orientation="vertical", padding=None, spacing=None, **kw):
        super().__init__(orientation=orientation, **kw)
        self.padding = padding if padding is not None else dp(14)
        self.spacing = spacing if spacing is not None else dp(8)
        with self.canvas.before:
            Color(*colors.CARD)
            self._bg = RoundedRectangle(radius=[dp(14)], pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size


# --------------------------------------------------------------------------
# Puce de langage (bouton à bascule) — colorée par langage
# --------------------------------------------------------------------------
class Chip(Button):
    # couleur unique du langage (ui.colors.LANG_COLORS) ; au repos la puce
    # reste teintée de cette couleur, sélectionnée elle est en aplat.
    accent = ListProperty(list(colors.ACCENT))
    # Puce portant la sélection courante. ButtonBehavior planifie une remise à
    # 'normal' (_do_release) 35 ms après on_release quand l'appui est rapide :
    # sans ce verrou, la puce sélectionnée redescendrait après coup alors que
    # le champ garde la valeur — la sélection semblerait ne pas prendre.
    locked = BooleanProperty(False)

    def __init__(self, **kw):
        kw.setdefault("background_normal", "")
        kw.setdefault("background_down", "")
        kw.setdefault("background_color", (0, 0, 0, 0))  # sinon le fond blanc par défaut masque la puce
        kw.setdefault("color", colors.TEXT)
        kw.setdefault("font_size", sp(13))
        kw.setdefault("size_hint_x", None)
        kw.setdefault("accent", list(colors.ACCENT))  # liste propre par puce
        super().__init__(**kw)
        with self.canvas.before:
            self._c = Color(*colors.CARD_HI)
            self._rect = RoundedRectangle(radius=[dp(13)], pos=self.pos, size=self.size)
        self.bind(size=self._sync, pos=self._sync, state=self._on_state,
                  accent=self._on_state)
        self._on_state()

    def _on_state(self, *_):
        bg = colors.chip_bg(self.accent, self.state == "down")
        self._c.rgba = bg
        self.color = colors.text_on(bg)

    def _sync(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def _do_release(self, *args):
        # Puce verrouillée (sélection courante) : on ignore la remise à plat
        # planifiée par ButtonBehavior — seule la synchronisation de l'écran
        # décide de l'état.
        if self.locked:
            return
        super()._do_release(*args)


# --------------------------------------------------------------------------
# Bouton de navigation du bas
# --------------------------------------------------------------------------
class NavButton(Button):
    """Bouton de navigation du bas.

    Responsivité : la police est réduite (mesurée au CoreLabel) jusqu'à ce que
    le libellé ENTIER tienne dans la largeur du bouton ; le raccourcissement
    « … » ne survient qu'en dernier recours. Un libellé ne déborde donc jamais
    sur ses voisins, quelle que soit la largeur d'écran.
    """

    _FONT_BASE = 12   # sp de départ
    _FONT_MIN = 8     # sp plancher (au-delà : raccourci)
    _MARGE = 4        # dp de confort de chaque côté

    def __init__(self, **kw):
        kw.setdefault("background_normal", "")
        kw.setdefault("background_down", "")
        kw.setdefault("background_color", (0, 0, 0, 0))
        kw.setdefault("font_size", sp(self._FONT_BASE))
        kw.setdefault("bold", True)
        kw.setdefault("color", colors.FAINT)
        # garde-fou anti-débordement : texte cadré sur toute la largeur,
        # raccourci avec « … » si la police minimale ne suffit pas
        kw.setdefault("halign", "center")
        kw.setdefault("shorten", True)
        kw.setdefault("shorten_from", "right")
        kw.setdefault("max_lines", 1)
        super().__init__(**kw)
        # valeur par défaut de text_size du Label (réinitialisable : None
        # est refusé par la ListProperty, on restaure donc le défaut exact)
        self._ts_initial = list(self.text_size)
        with self.canvas.before:
            self._line_c = Color(0, 0, 0, 0)
            # y + height et non self.top : AliasProperty cachée, périmée
            # pendant le dispatch de size (voir RingWidget.redraw).
            self._line = RoundedRectangle(pos=(self.x, self.y + self.height - dp(3)), size=(0, dp(3)))
        self.bind(pos=self._sync, size=self._sync)
        self.bind(width=self._fit_label)
        self._fit_label()

    def _measure(self, fs: float) -> float:
        """Largeur naturelle du libellé à la police fs (px), au pixel près.

        CoreLabel (= classe provider active) mesure hors canevas de façon
        synchrone ; utilisable dans l'application (fenêtre initialisée).
        """
        lbl = CoreLabel(
            text=self.text,
            font_name=self.font_name,
            font_size=fs,
            bold=bool(self.bold),
        )
        lbl.refresh()
        tex = getattr(lbl, "texture", None)
        return float(tex.size[0]) if tex else 0.0

    def _fit_label(self, *_):
        """Réduit la police pour garder le libellé entier dans le bouton.

        Tant que le texte naturel tient, on laisse `text_size` à None :
        Kivy centre alors la texture naturelle d'elle-même, et les contrôles
        de mise en page (check_layout, probe_nav) mesurent le vrai texte.
        Le cadrage strict + raccourci « … » n'intervient qu'en dernier recours.
        """
        dispo = self.width - dp(self._MARGE * 2)
        if dispo <= dp(8):
            return
        fs = sp(self._FONT_BASE)
        while fs > sp(self._FONT_MIN) and self._measure(fs) > dispo:
            fs -= sp(0.5)
        if abs(float(self.font_size) - fs) > 0.25:
            self.font_size = fs
        if self._measure(fs) > self.width:
            self.text_size = (self.width, None)
        else:
            self.text_size = self._ts_initial

    def _sync(self, *_):
        self._line.pos = (self.x, self.y + self.height - dp(3))
        self._line.size = (self.width, dp(3))

    def set_active(self, active: bool) -> None:
        self.color = colors.ACCENT if active else colors.FAINT
        self._line_c.rgba = colors.ACCENT if active else (0, 0, 0, 0)


# --------------------------------------------------------------------------
# Base des graphiques : libellés d'abscisse gérés en enfants Label
# --------------------------------------------------------------------------
class _ChartBase(Widget):
    """Un Label créé dans un bloc `with widget.canvas:` n'est jamais rendu
    (ce n'est pas une instruction graphique) : les libellés d'abscisse vivent
    donc dans `self._xlabels`, positionnés à chaque redessin."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self._xlabels = []

    def _hide_xlabels(self) -> None:
        for lbl in self._xlabels:
            lbl.text = ""

    def _xlabel(self, index: int, text, color, cx: float) -> None:
        while len(self._xlabels) <= index:
            lbl = Label(
                font_size=sp(10),
                color=colors.FAINT,
                size_hint=(None, None),
                size=(dp(30), dp(16)),
                halign="center",
                valign="middle",
            )
            lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
            self._xlabels.append(lbl)
            self.add_widget(lbl)
        lbl = self._xlabels[index]
        lbl.text = str(text)
        lbl.color = color
        lbl.pos = (cx - lbl.width / 2, self.y + dp(4))


# --------------------------------------------------------------------------
# Graphique en barres (N derniers jours, ligne d'objectif)
# --------------------------------------------------------------------------
class BarChart(_ChartBase):
    data = ListProperty([])     # [(label_jour, secondes, highlight:bool)]
    target = NumericProperty(0)  # objectif quotidien en secondes

    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(data=self.redraw, target=self.redraw, pos=self.redraw, size=self.redraw)

    def redraw(self, *_args) -> None:
        # canvas.before et non canvas : canvas.clear() détacherait les
        # canvases des libellés enfants (jamais plus rendus ensuite).
        self.canvas.before.clear()
        self._hide_xlabels()
        n = len(self.data)
        if not n or self.width <= 0 or self.height <= 0:
            return

        values = [float(v) for _, v, _ in self.data]
        goal = float(self.target)
        peak = max(max(values, default=0.0), goal, 60.0) * 1.18

        pad_l, pad_r, pad_t, pad_b = dp(4), dp(4), dp(10), dp(22)
        x0 = self.x + pad_l
        base_y = self.y + pad_b
        plot_h = max(dp(20), self.height - pad_t - pad_b)
        avail = max(dp(10), self.width - pad_l - pad_r)
        gap = dp(3) if n > 7 else dp(5)
        bar_w = max(dp(3), (avail - gap * (n - 1)) / n)

        def h_for(value: float) -> float:
            return (value / peak) * plot_h

        with self.canvas.before:
            Color(*colors.LINE)
            Rectangle(pos=(self.x, base_y - dp(1)), size=(self.width, dp(1)))

            if goal > 0:
                gy = base_y + h_for(goal)
                Color(colors.ORANGE[0], colors.ORANGE[1], colors.ORANGE[2], 0.8)
                seg, seg_gap = dp(6), dp(5)
                x = x0
                while x < x0 + avail:
                    Rectangle(pos=(x, gy), size=(min(seg, x0 + avail - x), dp(1.5)))
                    x += seg + seg_gap

            for i, (label, value, highlight) in enumerate(self.data):
                value = float(value)
                x = x0 + i * (bar_w + gap)
                h = h_for(value)
                if value <= 0:
                    Color(*colors.CARD_HI, 0.8)
                    Rectangle(pos=(x, base_y), size=(bar_w, dp(2)))
                elif highlight and goal and value >= goal:
                    Color(*colors.GREEN)
                    RoundedRectangle(pos=(x, base_y), size=(bar_w, max(dp(3), h)), radius=[dp(3), dp(3), 0, 0])
                elif highlight:
                    Color(*colors.ACCENT)
                    RoundedRectangle(pos=(x, base_y), size=(bar_w, max(dp(3), h)), radius=[dp(3), dp(3), 0, 0])
                else:
                    Color(0.330, 0.470, 0.660, 1.0)
                    RoundedRectangle(pos=(x, base_y), size=(bar_w, max(dp(3), h)), radius=[dp(3), dp(3), 0, 0])

                show = n <= 10 or i % 2 == 1 or i == n - 1
                if show:
                    self._xlabel(i, label, colors.TEXT if highlight else colors.FAINT,
                                 cx=x + bar_w / 2)


# --------------------------------------------------------------------------
# Courbe d'évolution (cumul sur N jours)
# --------------------------------------------------------------------------
class LineChart(_ChartBase):
    """[(label_jour, valeur_cumulée)] → ligne + points + valeur courante.

    Utilisée pour « l'évolution » de l'apprentissage dans les statistiques.
    """

    data = ListProperty([])  # [(label, valeur)]

    def __init__(self, **kw):
        super().__init__(**kw)
        self._value_lbl = Label(
            text="",
            font_size=sp(12),
            bold=True,
            color=colors.GREEN,
            size_hint=(None, None),
            size=(dp(48), dp(16)),
            halign="center",
            valign="middle",
        )
        self._value_lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
        self.add_widget(self._value_lbl)
        self.bind(data=self.redraw, pos=self.redraw, size=self.redraw)

    def redraw(self, *_args) -> None:
        self.canvas.before.clear()
        self._hide_xlabels()
        self._value_lbl.text = ""
        n = len(self.data)
        if not n or self.width <= 0 or self.height <= 0:
            return

        values = [float(v) for _, v in self.data]
        vmax = max(max(values), 1.0)

        pad_l, pad_r, pad_t, pad_b = dp(8), dp(8), dp(18), dp(22)
        x0 = self.x + pad_l
        base_y = self.y + pad_b
        plot_h = max(dp(20), self.height - pad_t - pad_b)
        avail = max(dp(10), self.width - pad_l - pad_r)

        if n == 1:
            xs = [x0 + avail / 2]
        else:
            step = avail / (n - 1)
            xs = [x0 + i * step for i in range(n)]
        ys = [base_y + (v / vmax) * plot_h for v in values]

        with self.canvas.before:
            # ligne de base et grille médiane
            Color(*colors.LINE)
            Rectangle(pos=(self.x, base_y - dp(1)), size=(self.width, dp(1)))
            Color(colors.LINE[0], colors.LINE[1], colors.LINE[2], 0.45)
            Rectangle(pos=(self.x, base_y + plot_h / 2), size=(self.width, dp(1)))

            # aire sous la courbe (deux triangles par segment)
            Color(colors.ACCENT[0], colors.ACCENT[1], colors.ACCENT[2], 0.16)
            for i in range(n - 1):
                a, b = (xs[i], ys[i]), (xs[i + 1], ys[i + 1])
                Triangle(points=(a[0], a[1], b[0], b[1], b[0], base_y))
                Triangle(points=(a[0], a[1], b[0], base_y, a[0], base_y))

            # ligne + points (contour carte pour la lisibilité sur l'aire)
            if n > 1:
                Color(*colors.ACCENT)
                Line(points=[c for xy in zip(xs, ys) for c in xy],
                     width=dp(2), joint="round")
            for i, (px, py) in enumerate(zip(xs, ys)):
                last = i == n - 1
                r = dp(7) if last else dp(5)
                Color(*colors.CARD)
                Ellipse(pos=(px - r / 2 - dp(1), py - r / 2 - dp(1)),
                        size=(r + dp(2), r + dp(2)))
                Color(*(colors.GREEN if last and values[-1] > 0 else colors.ACCENT))
                Ellipse(pos=(px - r / 2, py - r / 2), size=(r, r))

        # libellés d'abscisse (enfants, jamais dans le canvas)
        for i, (label, _) in enumerate(self.data):
            if len(self.data) <= 10 or i % 2 == 1 or i == n - 1:
                self._xlabel(
                    i, label,
                    colors.TEXT if i == n - 1 else colors.FAINT,
                    cx=xs[i],
                )

        # valeur du dernier point, au-dessus (bornée dans le widget)
        self._value_lbl.text = str(int(values[-1]))
        self._value_lbl.color = colors.GREEN if values[-1] > 0 else colors.FAINT
        right = self.x + self.width    # pas self.right : cache périmé sur size
        top = self.y + self.height     # pas self.top : idem
        vx = min(max(xs[-1] - self._value_lbl.width / 2, self.x),
                 right - self._value_lbl.width)
        vy = min(max(ys[-1] - dp(14), self.y + dp(2)), top - dp(16))
        self._value_lbl.pos = (vx, vy)


# --------------------------------------------------------------------------
# Anneau de progression (objectif du jour)
# --------------------------------------------------------------------------
class RingWidget(Widget):
    progress = NumericProperty(0.0)   # 0..1 (peut dépasser 1)
    caption = StringProperty("")
    center_text = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self._label = Label(
            font_size=sp(22), color=colors.TEXT, halign="center", bold=True,
            size_hint=(None, None), size=(dp(160), dp(30)),
        )
        self._sub = Label(
            font_size=sp(11), color=colors.MUTED, halign="center",
            size_hint=(None, None), size=(dp(160), dp(18)),
        )
        self.add_widget(self._label)
        self.add_widget(self._sub)
        self.bind(progress=self.redraw, caption=self.redraw, center_text=self.redraw,
                  pos=self.redraw, size=self.redraw)
        self.redraw()

    def redraw(self, *_args) -> None:
        self.canvas.before.clear()
        # x, y, width, height (propriétés premières) et non self.center :
        # center est une AliasProperty cachée qui reste périmée quand le
        # déclencheur est un changement de size — l'anneau serait dessiné
        # à sa position précédente.
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        r = max(dp(10), min(self.width, self.height) / 2 - dp(10))
        with self.canvas.before:
            Color(*colors.CARD_HI)
            Line(circle=(cx, cy, r, 0, 360), width=dp(10))
            frac = max(0.0, min(1.0, float(self.progress)))
            if frac > 0:
                Color(*(colors.GREEN if frac >= 1.0 else colors.ACCENT))
                Line(circle=(cx, cy, r, -90, -90 + 360 * frac), width=dp(10), cap="round")
            if self.progress > 1.0:
                # petit repère "+100 %"
                pass

        self._label.text = self.center_text
        self._label.pos = (cx - dp(80), cy - dp(15))
        self._sub.text = self.caption
        self._sub.pos = (cx - dp(80), cy - dp(40))


# --------------------------------------------------------------------------
# Ligne de répartition (langages / projets)
# --------------------------------------------------------------------------
class BarRow(Widget):
    """Une ligne : nom en haut, barre en dessous, valeur à droite."""

    label = StringProperty("")
    value_text = StringProperty("")
    fraction = NumericProperty(0.0)
    color = ListProperty(list(colors.ACCENT))

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint_y = None
        self.height = dp(34)
        self._name = Label(
            font_size=sp(12), color=colors.TEXT, halign="left",
            size_hint=(None, None), size=(dp(10), dp(16)),
        )
        self._val = Label(
            font_size=sp(12), color=colors.MUTED, halign="right",
            size_hint=(None, None), size=(dp(10), dp(16)),
        )
        self.add_widget(self._name)
        self.add_widget(self._val)
        self.bind(pos=self.redraw, size=self.redraw, fraction=self.redraw,
                  color=self.redraw, label=self.redraw, value_text=self.redraw)
        self.redraw()

    def redraw(self, *_args) -> None:
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0)
            Rectangle(pos=self.pos, size=self.size)
            Color(*colors.CARD_HI)
            RoundedRectangle(pos=(self.x, self.y + dp(2)), size=(self.width, dp(8)), radius=[dp(4)])
            frac = max(0.0, min(1.0, float(self.fraction)))
            if frac > 0:
                Color(*self.color)
                RoundedRectangle(pos=(self.x, self.y + dp(2)), size=(max(dp(8), self.width * frac), dp(8)),
                                 radius=[dp(4)])
        self._name.text = self.label
        self._name.pos = (self.x, self.y + dp(16))
        self._name.size = (self.width * 0.62, dp(16))
        self._val.text = self.value_text
        self._val.pos = (self.x + self.width * 0.6, self.y + dp(16))
        self._val.size = (self.width * 0.4, dp(16))


class StatTile(Card):
    """Petite carte 'Aujourd'hui / Semaine / Série'."""

    def __init__(self, **kw):
        super().__init__(spacing=dp(2), padding=dp(12), **kw)
        self.value_label = Label(
            text="0", font_size=sp(18), bold=True, color=colors.TEXT,
            size_hint_y=None, height=dp(26), halign="left",
        )
        self.title_label = Label(
            text="", font_size=sp(11), color=colors.MUTED,
            size_hint_y=None, height=dp(16), halign="left",
        )
        for lab in (self.value_label, self.title_label):
            lab.bind(size=lambda l, _s: setattr(l, "text_size", _s))
        self.add_widget(self.value_label)
        self.add_widget(self.title_label)

    def set(self, title: str, value: str) -> None:
        self.title_label.text = title
        self.value_label.text = value


# --------------------------------------------------------------------------
# Ligne cochable (cours / exercices de l'onglet Formation)
# --------------------------------------------------------------------------
class CheckRow(ButtonBehavior, Widget):
    """Titre + résumé + case à cocher, sur fond arrondi comme une carte.

    Appui = bascule, glisser = défilement : si le pointeur a bougé de plus de
    8 dp entre l'appui et le relâchement, aucun basculement n'a lieu (le
    ScrollView reçoit le même toucher que nous).

    ``read = False`` signale qu'aucune fiche n'a encore été ouverte : la
    ligne se démarque (pastille « Lire » pleine, résumé en accent) et
    l'écran ouvre la fiche au lieu de cocher — la lecture précède la coche.
    """

    done = BooleanProperty(False)
    read = BooleanProperty(True)   # fiche déjà ouverte (ou élément coché)
    title = StringProperty("")
    subtitle = StringProperty("")
    toggle_callback = None  # callable(row) — appelée sur appui validé
    read_callback = None    # callable(row) — appelée sur la zone « Lire »

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint_y = None
        self.height = dp(62)
        self._down = None
        self._read_tap = False
        self._title_lbl = Label(
            font_size=sp(13), bold=True, color=colors.TEXT,
            size_hint=(None, None), halign="left", valign="middle",
        )
        self._sub_lbl = Label(
            font_size=sp(11), color=colors.MUTED,
            size_hint=(None, None), halign="left", valign="middle",
        )
        self._check_lbl = Label(
            text="✓", font_size=sp(14), bold=True, color=(0, 0, 0, 0),
            size_hint=(None, None), halign="center", valign="middle",
        )
        self._read_lbl = Label(
            text="Lire", font_size=sp(11), bold=True, color=colors.ACCENT,
            size_hint=(None, None), halign="center", valign="middle",
        )
        for lbl in (self._title_lbl, self._sub_lbl, self._check_lbl, self._read_lbl):
            lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
            self.add_widget(lbl)
        self.bind(pos=self.redraw, size=self.redraw, done=self.redraw,
                  title=self.redraw, subtitle=self.redraw, state=self.redraw,
                  read=self.redraw)
        self.redraw()

    # -------------------------------------------------------------- #
    def on_touch_down(self, touch):
        # Repère l'appui (coordonnées brutes, espace commun avec on_touch_up)
        if self.collide_point(*touch.pos):
            self._down = (touch.x, touch.y)
            # zone « Lire » : les 56 dp de droite de la ligne
            # (x + width : self.right est une AliasProperty cachée)
            self._read_tap = touch.x >= self.x + self.width - dp(56)
        else:
            self._down = None
            self._read_tap = False
        return super().on_touch_down(touch)

    def on_release(self):
        moved = False
        last = getattr(self, "last_touch", None)
        if self._down is not None and last is not None:
            dx = abs(last.x - self._down[0])
            dy = abs(last.y - self._down[1])
            moved = max(dx, dy) > dp(8)
        read = self._read_tap
        self._down = None
        self._read_tap = False
        if moved:
            return
        if read and callable(self.read_callback):
            self.read_callback(self)
        elif callable(self.toggle_callback):
            self.toggle_callback(self)

    # -------------------------------------------------------------- #
    def redraw(self, *_args) -> None:
        # canvas.before : on ne touche pas à self.canvas, qui contient les
        # canvases des libellés enfants (title, subtitle, ✓).
        self.canvas.before.clear()
        pressed = self.state == "down"
        unread = not self.read and not self.done   # fiche à lire avant coche
        with self.canvas.before:
            Color(*(colors.CARD_HI if pressed else colors.CARD))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])

            bx = self.x + dp(12)
            by = self.y + self.height / 2 - dp(10)
            if self.done:
                Color(*colors.GREEN)
                RoundedRectangle(pos=(bx, by), size=(dp(20), dp(20)), radius=[dp(6)])
            else:
                Color(*colors.CARD_HI)
                RoundedRectangle(pos=(bx, by), size=(dp(20), dp(20)), radius=[dp(6)])
                Color(*colors.LINE)
                Line(rounded_rectangle=(bx, by, dp(20), dp(20), dp(6)),
                     width=dp(1.5))

            # pastille « Lire » (zone cliquable de 56 dp à droite)
            # x + width et non self.right : AliasProperty cachée, périmée
            # pendant le dispatch de size (le décalage l'envoyait à gauche).
            # Pleine (accent) tant que la fiche n'a pas été ouverte.
            pill_w, pill_h = dp(44), dp(22)
            if unread:
                Color(*colors.ACCENT)
            else:
                Color(*(colors.LINE if pressed else colors.CARD_HI))
            RoundedRectangle(pos=(self.x + self.width - dp(52),
                                  self.y + self.height / 2 - pill_h / 2),
                             size=(pill_w, pill_h), radius=[dp(11)])

        pill_x = self.x + self.width - dp(52)
        pill_y = self.y + self.height / 2 - pill_h / 2
        tx = bx + dp(20) + dp(10)
        tw = max(dp(40), self.width - (tx - self.x) - dp(12) - dp(58))
        if self.subtitle:
            self._title_lbl.size = (tw, dp(20))
            self._title_lbl.pos = (tx, self.y + self.height - dp(6) - dp(20))
            self._sub_lbl.size = (tw, dp(16))
            self._sub_lbl.pos = (tx, self.y + dp(8))
        else:
            self._title_lbl.size = (tw, dp(20))
            self._title_lbl.pos = (tx, self.y + self.height / 2 - dp(10))
            self._sub_lbl.size = (0, 0)
            self._sub_lbl.pos = (self.x, self.y)

        self._title_lbl.text = self.title
        self._title_lbl.color = colors.FAINT if self.done else colors.TEXT
        self._sub_lbl.text = self.subtitle
        self._sub_lbl.color = (colors.FAINT if self.done
                               else colors.ACCENT if unread else colors.MUTED)

        self._check_lbl.size = (dp(20), dp(20))
        self._check_lbl.pos = (bx, by)
        self._check_lbl.color = (0.04, 0.12, 0.09, 1.0) if self.done else (0, 0, 0, 0)

        self._read_lbl.size = (pill_w, pill_h)
        self._read_lbl.pos = (pill_x, pill_y)
        # « Lire » en sombre sur pastille pleine tant que non lu
        self._read_lbl.color = ((0.04, 0.12, 0.09, 1.0) if unread
                                else colors.ACCENT)


class LinkRow(ButtonBehavior, Widget):
    """Titre + résumé + pastille « Voir » : ligne de liste qui ouvre un
    contenu (correction, fiche) sans état de progression.

    Appui = action, glisser = défilement : si le pointeur a bougé de plus
    de 8 dp entre l'appui et le relâchement, aucune action n'a lieu (le
    ScrollView reçoit le même toucher que nous). Même géométrie que
    CheckRow (62 dp, pastille de 56 dp à droite) pour des listes
    homogènes dans toute l'application.
    """

    title = StringProperty("")
    subtitle = StringProperty("")
    action = None  # callable(row) — appelée sur appui validé

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint_y = None
        self.height = dp(62)
        self._down = None
        self._title_lbl = Label(
            font_size=sp(13), bold=True, color=colors.TEXT,
            size_hint=(None, None), halign="left", valign="middle",
        )
        self._sub_lbl = Label(
            font_size=sp(11), color=colors.MUTED,
            size_hint=(None, None), halign="left", valign="middle",
        )
        self._go_lbl = Label(
            text="Voir »", font_size=sp(11), bold=True, color=colors.ACCENT,
            size_hint=(None, None), halign="center", valign="middle",
        )
        for lbl in (self._title_lbl, self._sub_lbl, self._go_lbl):
            lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
            self.add_widget(lbl)
        self.bind(pos=self.redraw, size=self.redraw, state=self.redraw,
                  title=self.redraw, subtitle=self.redraw)
        self.redraw()

    # -------------------------------------------------------------- #
    def on_touch_down(self, touch):
        # Repère l'appui (coordonnées brutes, espace commun avec on_touch_up)
        if self.collide_point(*touch.pos):
            self._down = (touch.x, touch.y)
        else:
            self._down = None
        return super().on_touch_down(touch)

    def on_release(self):
        moved = False
        last = getattr(self, "last_touch", None)
        if self._down is not None and last is not None:
            dx = abs(last.x - self._down[0])
            dy = abs(last.y - self._down[1])
            moved = max(dx, dy) > dp(8)
        self._down = None
        if moved:
            return
        if callable(self.action):
            self.action(self)

    # -------------------------------------------------------------- #
    def redraw(self, *_args) -> None:
        # canvas.before : on ne touche pas à self.canvas, qui contient les
        # canvases des libellés enfants (title, subtitle, »).
        self.canvas.before.clear()
        pressed = self.state == "down"
        with self.canvas.before:
            Color(*(colors.CARD_HI if pressed else colors.CARD))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])

            # pastille « Voir » (zone de 56 dp à droite, comme CheckRow) ;
            # x + width et non self.right : AliasProperty cachée (voir CheckRow)
            pill_w, pill_h = dp(44), dp(22)
            Color(*(colors.LINE if pressed else colors.CARD_HI))
            RoundedRectangle(pos=(self.x + self.width - dp(52),
                                  self.y + self.height / 2 - pill_h / 2),
                             size=(pill_w, pill_h), radius=[dp(11)])

        pill_x = self.x + self.width - dp(52)
        pill_y = self.y + self.height / 2 - pill_h / 2
        tx = self.x + dp(12)
        tw = max(dp(40), self.width - (tx - self.x) - dp(12) - dp(58))
        if self.subtitle:
            self._title_lbl.size = (tw, dp(20))
            self._title_lbl.pos = (tx, self.y + self.height - dp(6) - dp(20))
            self._sub_lbl.size = (tw, dp(16))
            self._sub_lbl.pos = (tx, self.y + dp(8))
        else:
            self._title_lbl.size = (tw, dp(20))
            self._title_lbl.pos = (tx, self.y + self.height / 2 - dp(10))
            self._sub_lbl.size = (0, 0)
            self._sub_lbl.pos = (self.x, self.y)

        self._title_lbl.text = self.title
        self._title_lbl.color = colors.TEXT
        self._sub_lbl.text = self.subtitle
        self._sub_lbl.color = colors.MUTED

        self._go_lbl.size = (pill_w, pill_h)
        self._go_lbl.pos = (pill_x, pill_y)
