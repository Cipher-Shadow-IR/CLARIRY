# study_engine/persistence/progress_store.py
# ────────────────────────────────────────────
# Saves and loads learning progress to/from a local JSON file.
# Keeps track of: last paragraph index, resume points per paragraph,
# and which paragraphs have been fully explained.

from __future__ import annotations
import json
import os
from datetime import datetime


_DEFAULT_PATH = "data/progress.json"


class ProgressStore:
    """
    Persists study session progress to disk.

    Schema (JSON):
    {
        "document": "path/to/file.pdf",
        "last_paragraph": 3,
        "resume_points": { "0": 2, "3": 1 },
        "explained": [0, 1, 2],
        "last_session": "2026-02-27T22:00:00"
    }
    """

    def __init__(self, save_path: str = _DEFAULT_PATH):
        self._path = save_path
        self._data: dict = {}

    # ── Load ─────────────────────────────────────────────────────────────

    def load(self, document_path: str) -> dict:
        """Load progress for a given document. Returns empty dict if none."""
        if not os.path.exists(self._path):
            return {}
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                stored = json.load(f)
            if stored.get("document") == document_path:
                self._data = stored
                return stored
        except (json.JSONDecodeError, OSError):
            pass
        return {}

    # ── Save ─────────────────────────────────────────────────────────────

    def save(
        self,
        document_path: str,
        last_paragraph: int,
        resume_points: dict[int, int],
        explained: list[int],
    ):
        self._data = {
            "document": document_path,
            "last_paragraph": last_paragraph,
            "resume_points": {str(k): v for k, v in resume_points.items()},
            "explained": sorted(set(explained)),
            "last_session": datetime.now().isoformat(timespec="seconds"),
        }
        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    # ── Helpers ───────────────────────────────────────────────────────────

    def get_last_paragraph(self) -> int:
        return self._data.get("last_paragraph", 0)

    def get_resume_points(self) -> dict[int, int]:
        raw = self._data.get("resume_points", {})
        return {int(k): v for k, v in raw.items()}

    def get_explained(self) -> list[int]:
        return self._data.get("explained", [])
