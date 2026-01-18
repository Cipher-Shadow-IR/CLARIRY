# study_engine\explainer.py

class Explainer:
    def explain(self, paragraph_text):
        sentences = paragraph_text.split(".")
        core = sentences[0].strip().lower()

        explanation_units = [
            f"This paragraph is mainly about {core}.",
            f"In simple words, it explains that {core}.",
            "This helps you understand the topic more clearly.",
            "You should focus on the idea rather than memorizing the text.",
            "Once this idea is clear, related details become easier."
        ]

        return explanation_units

