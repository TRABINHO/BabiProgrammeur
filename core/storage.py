"""Stockage local JSON de BabiProgrammeur (aucun serveur, aucune donnée envoyée)."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from datetime import date
from typing import Optional, Tuple

from kivy.utils import platform

from core.models import Session

APP_DIR_NAME = "BabiProgrammeur"
# Ancien nom du dossier de données (avant renommage) : migré au premier lancement.
LEGACY_APP_DIR_NAME = "CodePulse"

DEFAULT_GOALS = {
    "daily_minutes": 120,
    "weekly_minutes": 600,
}

DEFAULT_SETTINGS = {
    "reminder_enabled": False,
    "reminder_time": "20:00",
    "last_reminder_day": "",
}

# Progression d'apprentissage :
#   {"progress": {langage: {"lessons": {slug: 1}, "exercises": {slug: 1}}},
#    "events":   [{"date": "AAAA-MM-JJ", "lang", "kind", "slug", "title"}]}
# Les événements datent chaque élément coché (courbe d'évolution) ; ils sont
# retirés si l'utilisateur décoche, pour rester cohérent avec la progression.
DEFAULT_LEARNING = {"progress": {}, "events": []}


def _dir_for(name: str) -> str:
    if platform == "android":
        try:
            from android.storage import app_storage_path

            return app_storage_path()
        except Exception:  # pragma: no cover - repli
            pass
    if platform == "win":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        return os.path.join(base, name)
    if platform == "macosx":
        return os.path.expanduser(os.path.join("~", "Library", "Application Support", name))
    return os.path.expanduser(os.path.join("~", "." + name.lower()))


def data_dir() -> str:
    """Répertoire local où vivent les données de l'application."""
    return _dir_for(APP_DIR_NAME)


def default_file() -> str:
    path = os.path.join(data_dir(), "data.json")
    _migrate_legacy(path)
    return path


def _migrate_legacy(new_file: str) -> None:
    """Déplace les données de l'ancien dossier (nom précédent de l'app).

    Si un fichier existe déjà sous le nouveau nom, il fait foi : rien n'est touché.
    """
    if platform == "android" or os.path.exists(new_file):
        return
    old_file = os.path.join(_dir_for(LEGACY_APP_DIR_NAME), "data.json")
    if not os.path.exists(old_file):
        return
    try:
        os.makedirs(os.path.dirname(new_file), exist_ok=True)
        shutil.move(old_file, new_file)
    except OSError:  # pragma: no cover - échec silencieux, on repart de zéro
        pass


def _clean_learning(raw) -> dict:
    """Valide la structure « learning » lue du JSON (tolère l'absence, anciens
    fichiers sans cette clé et valeurs inattendues)."""
    if not isinstance(raw, dict):
        return {"progress": {}, "read": {}, "events": []}

    def _clean_marks(raw_marks, with_date: bool) -> dict:
        """{langage: {kind: {slug: ...}}} — valeurs simplifiées (1 ou date)."""
        out: dict = {}
        if not isinstance(raw_marks, dict):
            return out
        for lang, kinds in raw_marks.items():
            if not isinstance(lang, str) or not isinstance(kinds, dict):
                continue
            clean_kinds: dict = {}
            for kind, slugs in kinds.items():
                if kind not in ("lessons", "exercises") or not isinstance(slugs, dict):
                    continue
                if with_date:
                    clean_kinds[kind] = {
                        s: (v if isinstance(v, str) and v else "1")
                        for s, v in slugs.items() if isinstance(s, str) and v
                    }
                else:
                    clean_kinds[kind] = {s: 1 for s, v in slugs.items()
                                         if isinstance(s, str) and v}
            if clean_kinds:
                out[lang] = clean_kinds
        return out

    progress: dict = _clean_marks(raw.get("progress"), with_date=False)
    # « read » : date d'ouverture de la fiche (la coche exige cette lecture)
    read: dict = _clean_marks(raw.get("read"), with_date=True)

    events: list = []
    raw_events = raw.get("events")
    if isinstance(raw_events, list):
        for ev in raw_events:
            if not isinstance(ev, dict):
                continue
            if not all(isinstance(ev.get(k), str) for k in ("date", "lang", "kind", "slug")):
                continue
            events.append({
                "date": ev["date"],
                "lang": ev["lang"],
                "kind": ev["kind"],
                "slug": ev["slug"],
                "title": str(ev.get("title", "")),
            })
    events.sort(key=lambda e: e["date"])
    return {"progress": progress, "read": read, "events": events}


def _clean_drafts(raw) -> dict:
    """{langage: {slug: texte}} — seules les chaînes non vides sont gardées."""
    if not isinstance(raw, dict):
        return {}
    out = {}
    for lang, items in raw.items():
        if not isinstance(items, dict):
            continue
        keep = {slug: text for slug, text in items.items()
                if isinstance(slug, str) and isinstance(text, str)
                and text.strip()}
        if keep:
            out[str(lang)] = keep
    return out


class SessionStore:
    """Charge / sauvegarde les sessions, objectifs et réglages."""

    def __init__(self, path: Optional[str] = None):
        self.path = path or default_file()
        self.sessions: list[Session] = []
        self.active: Optional[dict] = None  # {"started_at", "project", "language", "notes"}
        self.goals: dict = dict(DEFAULT_GOALS)
        self.settings: dict = dict(DEFAULT_SETTINGS)
        self.learning: dict = _clean_learning(None)
        self.drafts: dict = {}
        self.load()

    # ------------------------------------------------------------------ #
    # Persistance
    # ------------------------------------------------------------------ #
    def load(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, ValueError):
            # Fichier corrompu : on garde une copie de côté plutôt que d'écraser.
            try:
                shutil.copy(self.path, self.path + ".corrupt")
            except OSError:
                pass
            return

        self.sessions = [Session.from_dict(d) for d in raw.get("sessions", []) if isinstance(d, dict)]
        self.sessions.sort(key=lambda s: s.started_at, reverse=True)
        self.active = raw.get("active") if isinstance(raw.get("active"), dict) else None
        self.goals = {**DEFAULT_GOALS, **raw.get("goals", {})}
        self.settings = {**DEFAULT_SETTINGS, **raw.get("settings", {})}
        self.learning = _clean_learning(raw.get("learning"))
        self.drafts = _clean_drafts(raw.get("drafts"))

    def save(self) -> None:
        payload = {
            "version": 1,
            "updated_at": time.time(),
            "sessions": [s.to_dict() for s in self.sessions],
            "active": self.active,
            "goals": self.goals,
            "settings": self.settings,
            "learning": self.learning,
            "drafts": self.drafts,
        }
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        # Écriture atomique : on écrit à côté puis on remplace.
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(self.path), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
            shutil.move(tmp, self.path)
        except OSError:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise

    # ------------------------------------------------------------------ #
    # Chronomètre
    # ------------------------------------------------------------------ #
    @property
    def is_running(self) -> bool:
        return self.active is not None

    @property
    def active_elapsed(self) -> float:
        if not self.active:
            return 0.0
        return max(0.0, time.time() - float(self.active.get("started_at", 0)))

    def start(self, project: str, language: str, notes: str = "") -> None:
        if self.is_running:
            raise RuntimeError("Une session est déjà en cours.")
        self.active = {
            "started_at": time.time(),
            "project": project.strip(),
            "language": language.strip(),
            "notes": notes.strip(),
        }
        self.save()

    def update_active(self, **fields) -> None:
        if not self.is_running:
            return
        for key in ("project", "language", "notes"):
            if key in fields:
                self.active[key] = (fields[key] or "").strip()
        self.save()

    def stop(self) -> Optional[Session]:
        """Arrête la session en cours et l'enregistre."""
        if not self.active:
            return None
        started = float(self.active.get("started_at", 0))
        session = Session(
            project=self.active.get("project", ""),
            language=self.active.get("language", ""),
            notes=self.active.get("notes", ""),
            started_at=started,
            duration=max(1.0, time.time() - started),
        )
        self.active = None
        self.sessions.insert(0, session)
        self.save()
        return session

    def cancel_active(self) -> None:
        self.active = None
        self.save()

    # ------------------------------------------------------------------ #
    # Sessions
    # ------------------------------------------------------------------ #
    def add(self, session: Session) -> None:
        self.sessions.insert(0, session)
        self.save()

    def delete(self, session_id: str) -> bool:
        before = len(self.sessions)
        self.sessions = [s for s in self.sessions if s.id != session_id]
        if len(self.sessions) != before:
            self.save()
            return True
        return False

    # ------------------------------------------------------------------ #
    # Objectifs & réglages
    # ------------------------------------------------------------------ #
    def set_goals(self, daily_minutes: int, weekly_minutes: int) -> None:
        self.goals["daily_minutes"] = max(0, int(daily_minutes))
        self.goals["weekly_minutes"] = max(0, int(weekly_minutes))
        self.save()

    def set_settings(self, **fields) -> None:
        self.settings.update(fields)
        self.save()

    # ------------------------------------------------------------------ #
    # Apprentissage (cours & exercices)
    # ------------------------------------------------------------------ #
    def item_done(self, lang: str, kind: str, slug: str) -> bool:
        """True si l'élément est coché pour ce langage."""
        bucket = self.learning.get("progress", {}).get(lang, {}).get(kind, {})
        return bool(bucket.get(slug))

    def set_item(self, lang: str, kind: str, slug: str, title: str, done: bool) -> None:
        """Coche / décoche un élément ; date le jalon (ou le retire) et sauvegarde."""
        bucket = (self.learning.setdefault("progress", {})
                  .setdefault(lang, {})
                  .setdefault(kind, {}))
        events = self.learning.setdefault("events", [])
        same = lambda e: (e.get("lang") == lang and e.get("kind") == kind
                          and e.get("slug") == slug)
        if done:
            bucket[slug] = 1
            if not any(same(e) for e in events):
                events.append({
                    "date": date.today().isoformat(),
                    "lang": lang,
                    "kind": kind,
                    "slug": slug,
                    "title": title,
                })
        else:
            bucket.pop(slug, None)
            events[:] = [e for e in events if not same(e)]
        self.save()

    def item_read(self, lang: str, kind: str, slug: str) -> bool:
        """True si la fiche de l'élément a été ouverte au moins une fois."""
        bucket = self.learning.get("read", {}).get(lang, {}).get(kind, {})
        return bool(bucket.get(slug))

    def set_item_read(self, lang: str, kind: str, slug: str) -> bool:
        """Marque la fiche comme lue (date du jour) ; sauvegarde si nouveau.

        Renvoie True si l'élément venait d'être lu pour la première fois —
        la coche d'un cours n'est autorisée qu'après cette lecture."""
        bucket = (self.learning.setdefault("read", {})
                  .setdefault(lang, {})
                  .setdefault(kind, {}))
        if slug in bucket:
            return False
        bucket[slug] = date.today().isoformat()
        self.save()
        return True

    def learning_counts(self, lang: Optional[str] = None) -> Tuple[int, int]:
        """(cours terminés, exercices terminés) — tous langages si lang est vide."""
        progress = self.learning.get("progress", {})
        names = [lang] if lang else list(progress)
        lessons = exercises = 0
        for name in names:
            kinds = progress.get(name, {})
            lessons += sum(1 for v in kinds.get("lessons", {}).values() if v)
            exercises += sum(1 for v in kinds.get("exercises", {}).values() if v)
        return lessons, exercises

    def learning_events(self) -> list:
        """Jalons datés, du plus ancien au plus récent."""
        return sorted(self.learning.get("events", []), key=lambda e: e.get("date", ""))

    # ------------------------------------------------------------------ #
    # Brouillons « Mon essai » (fiches d'exercice, onglet Formation)
    # ------------------------------------------------------------------ #
    def get_draft(self, lang: str, slug: str) -> str:
        """Texte enregistré pour l'exercice, « » si aucun brouillon."""
        return self.drafts.get(lang, {}).get(slug, "")

    def set_draft(self, lang: str, slug: str, text: str) -> None:
        """Enregistre le brouillon de l'exercice ; un texte vidé l'efface."""
        items = dict(self.drafts.get(lang, {}))
        if items.get(slug, "") == text:
            return
        if text.strip():
            items[slug] = text
        else:
            items.pop(slug, None)
        if items:
            self.drafts[lang] = items
        else:
            self.drafts.pop(lang, None)
        self.save()

    def clear_all(self) -> None:
        self.sessions = []
        self.active = None
        self.goals = dict(DEFAULT_GOALS)
        self.settings = dict(DEFAULT_SETTINGS)
        self.learning = _clean_learning(None)
        self.drafts = {}
        self.save()
