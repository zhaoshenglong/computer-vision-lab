from typing import List
import numpy as np


class HistoryCtrl:
    position = 0
    history_src: List[np.ndarray]
    history_des: List[str]

    def __init__(self):
        self.history_src = []
        self.history_des = []

    def push(self, src: np.ndarray, desc: str):
        if self.position >= self.history_src.__len__():
            self.history_src.append(src)
            self.history_des.append(desc)
        else:
            self.history_src[self.position] = src
            self.history_des[self.position] = desc
        self.position += 1

    def clear(self):
        self.history_src = []
        self.history_des = []

    def get(self, pos: int):
        assert (0 <= pos < self.position)
        return self.history_des[pos], self.history_src[pos]

    def current(self) -> np.ndarray:
        return self.history_src[self.position - 1]

    def undo(self):
        self.position -= 1

    def redo(self):
        self.position += 1
