"""Sonde d'apprentissage : un VRAI tap (toucher injecté par la fenêtre)
respecte-t-il la règle de lecture — 1er appui sur une ligne non lue = fiche
ouverte (coche bloquée), 2e appui = bascule — et une puce change-t-elle de
langage ?

    python tests/probe_learn.py

Le toucher suit le pipeline réel de kivy/base.py : on_touch_down puis
on_touch_up par la fenêtre, et rejeu aux widgets « grabbés » avec
transformation des coordonnées par widget (la matrice g_translate du
ScrollView déplace le rendu sans bouger les positions brutes — sans cette
transformation, le relâchement « rate » la ligne).

Les données sont redirigées vers un fichier temporaire : aucune donnée
réelle n'est touchée.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.input.motionevent import MotionEvent  # noqa: E402
from kivy.metrics import dp  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402
from kivy.uix.widget import Widget  # noqa: E402

os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402
from ui.widgets import CheckRow  # noqa: E402

REPORT: list[str] = []
TMP: str | None = None
FIRST: dict = {}    # état du 1er tap (lang, slug, titre, coche avant)
RETRY = {"row": 0, "row2": 0, "chip": 0, "fiche": 0}
DONE = {"flag": False}


def _trace(fn):
    """Enveloppe chaque phase : une exception devient une ligne de rapport
    au lieu de casser silencieusement la chaîne de callbacks."""

    def wrap(*_args):
        try:
            fn(*_args)
        except Exception as exc:  # noqa: BLE001
            import traceback
            REPORT.append(f"[ERREUR] {fn.__name__}: {exc!r}")
            REPORT.append(traceback.format_exc())
            Clock.schedule_once(finish, 0.1)
    return wrap


# ----------------------------------------------------------------- toucher --
class Touch(MotionEvent):
    def __init__(self, x: float, y: float):
        super().__init__("mouse", "learn-tap", ())
        self.profile = ["pos"]
        self.ud = {}
        self.x = self.px = x
        self.y = self.py = y
        self.pos = (x, y)
        sx = x / max(Window.width, 1)
        sy = y / max(Window.height, 1)
        self.sx = self.psx = sx
        self.sy = self.psy = sy
        self.ox = self.osx = sx
        self.oy = self.osy = sy
        self.dx = self.dy = 0.0
        self.dsx = self.dsy = 0.0


def replay_up(touch: Touch) -> None:
    """Rejeu « end » comme kivy/base.py : coordonnées du pointeur ramenées
    dans le repère brut de chaque widget grabbé, puis on_touch_up."""
    for ref in list(touch.grab_list):
        wid = ref() if callable(ref) else ref
        if wid is None:
            continue
        touch.push()
        try:
            touch.apply_transform_2d(wid.to_widget)
            touch.grab_current = wid
            wid.dispatch("on_touch_up", touch)
        finally:
            touch.grab_current = None
            touch.pop()


def tap(x: float, y: float) -> int:
    """Tap complet : renvoie le nombre de widgets ayant grabbé le toucher."""
    t = Touch(x, y)
    Window.dispatch("on_touch_down", t)
    grabs = len(t.grab_list)
    Window.dispatch("on_touch_up", t)
    replay_up(t)
    return grabs


def rows_of(screen) -> list[CheckRow]:
    found: list[CheckRow] = []

    def walk(w):
        if isinstance(w, CheckRow):
            found.append(w)
        for child in w.children:
            walk(child)

    walk(screen)
    return list(reversed(found))  # ordre visuel, haut -> bas


def row_for(screen, title: str) -> CheckRow | None:
    """Ligne portant ce titre exact (indépendamment de l'ordre du parcours)."""
    for row in rows_of(screen):
        if row.title == title:
            return row
    return None


def row_visible(learn, row) -> tuple[bool, float, float, str]:
    """Vrai si l'onglet Formation est au repos, la ligne mise en page et
    réellement dans la fenêtre (transition, resize ou layout encore en cours)."""
    if row is None:
        return False, 0.0, 0.0, "ligne introuvable"
    if app.sm.current != "learn" or abs(learn.x) >= 1:
        return False, 0.0, 0.0, "transition d'onglet"
    if row.width < dp(200) or row.height < dp(60):
        return False, 0.0, 0.0, "pas encore mis en page"
    wx, wy = row.to_window(*row.center)
    if not (0 < wx < Window.width - 1 and 0 < wy < Window.height - 1):
        return False, wx, wy, "hors fenetre"
    return True, wx, wy, ""


def scroll_ancestors(w) -> list[ScrollView]:
    """ScrollViews contenant w — chaîne strictement bornée : jamais au-delà de
    l'arbre Kivy (une marche .parent non bornée tourne en boucle à l'infini)."""
    found: list[ScrollView] = []
    p = getattr(w, "parent", None)
    for _ in range(40):  # garde-fou absolu
        if p is None or not isinstance(p, Widget):
            break
        if isinstance(p, ScrollView):
            found.append(p)
        p = getattr(p, "parent", None)
    return found


def ensure_visible(learn, row, tag: str) -> None:
    """Recale le défilement vertical sur la ligne (si un ScrollView la porte).

    Jamais sur une ligne non mise en page : ScrollView.scroll_to renvoie une
    distance de défilement erronée quand le contenu est encore incomplet
    (convert_distance_to_scroll → sy=1) et force scroll_y à 0 (bas de liste)."""
    del learn  # la colonne se trouve via les parents de la ligne
    ancs = scroll_ancestors(row)
    if not ancs:
        return
    sv = ancs[-1]  # le plus externe : la colonne verticale
    before = sv.scroll_y
    for a in ancs:
        a.scroll_to(row, padding=dp(8), animate=False)
    after = sv.scroll_y
    vp_h = sv._viewport.height if sv._viewport else 0.0
    REPORT.append(
        f"[retry {tag}] scroll_to : {before:.3f} -> {after:.3f} "
        f"(contenu={vp_h:.0f} fenetre={sv.height:.0f})"
    )


def debug_geom(learn, w, tag: str) -> None:
    """Trace la géométrie brute (window, écran, widget, défilements)."""
    parts = [f"win={Window.size}", f"cur={app.sm.current}",
             f"learn=({learn.x:.0f},{learn.y:.0f},"
             f"{learn.width:.0f}x{learn.height:.0f})"]
    if w is not None:
        wx, wy = w.to_window(w.x, w.y)
        parts.append(f"pos=({w.x:.0f},{w.y:.0f}) "
                     f"size=({w.width:.0f}x{w.height:.0f}) "
                     f"win=({wx:.0f},{wy:.0f})")
        for sv in scroll_ancestors(w):
            parts.append(f"sv=({sv.x:.0f},{sv.y:.0f},{sv.width:.0f}x{sv.height:.0f})"
                         f" scroll_y={sv.scroll_y:.3f}")
    REPORT.append(f"[debug {tag}] " + " ".join(parts))


# ------------------------------------------------------------------ phases --
def start(_dt: float) -> None:
    global TMP
    TMP = tempfile.mkdtemp(prefix="babi-learn-")
    app.store.path = os.path.join(TMP, "data.json")
    app.store.clear_all()
    app.switch_tab("learn")
    REPORT.append("[step] start : donnees temporaires, onglet Formation")
    Clock.schedule_once(tap_row, 1.0)


def tap_row(_dt: float) -> None:
    """1er appui : fiche non lue → la coche doit rester bloquée."""
    from core import curriculum

    learn = app.screens["learn"]
    slug, title, _ = curriculum.items(learn.lang, "lessons")[0]
    row = row_for(learn, title)
    if row is None:
        REPORT.append(f"[ligne] AUCUNE ligne pour {title!r}")
        Clock.schedule_once(finish, 0.2)
        return
    ok_pos, wx, wy, raison = row_visible(learn, row)
    if not ok_pos:
        # transition / mise en page en cours : retenter — et ne JAMAIS appeler
        # scroll_to sur une ligne non mise en page (forcerait scroll_y à 0)
        if raison == "hors fenetre":
            ensure_visible(learn, row, "1er")
        REPORT.append(f"[retry 1er] n={RETRY['row']} : {raison}")
        RETRY["row"] += 1
        if RETRY["row"] <= 20:
            Clock.schedule_once(tap_row, 0.3)
            return
        REPORT.append(f"[ligne] ECHEC ligne jamais visible ({wx:.0f},{wy:.0f})")
        Clock.schedule_once(tap_chip, 0.4)  # on poursuit par la puce
        return
    FIRST.update(lang=learn.lang, slug=slug, title=title,
                 before=app.store.item_done(learn.lang, "lessons", slug))
    debug_geom(learn, row, "1er")
    grabs = tap(wx, wy)
    lu = app.store.item_read(learn.lang, "lessons", slug)
    after = app.store.item_done(learn.lang, "lessons", slug)
    ok = after == FIRST["before"] and lu and grabs >= 1
    REPORT.append(
        f"[ligne] 1er appui {title!r} centre=({wx:.0f},{wy:.0f}) grabs={grabs} | "
        f"fiche non lue : coche inchangee ({after}), lue={lu} : "
        f"{'OK' if ok else 'ECHEC'}"
    )
    # fermer la fiche ouverte, puis retaper la ligne (elle est maintenant lue)
    for w in list(Window.children):
        if type(w).__name__ == "ContentFiche":
            w.dismiss()
    Clock.schedule_once(tap_row_again, 0.6)


def tap_row_again(_dt: float) -> None:
    """2e appui : la fiche est lue → la ligne doit basculer."""
    pending = [w for w in Window.children
               if type(w).__name__ == "ContentFiche"]
    if pending and RETRY["fiche"] < 5:  # fermeture animée encore en cours
        RETRY["fiche"] += 1
        Clock.schedule_once(tap_row_again, 0.4)
        return
    if pending:
        REPORT.append(f"[ligne] ECHEC fiche encore ouverte apres attente : {pending}")

    learn = app.screens["learn"]
    # pas de refresh ici : il reconstruit les lignes (positions à zéro) et
    # raterait perpétuellement la garde — le rafraîchissement a déjà eu lieu
    # à l'ouverture de la fiche (set_item_read → refresh).
    row = row_for(learn, FIRST["title"])
    ok_pos, wx, wy, raison = row_visible(learn, row)
    if not ok_pos:
        if raison == "hors fenetre":
            ensure_visible(learn, row, "2e")
        REPORT.append(f"[retry 2e] n={RETRY['row2']} : {raison}")
        RETRY["row2"] += 1
        if RETRY["row2"] <= 20:
            Clock.schedule_once(tap_row_again, 0.3)
            return
        REPORT.append(f"[ligne] ECHEC 2e appui : ligne jamais visible ({wx:.0f},{wy:.0f})")
        app.store.set_item(FIRST["lang"], "lessons", FIRST["slug"],
                           FIRST["title"], FIRST["before"])
        Clock.schedule_once(tap_chip, 0.4)
        return
    debug_geom(learn, row, "2e")
    grabs = tap(wx, wy)
    before, after = FIRST["before"], app.store.item_done(FIRST["lang"], "lessons", FIRST["slug"])
    ok = after != before and grabs >= 1
    REPORT.append(
        f"[ligne] 2e appui apres lecture centre=({wx:.0f},{wy:.0f}) grabs={grabs} | "
        f"coche {before} -> {after} : {'OK' if ok else 'ECHEC'}"
    )
    # remettre l'état initial
    app.store.set_item(FIRST["lang"], "lessons", FIRST["slug"], FIRST["title"], before)
    learn.refresh()
    Clock.schedule_once(tap_chip, 0.6)


def tap_chip(_dt: float) -> None:
    learn = app.screens["learn"]
    chip = next((c for c in learn.chips if c.text == "JavaScript"), None)
    if chip is None:
        REPORT.append("[puce] puce JavaScript introuvable")
        Clock.schedule_once(finish, 0.2)
        return
    cx, cy = chip.to_window(*chip.center)
    if abs(learn.x) >= 1 or not (0 < cx < Window.width - 1
                                 and 0 < cy < Window.height - 1):
        RETRY["chip"] += 1  # onglet encore en transition : retenter
        if RETRY["chip"] <= 20:
            Clock.schedule_once(tap_chip, 0.3)
            return
    debug_geom(learn, chip, "puce")
    grabs = tap(cx, cy)
    ok = learn.lang == "JavaScript"
    REPORT.append(
        f"[puce] JavaScript centre=({cx:.0f},{cy:.0f}) grabs={grabs} | "
        f"lang={learn.lang!r} : {'OK' if ok else 'ECHEC'}"
    )
    Clock.schedule_once(finish, 0.5)


def finish(_dt: float = 0.0) -> None:
    if DONE["flag"]:  # appelé une 2e fois par le filet de sécurité
        return
    DONE["flag"] = True
    print("\n".join(REPORT))
    bad = [r for r in REPORT if "ECHEC" in r or r.startswith("[ERREUR]")]
    if not any(r.startswith(("[ligne]", "[puce]")) for r in REPORT):
        bad.append("aucune phase terminee (boucle de callbacks interrompue ?)")
    print("-" * 70)
    print("SONDE D'APPRENTISSAGE : " + ("PROBLEMES DETECTES" if bad else "OK"))
    if TMP:
        shutil.rmtree(TMP, ignore_errors=True)
    app.stop()


app = BabiProgrammeur()
start = _trace(start)
tap_row = _trace(tap_row)
tap_row_again = _trace(tap_row_again)
tap_chip = _trace(tap_chip)
Clock.schedule_once(start, 2.0)
Clock.schedule_once(finish, 45.0)  # fin garantie même si une phase casse
app.run()
_bad = [r for r in REPORT if "ECHEC" in r or r.startswith("[ERREUR]")]
if not any(r.startswith(("[ligne]", "[puce]")) for r in REPORT):
    _bad.append("aucune phase")
sys.exit(1 if _bad else 0)
