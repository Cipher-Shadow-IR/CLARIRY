# main.py

from study_engine.paragraph_store import ParaStore
from study_engine.state_manager import StateManager

def main():
    store = ParaStore("data/sample_text.txt")
    state = StateManager(store.total_para())

    while True:
        index = state.current()
        paragraph = store.get_para(index)

        print("\n--------------------")
        print(f"PARAGRAPH {index}")
        print(paragraph)
        print("--------------------")

        command = input("Enter n (next), p (previous), q (quit): ")

        if command == "n":
            state.next()

        elif command == "p":
            state.previous()

        elif command == "q":
            print("Exiting tutor.")
            break

        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()