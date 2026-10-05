"""Boîtes de dialogue (ModalView Kivy pur — API stable quel que soit KivyMD)."""
from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ui import colors


def _dialog_button(text: str, primary: bool, on_release: Callable[[], None]) -> Button:
    btn = Button(
        text=text,
        size_hint_x=None,
        width=dp(110),
        size_hint_y=None,
        height=dp(40),
        font_size=sp(14),
        bold=True,
        background_normal="",
        background_down="",
        background_color=(0, 0, 0, 0),
        # primaire : texte blanc sur la pastille bleue (façon SoloLearn —
        # du texte bleu sur fond bleu était illisible)
        color=(1, 1, 1, 1) if primary else colors.MUTED,
    )

    def _sync(*_):
        btn.canvas.before.clear()
        with btn.canvas.before:
            Color(*(colors.ACCENT if primary else colors.CARD_HI))
            RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(8)])

    btn.bind(pos=_sync, size=_sync)
    btn.bind(on_release=lambda *_: on_release())
    _sync()
    return btn


class AppDialog(ModalView):
    """Titre + message + boutons, sur fond assombri."""

    def __init__(self, title: str, message: str,
                 actions: Optional[List[Tuple[str, bool, Callable[[], None]]]] = None,
                 **kw):
        kw.setdefault("size_hint", (0.88, None))
        kw.setdefault("auto_dismiss", True)
        super().__init__(**kw)
        self.height = dp(220)

        card = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
        )
        card.bind(minimum_height=lambda *_: setattr(self, "height", card.height + dp(40)))

        with card.canvas.before:
            Color(*colors.CARD)
            bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(18)])
        card.bind(pos=lambda *_: setattr(bg, "pos", card.pos),
                  size=lambda *_: setattr(bg, "size", card.size))

        title_lbl = Label(
            text=title, font_size=sp(17), bold=True, color=colors.TEXT,
            size_hint_y=None, height=dp(26), halign="left",
        )
        title_lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
        card.add_widget(title_lbl)

        msg_lbl = Label(
            text=message, font_size=sp(14), color=colors.MUTED,
            size_hint_y=None, halign="left", valign="top",
        )

        def _msg_size(l, s):
            l.text_size = (s[0], None)
            l.height = max(dp(40), l.texture_size[1] + dp(4))
            card.height = dp(96) + l.height + (dp(56) if actions else 0)

        msg_lbl.bind(size=_msg_size)
        card.add_widget(msg_lbl)
        card.add_widget(Widget(size_hint_y=None, height=0))

        if actions:
            row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(10))
            row.add_widget(Widget())
            for text, primary, cb in actions:
                row.add_widget(
                    _dialog_button(
                        text, primary, lambda _cb=cb: (self.dismiss(), _cb())
                    )
                )
            card.add_widget(row)

        self.add_widget(card)


def show_message(title: str, message: str, on_ok: Optional[Callable[[], None]] = None) -> AppDialog:
    dlg = AppDialog(title, message, actions=[("OK", True, on_ok or (lambda: None))])
    dlg.open()
    return dlg


def confirm(title: str, message: str, on_yes: Callable[[], None],
            yes_label: str = "Confirmer", no_label: str = "Annuler",
            danger: bool = False) -> AppDialog:
    dlg = AppDialog(
        title,
        message,
        actions=[
            (no_label, False, lambda: None),
            (yes_label, True, on_yes),
        ],
    )
    dlg.open()
    return dlg


class ContentFiche(ModalView):
    """Fiche plein écran : contenu détaillé d'un cours ou d'un exercice.

    Barre de titre avec retour, méta (langage · type), résumé, puis le
    contenu défilable dans un ScrollView. Les fiches d'exercice reçoivent
    ``draft=(store, lang, slug)`` : un espace « Mon essai » est ajouté en
    bas de la carte (brouillon enregistré automatiquement) avec un bouton
    « Voir la correction » qui ouvre la correction au-dessus de la fiche.
    """

    def __init__(self, title: str, meta: str, desc: str, text: str,
                 draft: Optional[Tuple[object, str, str]] = None, **kw):
        kw.setdefault("size_hint", (1, 1))
        kw.setdefault("auto_dismiss", True)  # Échap ferme ; tap sur le fond aussi
        super().__init__(**kw)
        self._draft_flush = None  # force l'enregistrement (tests, fermeture)

        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))

        card = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        with card.canvas.before:
            Color(*colors.CARD)
            bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(16)])
        card.bind(pos=lambda *_: setattr(bg, "pos", card.pos),
                  size=lambda *_: setattr(bg, "size", card.size))

        # barre de titre : retour + titre
        bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(12))
        back = _dialog_button("Retour", False, self.dismiss)
        back.width = dp(96)
        head = Label(
            text=title, font_size=sp(16), bold=True, color=colors.TEXT,
            halign="left", valign="middle",
        )
        head.bind(size=lambda l, s: setattr(l, "text_size", s))
        bar.add_widget(back)
        bar.add_widget(head)
        card.add_widget(bar)

        # méta + résumé (une seule étiquette, hauteur suivant la texture)
        sub = Label(
            text=f"{meta}\n{desc}", font_size=sp(12), color=colors.MUTED,
            size_hint_y=None, halign="left", valign="top",
        )
        sub.bind(size=lambda l, s: setattr(l, "text_size", (s[0], None)),
                 texture_size=lambda l, s: setattr(l, "height", max(dp(20), s[1])))
        card.add_widget(sub)

        # contenu défilable
        scroll = ScrollView(size_hint_y=1)
        body = Label(
            text=text, font_size=sp(13), color=colors.TEXT,
            line_height=1.25, halign="left", valign="top",
            size_hint=(1, None),
        )
        body.bind(width=lambda l, w: setattr(l, "text_size", (w, None)),
                  texture_size=lambda l, s: setattr(l, "height", s[1]))
        scroll.add_widget(body)
        card.add_widget(scroll)

        # --- espace « Mon essai » (fiches d'exercice uniquement) --------- #
        if draft is not None:
            store, lang, slug = draft
            panel = BoxLayout(orientation="vertical", size_hint_y=None,
                              spacing=dp(6), padding=(0, dp(4), 0, 0))
            head_lbl = Label(
                text="MON ESSAI — enregistrement automatique",
                font_size=sp(11), bold=True, color=colors.ACCENT,
                size_hint_y=None, height=dp(16),
                halign="left", valign="middle",
            )
            head_lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
            panel.add_widget(head_lbl)

            editor = TextInput(
                text=store.get_draft(lang, slug),
                hint_text="Écris ici ta solution, puis compare avec la correction.",
                multiline=True,
                size_hint_y=None,
                height=dp(110),
                font_size=sp(13),
                background_color=colors.BG_ALT,
                foreground_color=colors.TEXT,
                cursor_color=colors.ACCENT,
                hint_text_color=colors.FAINT,
                write_tab=True,
                padding=(dp(10), dp(8)),
            )
            panel.add_widget(editor)

            def _save(*_):
                store.set_draft(lang, slug, editor.text)
                status.text = "Brouillon enregistré"

            def _schedule(*_):
                status.text = "Enregistrement…"
                Clock.unschedule(_save)
                Clock.schedule_once(_save, 0.6)

            def _open_correction(*_):
                _save()  # le brouillon courant part avant d'ouvrir la correction
                from core import solutions
                ContentFiche(
                    title=title,
                    meta=f"{lang} · Correction d'exercice",
                    desc=desc,
                    text=solutions.solution_for(lang, title),
                ).open()

            row = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(8))
            btn = _dialog_button("Voir la correction", True, _open_correction)
            btn.width = dp(168)
            btn.height = dp(34)
            btn.font_size = sp(13)
            row.add_widget(btn)
            status = Label(
                text=("Brouillon enregistré" if editor.text else ""),
                font_size=sp(11), color=colors.MUTED,
                halign="right", valign="middle",
            )
            status.bind(size=lambda l, s: setattr(l, "text_size", s))
            row.add_widget(status)
            panel.add_widget(row)

            editor.bind(on_text=_schedule)
            # hauteur fixe : 16 (titre) + 110 (éditeur) + 34 (rangée)
            #                + espacements 6×2 + padding haut 4
            panel.height = dp(176)
            # fermeture de la fiche : dernier enregistrement par sécurité
            self.bind(on_dismiss=_save)
            self._draft_flush = _save
            card.add_widget(panel)

        root.add_widget(card)
        self.add_widget(root)
