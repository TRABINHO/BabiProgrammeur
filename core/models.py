"""Modèles de données de BabiProgrammeur."""
from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import date, datetime


@dataclass
class Session:
    """Une session de programmation chronométrée."""

    project: str = ""
    language: str = ""
    notes: str = ""
    started_at: float = field(default_factory=time.time)
    duration: float = 0.0  # en secondes
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    # ------------------------------------------------------------------ #
    @property
    def end_at(self) -> float:
        return self.started_at + self.duration

    @property
    def started_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.started_at)

    @property
    def day(self) -> "date":
        """Date locale (jour) du début de la session."""
        return datetime.fromtimestamp(self.started_at).date()

    @classmethod
    def from_dict(cls, d: dict) -> "Session":
        """Construit une session à partir d'un dict JSON, en ignorant les clés inconnues."""
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})

    def to_dict(self) -> dict:
        return asdict(self)
