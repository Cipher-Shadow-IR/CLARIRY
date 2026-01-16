# main.py

from study_engine.paragraph_store import ParaStore

def main():
    print("PROGRAM STARTED!!!")

    store = ParaStore("data/sample_text.txt")

    count = store.total_para()
    print(f"Total Paragraphs: {count}!!")

    first = store.get_para(0)
    print(f"\nParagraph 0:\n {first}!!")

if __name__ == "__main__":
    main()