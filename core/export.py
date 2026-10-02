"""Export des sessions vers CSV / JSON."""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from typing import List

from kivy.utils import platform

from core.models import Session

CSV_COLUMNS = ["id", "date", "debut", "fin", "projet", "langage", "duree_s", "duree", "notes"]


def _fmt(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def export_dir() -> str:
    """Répertoire d'export accessible par l'utilisateur."""
    if platform == "win":
        docs = os.path.expanduser(os.path.join("~", "Documents"))
        return docs if os.path.isdir(docs) else os.path.expanduser("~")
    if platform == "macosx":
        docs = os.path.expanduser(os.path.join("~", "Documents"))
        return docs if os.path.isdir(docs) else os.path.expanduser("~")
    docs = os.path.expanduser(os.path.join("~", "Documents"))
    if os.path.isdir(docs):
        return docs
    docs = os.path.expanduser(os.path.join("~", "Export"))
    os.makedirs(docs, exist_ok=True)
    return docs


def _target(ext: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(export_dir(), f"babiprogrammeur-{stamp}.{ext}")


def export_json(sessions: List[Session]) -> str:
    path = _target("json")
    payload = [s.to_dict() for s in sessions]
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return path


def export_csv(sessions: List[Session]) -> str:
    path = _target("csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for s in sessions:
            writer.writerow(
                {
                    "id": s.id,
                    "date": datetime.fromtimestamp(s.started_at).strftime("%Y-%m-%d"),
                    "debut": _fmt(s.started_at),
                    "fin": _fmt(s.end_at),
                    "projet": s.project,
                    "langage": s.language,
                    "duree_s": int(s.duration),
                    "duree": f"{int(s.duration) // 3600:02d}:{(int(s.duration) % 3600) // 60:02d}:{int(s.duration) % 60:02d}",
                    "notes": s.notes,
                }
            )
    return path
