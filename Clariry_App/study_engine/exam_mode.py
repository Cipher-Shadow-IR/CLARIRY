import subprocess


class ExamFormatter:
    def __init__(self, model_name="llama3:latest"):
        self._model = model_name

    def format(self, paragraph_text):
        prompt = (
            "Convert the following paragraph into exam-ready points.\n"
            "Rules:\n"
            "- Use short bullet points.\n"
            "- Focus on definitions, facts, and keywords.\n"
            "- No explanations or examples.\n"
            "- No extra text.\n\n"
            f"Paragraph:\n{paragraph_text}"
        )

        result = subprocess.run(
            ["ollama", "run", self._model],
            input=prompt,
            text=True,
            capture_output=True
        )

        return result.stdout.strip()
