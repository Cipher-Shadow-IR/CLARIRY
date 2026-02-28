# study_engine/explainer/__init__.py
# ────────────────────────────────────
# Re-exports AIExplainer as `Explainer` so existing code that does
# `from study_engine.explainer import Explainer` works without changes.

from study_engine.explainer.ai_explainer import AIExplainer as Explainer

__all__ = ["Explainer", "AIExplainer"]
