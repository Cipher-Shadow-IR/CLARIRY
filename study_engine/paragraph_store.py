# study_engine\paragraph_store.py

class ParaStore:
    def __init__(self, txt_path):
        self._paras = []
        self._load_text(txt_path)
    
    def _load_text(self, txt_path):
        with open(txt_path, "r", encoding="utf-8") as file:
            raw_txt = file.read()
        
        chunks = raw_txt.split("\n\n")

        for item in chunks:
            cleaned = item.strip()
            if cleaned:
                self._paras.append(cleaned)

    def get_para(self, para_id):
        if para_id < 0:
            return None

        if para_id >= len(self._paras):
            return None

        return self._paras[para_id]

    def total_para(self):
        return len(self._paras)
