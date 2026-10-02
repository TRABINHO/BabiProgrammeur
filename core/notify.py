"""Notifications locales (plyer si disponible, sinon silencieux)."""
from __future__ import annotations


def notify(title: str, message: str) -> bool:
    """Envoie une notification système. Retourne False si indisponible."""
    try:
        from plyer import notification

        notification.notify(title=title, message=message, timeout=10)
        return True
    except Exception:
        return False


def can_notify() -> bool:
    try:
        import plyer  # noqa: F401

        return True
    except Exception:
        return False
