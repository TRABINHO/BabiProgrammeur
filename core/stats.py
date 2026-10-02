"""Statistiques calculées à partir des sessions enregistrées."""
from __future__ import annotations

from datetime import date, datetime, time as dtime, timedelta
from typing import Iterable, List, Tuple

from core.models import Session

STREAK_MIN_SECONDS = 60  # une journée "comptée" = au moins 1 min de code


# ---------------------------------------------------------------------- #
# Formatage
# ---------------------------------------------------------------------- #
def format_duration(seconds: float) -> str:
    """'1 h 24 min', '42 min', '12 s'."""
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds} s"
    minutes = seconds // 60
    hours, minutes = divmod(minutes, 60)
    if hours and minutes:
        return f"{hours} h {minutes:02d} min"
    if hours:
        return f"{hours} h"
    return f"{minutes} min"


def format_clock(seconds: float) -> str:
    """'01:24:07' — chrono affiché."""
    seconds = max(0, int(seconds))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# ---------------------------------------------------------------------- #
# Agrégats
# ---------------------------------------------------------------------- #
def total_seconds(sessions: Iterable[Session]) -> float:
    return sum(s.duration for s in sessions)


def day_start(d: date) -> float:
    return datetime.combine(d, dtime.min).timestamp()


def day_end(d: date) -> float:
    return datetime.combine(d + timedelta(days=1), dtime.min).timestamp()


def in_day(s: Session, d: date) -> bool:
    return day_start(d) <= s.started_at < day_end(d)


def seconds_on(sessions: Iterable[Session], d: date) -> float:
    return sum(s.duration for s in sessions if in_day(s, d))


def week_bounds(today: date | None = None) -> Tuple[date, date]:
    """Semaine ISO (lundi -> dimanche)."""
    today = today or date.today()
    start = today - timedelta(days=today.weekday())
    return start, start + timedelta(days=6)


def seconds_today(sessions: Iterable[Session], today: date | None = None) -> float:
    return seconds_on(sessions, today or date.today())


def seconds_this_week(sessions: Iterable[Session], today: date | None = None) -> float:
    start, end = week_bounds(today)
    return sum(s.duration for s in sessions if day_start(start) <= s.started_at < day_end(end))


def seconds_this_month(sessions: Iterable[Session], today: date | None = None) -> float:
    today = today or date.today()
    start = today.replace(day=1)
    return sum(s.duration for s in sessions if s.started_at >= day_start(start))


def active_days(sessions: Iterable[Session]) -> int:
    return len({s.day for s in sessions})


def daily_series(sessions: List[Session], days: int = 14, today: date | None = None) -> List[Tuple[date, float]]:
    """Séquence (jour, secondes) des `days` derniers jours, du plus ancien à aujourd'hui."""
    today = today or date.today()
    totals = {}
    for s in sessions:
        totals[s.day] = totals.get(s.day, 0.0) + s.duration
    return [(today - timedelta(days=days - 1 - i), totals.get(today - timedelta(days=days - 1 - i), 0.0))
            for i in range(days)]


def totals_by_language(sessions: Iterable[Session]) -> List[Tuple[str, float]]:
    """[(langage, secondes)] trié par temps décroissant."""
    totals: dict = {}
    for s in sessions:
        key = s.language.strip() or "Non renseigné"
        totals[key] = totals.get(key, 0.0) + s.duration
    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)


def totals_by_project(sessions: Iterable[Session], limit: int = 5) -> List[Tuple[str, float]]:
    totals: dict = {}
    for s in sessions:
        key = s.project.strip() or "Sans projet"
        totals[key] = totals.get(key, 0.0) + s.duration
    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:limit]


def streak(sessions: Iterable[Session], today: date | None = None) -> int:
    """Nombre de jours consécutifs avec >= 1 min de code (aujourd'hui ou hier en tête)."""
    days = {s.day for s in sessions if s.duration >= STREAK_MIN_SECONDS}
    if not days:
        return 0
    today = today or date.today()
    cursor = today if today in days else today - timedelta(days=1)
    if cursor not in days:
        return 0
    count = 0
    while cursor in days:
        count += 1
        cursor -= timedelta(days=1)
    return count


def best_day(sessions: Iterable[Session]) -> Tuple[date | None, float]:
    totals: dict = {}
    for s in sessions:
        totals[s.day] = totals.get(s.day, 0.0) + s.duration
    if not totals:
        return None, 0.0
    day = max(totals, key=lambda d: totals[d])
    return day, totals[day]


def learning_series(events: Iterable[dict], days: int = 14,
                    today: date | None = None) -> List[Tuple[date, float]]:
    """Cumul (jour, éléments d'apprentissage terminés) sur `days` jours.

    Chaque événement porte une date ISO ("AAAA-MM-JJ") : le tri lexicographique
    vaut tri chronologique. La courbe est cumulative — on voit « l'évolution »
    de l'apprentissage, pas seulement le total actuel.
    """
    today = today or date.today()
    dates = sorted(e["date"] for e in events
                   if isinstance(e, dict) and isinstance(e.get("date"), str))
    out: List[Tuple[date, float]] = []
    for i in range(days):
        d = today - timedelta(days=days - 1 - i)
        key = d.isoformat()
        out.append((d, float(sum(1 for k in dates if k <= key))))
    return out
