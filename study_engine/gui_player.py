class GUIExplanationPlayer:
    def __init__(self, speaker):
        self._speaker = speaker
        self._is_playing = False
        self._current_units = []
        self._sentence_index = 0
        self._state = None
        self._paragraph_index = None

    def start(self, explanation_units, state, paragraph_index):
        self._current_units = explanation_units
        self._state = state
        self._paragraph_index = paragraph_index
        self._sentence_index = state.get_resume_sentence(paragraph_index)
        self._is_playing = True

    def play_next(self):
        if not self._is_playing:
            return

        if self._sentence_index >= len(self._current_units):
            self._is_playing = False
            return

        sentence = self._current_units[self._sentence_index]
        self._speaker.speak(sentence)

        self._sentence_index += 1
        self._state.set_resume_sentence(
            self._paragraph_index, self._sentence_index
        )

    def pause(self):
        self._is_playing = False
