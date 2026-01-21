from __future__ import annotations


class ValueWeight:
    def __init__(self, value: float, weight: float):
        self.value = value
        self.weight = weight

    def __lt__(self, other: ValueWeight):
        return self.value < other.value
