# study_engine/paragraph_store.py
# ─────────────────────────────────
# Loads study content from .txt or .pdf files.
# .pdf files are parsed via PyMuPDF (fitz) — no internet required.

from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass
class ParagraphSource:
    page_index: int | None = None
    rect: tuple[float, float, float, float] | None = None


class ParaStore:
    """
    Loads a study document and exposes it as a list of paragraph strings.

    Supported formats:
      .txt  — paragraphs separated by blank lines
      .pdf  — text extracted page-by-page, then split into paragraphs
    """

    def __init__(self, file_path: str):
        self._paras: list[str] = []
        self._sources: list[ParagraphSource] = []
        self._file_path = file_path
        self._is_pdf = False
        self._load(file_path)

    # ── Public API ───────────────────────────────────────────────────────

    def get_para(self, para_id: int) -> str | None:
        if para_id < 0 or para_id >= len(self._paras):
            return None
        return self._paras[para_id]

    def total_para(self) -> int:
        return len(self._paras)

    def all_paras(self) -> list[str]:
        return list(self._paras)

    def get_source(self, para_id: int) -> ParagraphSource | None:
        if para_id < 0 or para_id >= len(self._sources):
            return None
        return self._sources[para_id]

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def is_pdf(self) -> bool:
        return self._is_pdf

    # ── Loaders ──────────────────────────────────────────────────────────

    def _load(self, path: str):
        ext = os.path.splitext(path)[1].lower()
        self._is_pdf = ext == ".pdf"
        if ext == ".pdf":
            self._load_pdf(path)
        else:
            self._load_txt(path)

    def _load_txt(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        self._paras = self._split_paragraphs(raw)
        self._sources = [ParagraphSource() for _ in self._paras]

    def _load_pdf(self, path: str):
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF is required for PDF support. "
                "Run: pip install PyMuPDF"
            )

        with fitz.open(path) as doc:
            paragraphs: list[str] = []
            sources: list[ParagraphSource] = []
            for page_index, page in enumerate(doc):
                blocks = [
                    b for b in page.get_text("blocks")
                    if len(b) >= 5 and str(b[4]).strip()
                ]
                blocks.sort(key=lambda b: (round(float(b[1]), 1), round(float(b[0]), 1)))

                current_text: list[str] = []
                current_rect: tuple[float, float, float, float] | None = None
                prev_bottom: float | None = None

                def flush_current():
                    nonlocal current_text, current_rect, prev_bottom
                    if not current_text or not current_rect:
                        current_text = []
                        current_rect = None
                        prev_bottom = None
                        return
                    cleaned = " ".join(" ".join(current_text).split())
                    if len(cleaned) > 40:
                        paragraphs.append(cleaned)
                        sources.append(
                            ParagraphSource(page_index=page_index, rect=current_rect)
                        )
                    current_text = []
                    current_rect = None
                    prev_bottom = None

                for block in blocks:
                    x0, y0, x1, y1, text, *_ = block
                    block_text = " ".join(str(text).split())
                    if not block_text:
                        continue

                    if prev_bottom is not None and (float(y0) - prev_bottom) > 18.0:
                        flush_current()

                    if current_rect is None:
                        current_rect = (float(x0), float(y0), float(x1), float(y1))
                    else:
                        cx0, cy0, cx1, cy1 = current_rect
                        current_rect = (
                            min(cx0, float(x0)),
                            min(cy0, float(y0)),
                            max(cx1, float(x1)),
                            max(cy1, float(y1)),
                        )

                    current_text.append(block_text)
                    prev_bottom = float(y1)

                flush_current()
        self._paras = paragraphs
        self._sources = sources

    def _split_paragraphs(self, text: str) -> list[str]:
        """Split on blank lines; discard very short fragments."""
        chunks = text.split("\n\n")
        result = []
        for chunk in chunks:
            cleaned = " ".join(chunk.split())  # normalise whitespace
            if len(cleaned) > 40:              # skip headers, page numbers etc.
                result.append(cleaned)
        return result
