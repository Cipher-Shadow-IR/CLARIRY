# study_engine/explainer/ai_explainer.py
# ───────────────────────────────────────
# Calls local Ollama LLM via subprocess for offline inference.
# All prompts are imported from prompt_templates.py.

import subprocess
from study_engine.explainer.prompt_templates import (
    explain_paragraph,
    explain_doubt,
    format_exam,
)


class AIExplainer:
    """
    Wraps Ollama CLI to generate spoken explanations and exam notes.
    All calls are blocking — run from a background thread via TTSWorker.
    """

    def __init__(self, model_name: str = "llama3:latest"):
        self._model = model_name

    # ── Public API ───────────────────────────────────────────────────────

    def explain(self, paragraph_text: str) -> str:
        """Return a short conversational explanation of the paragraph."""
        prompt = explain_paragraph(paragraph_text)
        return self._call_ollama(prompt)

    def explain_doubt(self, selected_text: str) -> str:
        """Return a focused explanation of the passage the student didn't understand."""
        prompt = explain_doubt(selected_text)
        return self._call_ollama(prompt)

    def explain_exam(self, paragraph_text: str) -> str:
        """Return exam-ready bullet points for the paragraph."""
        prompt = format_exam(paragraph_text)
        return self._call_ollama(prompt)

    # ── Internal ─────────────────────────────────────────────────────────

    def _call_ollama(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self._model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=120,      # max 2 min; local models can be slow
            )
            output = result.stdout.strip()
            if not output and result.stderr:
                return f"[Ollama error: {result.stderr.strip()[:200]}]"
            return output
        except FileNotFoundError:
            return (
                "[Ollama not found. Please install Ollama and run "
                f"'ollama pull {self._model}' first.]"
            )
        except subprocess.TimeoutExpired:
            return "[LLM timed out — try a shorter paragraph or a faster model.]"
        except Exception as exc:
            return f"[Unexpected error: {exc}]"
