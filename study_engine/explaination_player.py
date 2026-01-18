import time

class ExplainationPlayer:
    def __init__(self, speaker):
        self._speaker = speaker

    def play(self, explanation_units, state, paragraph_index):
        sentence_index = state.get_resume_sentence(paragraph_index)

        while sentence_index < len(explanation_units):
            self._speaker.speak(explanation_units[sentence_index])
            time.sleep(0.4)

            command = input(
                "Enter = continue | d = doubt | s = stop explanation: "
            ).strip().lower()

            if command == "":
                sentence_index += 1
            elif command == "d":
                print("Doubt noted. (stub)")
                sentence_index += 1
            elif command == "s":
                print("Explanation paused.")
                break
            else:
                print("Invalid input.")

        state.set_resume_sentence(paragraph_index, sentence_index)
