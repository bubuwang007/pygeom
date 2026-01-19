import numpy as np


class MathVector:
    _data: np.ndarray

    def __init__(self, data, dtype=np.float64):
        self._data = np.array(data, dtype=dtype)

    @staticmethod
    def range(start, end, dtype=np.float64):
        return MathVector(np.arange(start, end, dtype=dtype))

    @staticmethod
    def zeros(length, dtype=np.float64):
        return MathVector(np.zeros(length, dtype=dtype))

    @staticmethod
    def ones(length, dtype=np.float64):
        return MathVector(np.ones(length, dtype=dtype))
