"""Données de démonstration (--demo) pour prévisualiser l'application."""
from __future__ import annotations

import random
import time
from datetime import date, timedelta
from typing import Tuple

from core.models import Session
from core.storage import SessionStore

_LANGS = [
    ("Python", 0.35),
    ("JavaScript", 0.20),
    ("TypeScript", 0.12),
    ("SQL", 0.10),
    ("Rust", 0.08),
    ("HTML/CSS", 0.07),
    ("Java", 0.05),
    ("C++", 0.03),
]

_PROJECTS = [
    "API REST",
    "App mobile",
    "Refactoring",
    "Bug fixing",
    "Data pipeline",
    "Portfolio",
]


def _pick_language() -> str:
    r = random.random()
    acc = 0.0
    for name, weight in _LANGS:
        acc += weight
        if r <= acc:
            return name
    return _LANGS[0][0]


def seed(store: SessionStore, days: int = 21, per_day: Tuple[int, int] = (1, 3)) -> int:
    """Génère des sessions réparties sur `days` jours. Retourne le nombre créées."""
    random.seed()
    created = 0
    for offset in range(days, 0, -1):
        day = date.today() - timedelta(days=offset)
        if day.weekday() == 6 and random.random() < 0.6:  # repos le dimanche
            continue
        for _ in range(random.randint(*per_day)):
            start_hour = random.randint(9, 21)
            start_min = random.randint(0, 59)
            started = time.mktime(
                (day.year, day.month, day.day, start_hour, start_min, 0, 0, 0, -1)
            )
            if started > time.time():
                continue
            duration = random.randint(15, 150) * 60
            store.sessions.append(
                Session(
                    project=random.choice(_PROJECTS),
                    language=_pick_language(),
                    notes=random.choice(["", "", "Avancement correct", "Bloqué sur un bug", "Revue de code"]),
                    started_at=started,
                    duration=duration,
                )
            )
            created += 1
    # Une session en cours pour montrer le chrono.
    if not store.is_running:
        store.active = {
            "started_at": time.time() - 487,
            "project": "App mobile",
            "language": "Python",
            "notes": "Session de démonstration",
        }
    store.sessions.sort(key=lambda s: s.started_at, reverse=True)
    _seed_learning(store)
    store.save()
    return created


def _seed_learning(store: SessionStore) -> None:
    """Cours/exercices terminés échelonnés sur les ~10 derniers jours (démo).

    Donne à voir la courbe d'évolution de l'onglet Stats dès le premier
    lancement en mode démonstration. Sans effet si une progression existe
    déjà.
    """
    if store.learning.get("progress"):
        return
    from core import curriculum

    progress = store.learning.setdefault("progress", {})
    events = store.learning.setdefault("events", [])
    # (langage, type, nombre d'éléments, jours avant aujourd'hui pour le 1er)
    plan = [
        ("Python", "lessons", 5, 11),
        ("Python", "exercises", 3, 6),
        ("JavaScript", "lessons", 3, 7),
        ("HTML/CSS", "lessons", 2, 4),
        ("HTML/CSS", "exercises", 2, 2),
        ("Flutter", "lessons", 2, 3),
    ]
    for lang, kind, count, days_ago in plan:
        items = curriculum.items(lang, kind)
        bucket = progress.setdefault(lang, {}).setdefault(kind, {})
        for i, (slug, title, _desc) in enumerate(items[:count]):
            bucket[slug] = 1
            day = date.today() - timedelta(days=max(0, days_ago - i * 2))
            events.append({
                "date": day.isoformat(),
                "lang": lang,
                "kind": kind,
                "slug": slug,
                "title": title,
            })
    events.sort(key=lambda e: e["date"])
