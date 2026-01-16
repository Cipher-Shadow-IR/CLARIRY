# study_engine\state_manager.py

class StateManager:
    def __init__(self, total_items):
        self._cur_index = 0
        self._total_items = total_items

    def current(self):
        return self._cur_index

    def next(self):
        if self._cur_index < self._total_items - 1:
            self._cur_index += 1

        return self._cur_index

    def previous(self):
        if self._cur_index > 0:
            self._cur_index -= 1

        return self._cur_index
