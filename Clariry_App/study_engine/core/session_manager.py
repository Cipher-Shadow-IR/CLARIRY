# study_engine/core/session_manager.py
# ─────────────────────────────────────
# SessionManager — thin coordinator between StateManager, ParaStore, and GUIExplanationPlayer.
# The GUI calls this instead of directly touching lower-level components.

from __future__ import annotations
from study_engine.state_manager import StateManager
from study_engine.paragraph_store import ParaStore


class SessionManager:
    """
    Manages the current study session:
    - Tracks which document is loaded
    - Provides a single point for paragraph retrieval
    - Delegates navigation to StateManager
    """

    def __init__(self, store: ParaStore, state: StateManager):
        self._store = store
        self._state = state
        self._explained: set[int] = set()

    # ── Navigation ───────────────────────────────────────────────────────

    def current_index(self) -> int:
        return self._state.current()

    def current_paragraph(self) -> str | None:
        return self._store.get_para(self._state.current())

    def go_to(self, index: int) -> str | None:
        if 0 <= index < self._store.total_para():
            self._state._cur_index = index
        return self.current_paragraph()

    def next(self) -> str | None:
        self._state.next()
        return self.current_paragraph()

    def previous(self) -> str | None:
        self._state.previous()
        return self.current_paragraph()

    # ── Explained tracking ───────────────────────────────────────────────

    def mark_explained(self, index: int):
        self._explained.add(index)

    def explained_indices(self) -> list[int]:
        return sorted(self._explained)

    # ── Info ─────────────────────────────────────────────────────────────

    def total(self) -> int:
        return self._store.total_para()

    def file_path(self) -> str:
        return self._store.file_path
