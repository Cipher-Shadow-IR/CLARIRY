class ExplanationSession:
    def __init__(self, paragraph, explainer, speaker):
        # Core inputs
        self.paragraph = paragraph
        self.explainer = explainer
        self.speaker = speaker

        # Explanation content (generated later)
        self._explanation_text = None
        self._chunks = []
        self._cursor = 0

        # Session state
        self._active = False
        self._interrupted = False

        # Doubt handling
        self._doubt_context = None


    def start(self):
        if self._active:
            return

        # Generate explanation once
        raw_explanation = self.explainer.explain(self.paragraph)

        # Normalize explainer output to a single spoken string
        if isinstance(raw_explanation, list):
            self._explanation_text = " ".join(raw_explanation)
        else:
            self._explanation_text = raw_explanation

        # Convert explanation into spoken chunks
        self._chunks = self._chunk_explanation(self._explanation_text)

        self._cursor = 0
        self._active = True
        self._interrupted = False

        # Start speaking continuously
        # self._speak_from_cursor()

        self._speak_next_chunk()

    def _speak_next_chunk(self):
        if not self._active or self._cursor >= len(self._chunks):
            self._active = False
            return

        chunk = self._chunks[self._cursor]
        self.speaker.speak(chunk)
        self._cursor += 1
    
    def _chunk_explanation(self, text, sentences_per_chunk=3):
        # Basic sentence split
        sentences = [
            s.strip()
            for s in text.split(".")
            if s.strip()
        ]

        chunks = []
        current_chunk = []

        for sentence in sentences:
            current_chunk.append(sentence)

            if len(current_chunk) >= sentences_per_chunk:
                chunk_text = ". ".join(current_chunk) + "."
                chunks.append(chunk_text)
                current_chunk = []

        # Add any remaining sentences
        if current_chunk:
            chunk_text = ". ".join(current_chunk) + "."
            chunks.append(chunk_text)

        return chunks

    def _speak_from_cursor(self):
        while self._active and not self._interrupted:
            if self._cursor >= len(self._chunks):
                # Explanation finished
                self._active = False
                return

            current_chunk = self._chunks[self._cursor]

            # Speak the chunk (blocking)
            self.speaker.speak(current_chunk)

            # Move forward only AFTER speaking
            self._cursor += 1

    def interrupt(self):
        if not self._active:
            return

        self._interrupted = True
        self._active = False


    def explain_doubt(self, selected_text):
        if not self._interrupted:
            return

        self._doubt_context = selected_text

        # Ask explainer for a deeper, focused explanation
        doubt_explanation = self.explainer.explain_doubt(selected_text)

        # Speak the doubt explanation fully (no chunking needed here)
        self.speaker.speak(doubt_explanation)


    def resume(self):
        if not self._interrupted:
            return

        # Clear interruption state
        self._interrupted = False
        self._doubt_context = None

        # Mark session active again
        self._active = True

        # Continue speaking from where we left off
        self._speak_from_cursor()


    def stop(self):
        # Stop any ongoing explanation
        self._active = False
        self._interrupted = False

        # Reset progression
        self._cursor = 0
        self._chunks = []

        # Clear explanation content
        self._explanation_text = None
        self._doubt_context = None

