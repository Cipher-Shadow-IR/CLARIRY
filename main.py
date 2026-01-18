# main.py

from study_engine.paragraph_store import ParaStore
from study_engine.state_manager import StateManager
# from study_engine.explainer import Explainer
from study_engine.ai_explainer import AIExplainer
from study_engine.explaination_player import ExplainationPlayer
# from study_engine.speaker import Speaker
# from study_engine.fake_audio_speaker import FakeAudioSpeaker
from study_engine.tts_speaker import TTSSpeaker
from study_engine.exam_mode import ExamFormatter

def display(store, explainer, player, state, index):
    paragraph = store.get_para(index)

    print("\n" + "-" * 20)
    print(f"PARAGRAPH {index}")
    print(paragraph)

    explanation_units = explainer.explain(paragraph)

    print("\nEXPLANATION:")
    player.play(explanation_units, state, index)



def main():
    store = ParaStore("data/sample_text.txt")
    state = StateManager(store.total_para())
    explainer = AIExplainer()
    speaker = TTSSpeaker()
    player = ExplainationPlayer(speaker)
    exam_formatter = ExamFormatter()

    while True:
        index = state.current()
        display(store, explainer, player, state, index)

        command = input("Enter n (next), p (previous), e (exam-mode), q (quit): ").strip().lower()

        if command == "n":
            state.next()
        elif command == "p":
            state.previous()
        elif command == "q":
            print("Exiting tutor.")
            break
        elif command == "e":
            paragraph = store.get_para(index)
            exam_notes = exam_formatter.format(paragraph)

            print("\n--- EXAM MODE ---")
            print(exam_notes)
            input("\nPress Enter to return to understanding mode.")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
