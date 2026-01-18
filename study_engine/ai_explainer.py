import subprocess
import json


class AIExplainer:
    def __init__(self, model_name="llama3:latest"):
        self._model = model_name

    def explain(self, paragraph_text):
        prompt = (
            "You are a calm tutor.\n"
            "Explain the following paragraph in simple spoken language.\n"
            "Rules:\n"
            "- Use at most 7 short sentences.\n"
            "- No bullet points.\n"
            "- No headings.\n"
            "- No exam tone.\n"
            "- Output ONLY the explanation text.\n\n"
            f"Paragraph:\n{paragraph_text}"
        )

        result = subprocess.run(
            ["ollama", "run", self._model],
            input=prompt,
            text=True,
            capture_output=True
        )

        raw_output = result.stdout.strip()

        sentences = [
            s.strip() + "."
            for s in raw_output.split(".")
            if s.strip()
        ]

        return sentences[:5]
