"""Test de fumée : construit l'application, exerce tous les écrans, le
chronomètre, les exports et les dialogues, puis quitte.

    python tests/smoke.py
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.clock import Clock  # noqa: E402

os.environ.setdefault("BABI_SPLASH", "0")  # pas d'écran d'accueil en test
from main import BabiProgrammeur  # noqa: E402

FAILURES: list[str] = []
DLG_CHILDREN_BEFORE = None
DLG_TRIES = {"n": 0}


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)
        print(f"ECHEC : {message}")
    else:
        print(f"ok    : {message}")


def scenario(app: BabiProgrammeur, _dt: float) -> None:
    tmp_dir = tempfile.mkdtemp(prefix="babiprogrammeur-test-")
    try:
        store = app.store
        store.path = os.path.join(tmp_dir, "data.json")
        store.clear_all()

        # --- chronomètre ------------------------------------------------ #
        check(not store.is_running, "aucune session au démarrage")
        store.start("Projet fumée", "Python", "notes initiales")
        check(store.is_running, "démarrage d'une session")
        store.update_active(notes="notes modifiées")
        session = store.stop()
        check(session is not None and session.duration >= 1, "arrêt et enregistrement")
        check(not store.is_running, "remise à zéro du chronomètre")
        check(store.active_elapsed == 0, "écoulement nul hors session")
        check(store.stop() is None, "stop() sans session actives renvoie None")

        # --- données de démonstration ----------------------------------- #
        from core.seed import seed

        created = seed(store, days=14)
        check(created > 0 and len(store.sessions) >= created,
              f"génération de {created} sessions ({len(store.sessions)} au total)")

        # --- écrans ------------------------------------------------------ #
        for key in app.screens:
            app.switch_tab(key)
            check(app.sm.current == key, f"affichage de l'onglet {key}")
            app.screens[key].refresh()
        check(len(app.screens) == 6, "six écrans présents")

        # --- écran Formation (cours & exercices) ------------------------- #
        from core import curriculum
        from ui.widgets import CheckRow

        learn = app.screens["learn"]
        app.switch_tab("learn")
        learn.refresh()
        rows = list(reversed(learn.lessons_box.children))  # ordre visuel, haut -> bas
        check(len(rows) >= 6 and all(isinstance(r, CheckRow) for r in rows),
              f"liste des cours construite ({len(rows)} lignes)")
        ex_rows = list(reversed(learn.exercises_box.children))
        check(len(ex_rows) >= 5 and all(isinstance(r, CheckRow) for r in ex_rows),
              f"liste des exercices construite ({len(ex_rows)} lignes)")

        # --- règle de lecture : pas de coche avant ouverture de la fiche --- #
        from kivy.core.window import Window

        slug0, title0, _ = curriculum.items("Python", "lessons")[0]
        store.set_item("Python", "lessons", slug0, title0, False)  # état non coché
        was_done = store.item_done("Python", "lessons", slug0)
        check(not store.item_read("Python", "lessons", slug0),
              "fiche du premier cours pas encore lue")
        rows[0].dispatch("on_release")  # appui sur la ligne
        check(store.item_done("Python", "lessons", slug0) == was_done,
              "coche bloquée tant que la fiche n'est pas ouverte")
        check(store.item_read("Python", "lessons", slug0),
              "premier appui = fiche ouverte et lecture enregistrée")
        for w in list(Window.children):  # fermer cette première fiche
            if type(w).__name__ == "ContentFiche":
                w.dismiss()

        # la fiche est lue : l'appui coche maintenant l'élément
        fresh = list(reversed(learn.lessons_box.children))[0]
        check(fresh.read and not fresh.done, "ligne passée en « lue »")
        fresh.dispatch("on_release")
        check(store.item_done("Python", "lessons", slug0) != was_done,
              "appui après lecture = bascule de l'élément")
        fresh = list(reversed(learn.lessons_box.children))[0]
        check(fresh.done == (not was_done), "état visuel de la ligne mis à jour")
        fresh.dispatch("on_release")  # retour à l'état initial
        check(store.item_done("Python", "lessons", slug0) == was_done,
              "second appui = retour arrière")

        # --- fiches détaillées (bouton « Lire » de chaque ligne) ---------- #
        from core import content as fiches
        from kivy.core.window import Window
        from kivy.metrics import dp
        from kivy.uix.label import Label

        miss = fiches.missing()
        check(not miss,
              f"fiches pour les {curriculum.grand_total()} éléments "
              f"({fiches.coverage()} rédigées)")
        check(len(fiches.CONTENT) == len(curriculum.LANGUAGES),
              f"contenu rédigé pour les {len(curriculum.LANGUAGES)} langages")
        check("OBJECTIFS" in fiches.content_for("Python", "lessons", title0),
              "fiche de cours structurée")
        check("ÉNONCÉ" in fiches.content_for("Python", "exercises", "FizzBuzz"),
              "fiche d'exercice structurée")

        class _Touch:  # toucher simulé : même protocole que ButtonBehavior
            def __init__(self, x, y):
                self.x, self.y = x, y
                self.is_mouse_scrolling = False
                self.ud = {}
                self.grab_current = None

            @property
            def pos(self):
                return (self.x, self.y)

            def grab(self, widget):
                self.grab_current = widget

            def ungrab(self, widget):
                self.grab_current = None

        # appui dans la zone « Lire » (56 dp de droite) : fiche, pas de coche
        row0 = list(reversed(learn.lessons_box.children))[0]
        was0 = store.item_done("Python", "lessons", slug0)
        fiche_before = len(Window.children)
        touch = _Touch(row0.x + row0.width - dp(20), row0.center_y)
        row0.on_touch_down(touch)
        row0.on_touch_up(touch)
        check(len(Window.children) > fiche_before,
              "fiche ouverte depuis la zone « Lire »")
        check(store.item_done("Python", "lessons", slug0) == was0,
              "la zone « Lire » ne bascule pas la coche")

        def _labels(widget):
            found = []
            for child in widget.children:
                if isinstance(child, Label):
                    found.append(child)
                found.extend(_labels(child))
            return found

        ouvertes = [w for w in Window.children
                    if type(w).__name__ == "ContentFiche"]
        check(bool(ouvertes), "widget ContentFiche monté dans la fenêtre")
        texts = [lbl.text for w in ouvertes for lbl in _labels(w)]
        check(any(title0 in t for t in texts), "titre du cours dans la fiche")
        check(any("OBJECTIFS" in t for t in texts),
              "contenu de la fiche affiché")
        for w in ouvertes:  # fermeture animée : vérifiée dans finish()
            w.dismiss()

        # puce de langage : change de parcours
        chip_js = next(c for c in learn.chips if c.text == "JavaScript")
        chip_js.dispatch("on_release")
        check(learn.lang == "JavaScript" and "JavaScript" in learn.prog_head.text,
              "changement de langage par puce")
        check(len(learn.chips) == len(curriculum.LANGUAGES),
              f"{len(learn.chips)} langages proposés en puces")

        # couleur unique de chaque langage (puces et barres)
        from ui import colors as palette

        teintes = {palette.lang_color(n) for n in curriculum.LANGUAGES}
        check(len(teintes) == len(curriculum.LANGUAGES),
              f"{len(teintes)} couleurs distinctes pour les langages")
        check(all(list(c.accent) == list(palette.lang_color(c.text))
                  for c in learn.chips),
              "chaque puce porte la couleur de son langage")
        puce_active = next(c for c in learn.chips if c.state == "down")
        check(list(puce_active._c.rgba) == palette.chip_bg(
            palette.lang_color(puce_active.text), True),
            "puce sélectionnée en couleur pleine")
        puce_repos = next(c for c in learn.chips if c.state != "down")
        check(list(puce_repos._c.rgba) == palette.chip_bg(
            palette.lang_color(puce_repos.text), False),
            "puce au repos en teinte de langage")
        check(list(learn.row_lessons.color)
              == list(palette.lang_color(learn.lang)),
              "barres de progression à la couleur du langage")
        check(all(list(c.accent) == list(palette.lang_color(c.text))
                  for c in app.screens["timer"].chips),
              "puces du chronomètre aussi colorées")
        check(list(palette.lang_color("Python")) != list(palette.lang_color("Flutter")),
              "Python et Flutter aux teintes distinctes")

        # --- onglet Correction ------------------------------------------- #
        from core import solutions as corr
        from ui.widgets import LinkRow

        check(not corr.missing(),
              f"corrections pour les {sum(len(curriculum.items(l, 'exercises')) for l in curriculum.langs())} "
              f"exercices ({corr.coverage()} rédigées)")
        check("SOLUTION" in corr.solution_for("Python", "FizzBuzz"),
              "correction structurée (tête SOLUTION)")
        check("EXPLICATION" in corr.solution_for("Python", "FizzBuzz"),
              "correction expliquée (tête EXPLICATION)")
        check(corr.solution_for("Python", "Inconnu") != corr.solution_for("Python", "FizzBuzz"),
              "repli générique pour un titre inconnu")

        corr_screen = app.screens["corrections"]
        app.switch_tab("corrections")
        corr_screen.refresh()
        c_rows = list(reversed(corr_screen.rows_box.children))
        check(len(c_rows) == 7 and all(isinstance(r, LinkRow) for r in c_rows),
              f"liste des corrections construite ({len(c_rows)} lignes)")
        check(len(corr_screen.chips) == len(curriculum.LANGUAGES),
              f"{len(corr_screen.chips)} langages en puces (corrections)")
        check("corrigés" in corr_screen.head_line.text,
              f"en-tête de correction : {corr_screen.head_line.text!r}")

        # appui sur une ligne : correction ouverte en fiche, sans progression
        before_events = len(store.learning_events())
        n_w = len(Window.children)
        c_rows[2].dispatch("on_release")
        check(len(Window.children) > n_w, "correction ouverte en fiche")
        corr_fiches = [w for w in Window.children
                       if type(w).__name__ == "ContentFiche"]
        texts = [lbl.text for w in corr_fiches for lbl in _labels(w)]
        check(any("SOLUTION" in t for t in texts),
              "contenu de la correction affiché")
        check(any("Correction d'exercice" in t for t in texts),
              "méta « Correction d'exercice » affiché")
        check(len(store.learning_events()) == before_events,
              "ouverture d'une correction sans effet sur la progression")
        for w in corr_fiches:
            w.dismiss()

        # puce de langage : change de parcours aussi ici
        chip_rust = next(c for c in corr_screen.chips if c.text == "Rust")
        chip_rust.dispatch("on_release")
        check(corr_screen.lang == "Rust", "changement de langage (corrections)")
        c_rows = list(reversed(corr_screen.rows_box.children))
        check(len(c_rows) == 7 and all(isinstance(r, LinkRow) for r in c_rows),
              "lignes reconstruites pour Rust")
        next(c for c in corr_screen.chips if c.text == "Python").dispatch("on_release")
        check(corr_screen.lang == "Python", "retour au Python (corrections)")

        # --- brouillon « Mon essai » (fiche d'exercice) -------------------- #
        from kivy.uix.button import Button as _Button
        from kivy.uix.textinput import TextInput

        def _find(widget, cls):
            found = []
            for child in widget.children:
                if isinstance(child, cls):
                    found.append(child)
                found.extend(_find(child, cls))
            return found

        def _fiches():
            # les fermetures sont animées : une fiche fermée peut encore
            # traîner dans Window.children — on cherche par contenu,
            # jamais par position dans la liste
            return [w for w in Window.children
                    if type(w).__name__ == "ContentFiche"]

        def _fiche_avec(cls):
            for w in _fiches():
                if _find(w, cls):
                    return w
            return None

        def _fiche_titre(titre):
            for w in _fiches():
                if any(lbl.text == titre for lbl in _labels(w)):
                    return w
            return None

        # on repasse en Python (le parcours Formation était en JavaScript)
        next(c for c in learn.chips if c.text == "Python").dispatch("on_release")
        check(learn.lang == "Python", "retour en Python avant l'essai")

        slug_fz, title_fz, desc_fz = next(
            (s, t, d) for s, t, d in curriculum.items("Python", "exercises")
            if t == "FizzBuzz")
        check(store.get_draft("Python", slug_fz) == "", "aucun brouillon au départ")

        learn._open_fiche("exercises", slug_fz, title_fz, desc_fz)
        check(bool(_fiches()), "fiche d'exercice ouverte")
        fiche = _fiche_avec(TextInput)
        champs = _find(fiche, TextInput) if fiche else []
        check(len(champs) == 1, "espace « Mon essai » présent dans la fiche")
        btns = [b for w in _fiches() for b in _find(w, _Button)
                if b.text == "Voir la correction"]
        check(bool(btns), "bouton « Voir la correction » présent")

        if champs:
            champ = champs[0]
            champ.text = "for n in range(1, 101):\n    print(n)"
            fiche._draft_flush()  # enregistrement immédiat (flux synchrone)
            check(store.get_draft("Python", slug_fz).startswith("for n in"),
                  "brouillon enregistré dans le stockage")
            relearn2 = type(store)(path=store.path)
            check(relearn2.get_draft("Python", slug_fz).startswith("for n in"),
                  "brouillon relu depuis le JSON")

        for w in _fiches():
            w.dismiss()

        # réouverture : brouillon pré-rempli + correction ouvrable
        learn._open_fiche("exercises", slug_fz, title_fz, desc_fz)
        tis = [ti for w in _fiches() for ti in _find(w, TextInput)]
        check(bool(tis) and any(t.text.startswith("for n in") for t in tis),
              "brouillon pré-rempli à la réouverture")
        btns = [b for w in _fiches() for b in _find(w, _Button)
                if b.text == "Voir la correction"]
        if btns:
            n_avant = len(_fiches())
            btns[0].dispatch("on_release")
            check(len(_fiches()) == n_avant + 1,
                  "correction ouverte au-dessus de la fiche")
            txt_corr = [lbl.text for w in _fiches() for lbl in _labels(w)]
            check(any("SOLUTION" in t for t in txt_corr),
                  "texte de la correction affiché")

        for w in _fiches():
            w.dismiss()

        # un cours n'a pas d'espace d'essai
        _s0, _t0, _d0 = curriculum.items("Python", "lessons")[0]
        learn._open_fiche("lessons", _s0, _t0, _d0)
        fiche_cours = _fiche_titre(_t0)
        check(fiche_cours is not None and not _find(fiche_cours, TextInput),
              "fiche de cours sans espace d'essai")
        for w in _fiches():
            w.dismiss()

        # courbe d'évolution et libellés du graphique (Stats)
        stats_screen = app.screens["stats"]
        check(len(stats_screen.learn_chart.data) == 14,
              "courbe d'apprentissage sur 14 jours alimentée")
        check(any(lbl.text for lbl in stats_screen.chart._xlabels),
              "libellés de jours rendus (enfants du graphique)")

        # --- statistiques ------------------------------------------------- #
        from core import stats as st
        from datetime import date

        check(st.format_duration(3725) == "1 h 02 min", "format_duration heures")
        check(st.format_duration(200) == "3 min", "format_duration minutes")
        check(st.format_duration(45) == "45 s", "format_duration secondes")
        check(st.format_clock(3671) == "01:01:11", "format_clock")
        check(st.seconds_today(store.sessions) >= 0, "temps du jour")
        check(st.seconds_this_week(store.sessions) >= 0, "temps de la semaine")
        check(len(st.daily_series(store.sessions, 14)) == 14, "série de 14 jours")
        check(st.streak(store.sessions) >= 0, "série de jours calculée")
        check(st.totals_by_language(store.sessions), "répartition par langage")
        check(st.totals_by_project(store.sessions), "répartition par projet")
        best_day, best = st.best_day(store.sessions)
        check(best_day is None or isinstance(best_day, date), "meilleure journée")

        # --- apprentissage : stockage de la progression -------------------- #
        check(set(curriculum.LANGUAGES) == set(curriculum.CURRICULUM),
              f"parcours défini pour les {len(curriculum.LANGUAGES)} langages")
        check(curriculum.grand_total() >= 150,
              f"{curriculum.grand_total()} cours/exercices au total")
        py_lessons = curriculum.items("Python", "lessons")
        check(len({s for s, _, _ in py_lessons}) == len(py_lessons),
              "identifiants de cours uniques")

        slug0, title0, _ = py_lessons[0]
        store.set_item("Python", "lessons", slug0, title0, False)
        n0 = len(store.learning_events())
        check(not store.item_done("Python", "lessons", slug0), "élément décoché")
        store.set_item("Python", "lessons", slug0, title0, True)
        check(store.item_done("Python", "lessons", slug0), "élément coché")
        check(len(store.learning_events()) == n0 + 1, "jalon daté ajouté")
        check(store.learning_events()[-1]["title"] == title0, "jalon nommé")
        store.set_item("Python", "lessons", slug0, title0, False)
        check(len(store.learning_events()) == n0, "jalon retiré à la décoche")

        store.set_item("Python", "exercises", "fizzbuzz", "FizzBuzz", True)
        relearn = type(store)(path=store.path)
        check(relearn.item_done("Python", "exercises", "fizzbuzz"),
              "progression relue depuis le JSON")
        check(relearn.item_read("Python", "lessons", slug0),
              "lecture de la fiche relue depuis le JSON")
        check(not store.set_item_read("Python", "lessons", slug0),
              "seconde lecture : première date conservée")
        serie = st.learning_series(store.learning_events(), 14)
        check(len(serie) == 14 and serie[-1][1] == float(len(store.learning_events())),
              "courbe cumulative = jalons actuels")
        check(st.learning_series([], 5)[-1][1] == 0.0, "courbe vide à zéro")

        # --- objectifs & réglages ---------------------------------------- #
        store.set_goals(90, 700)
        check(store.goals["daily_minutes"] == 90, "objectif quotidien enregistré")
        store.set_settings(reminder_enabled=True, reminder_time="21:30")
        check(store.settings["reminder_time"] == "21:30", "rappel enregistré")

        # --- exports ------------------------------------------------------ #
        from core import export as exporter

        exporter.export_dir = lambda: tmp_dir
        csv_path = exporter.export_csv(store.sessions)
        json_path = exporter.export_json(store.sessions)
        check(os.path.exists(csv_path) and os.path.getsize(csv_path) > 0, "export CSV")
        check(os.path.exists(json_path) and os.path.getsize(json_path) > 0, "export JSON")

        # --- dialogue ------------------------------------------------------ #
        from kivy.core.window import Window
        from kivy.uix.button import Button
        from ui.dialogs import AppDialog, confirm

        global DLG_CHILDREN_BEFORE
        dlg = AppDialog("Titre", "Message\nsur deux lignes", actions=[("OK", True, lambda: None)])
        DLG_CHILDREN_BEFORE = len(Window.children)
        dlg.open()
        check(len(Window.children) > DLG_CHILDREN_BEFORE, "ouverture d'un dialogue")
        dlg.dismiss()  # fermeture animée : vérifiée plus bas dans finish()

        called = {"n": 0}
        cd = confirm("Confirmer ?", "message", on_yes=lambda: called.__setitem__("n", called["n"] + 1))

        def _buttons(widget):
            found = []
            for child in widget.children:
                if isinstance(child, Button):
                    found.append(child)
                found.extend(_buttons(child))
            return found

        primary = [b for b in _buttons(cd) if b.text == "Confirmer"]
        check(bool(primary), "dialogue de confirmation construit")
        if primary:
            primary[0].dispatch("on_release")
            check(called["n"] == 1, "action du bouton de confirmation déclenchée")
        # --- persistance ---------------------------------------------------- #
        reloaded = type(store)(path=store.path)
        check(len(reloaded.sessions) == len(store.sessions), "rechargement du fichier JSON")
        check(reloaded.goals["daily_minutes"] == 90, "objectifs relus")
        check(reloaded.settings["reminder_enabled"] is True, "réglages relus")

        # --- suppression ---------------------------------------------------- #
        victim = store.sessions[0].id
        check(store.delete(victim), "suppression d'une session")
        check(not store.delete(victim), "suppression d'un id inconnu")

        app.refresh_chrome()
        check(bool(app.today_lbl.text), "barre d'état mise à jour")
    except Exception:
        traceback.print_exc()
        FAILURES.append("exception non gérée")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        Clock.schedule_once(finish, 0.8)


def finish(_dt: float) -> None:
    """Vérifications qui demandent d'attendre une animation, puis récapitulatif."""
    if DLG_CHILDREN_BEFORE is not None:
        from kivy.core.window import Window

        # La fermeture animée des fenêtres ne progresse pas pendant le gel
        # transitoire de la boucle d'événements causé par le redimensionnement
        # asynchrone de la fenêtre : on attend qu'aucun dialogue (AppDialog
        # ou ContentFiche) ne reste ouvert (25 essais × 0,2 s maximum).
        pending = [type(w).__name__ for w in Window.children
                   if type(w).__name__ in ("AppDialog", "ContentFiche")]
        if pending and DLG_TRIES["n"] < 25:
            DLG_TRIES["n"] += 1
            Clock.schedule_once(finish, 0.2)
            return
        check(not pending,
              f"fermeture des dialogues (encore ouverts : {pending}, "
              f"essai {DLG_TRIES['n']}, fenêtre = "
              f"{[type(w).__name__ for w in Window.children]})")
    print("\n" + "=" * 46)
    print("ECHECS : " + (", ".join(FAILURES) if FAILURES else "aucun"))
    app.stop()


app = BabiProgrammeur()
Clock.schedule_once(lambda _dt: scenario(app, _dt), 1.5)
app.run()
sys.exit(1 if FAILURES else 0)
