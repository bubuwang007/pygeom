import numpy as np


class MathMatrix:
    _data: np.ndarray

    def __init__(self, data, dtype=np.float64):
        self._data = np.array(data, dtype=dtype)

    @staticmethod
    def zeros(rows, cols, dtype=np.float64):
        return MathMatrix(np.zeros((rows, cols), dtype=dtype))

    @staticmethod
    def ones(rows, cols, dtype=np.float64):
        return MathMatrix(np.ones((rows, cols), dtype=dtype))

    @staticmethod
    def identity(size, dtype=np.float64):
        return MathMatrix(np.eye(size, dtype=dtype))

    def copy(self):
        return MathMatrix(self._data.copy())

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return f"MathMatrix({self._data})"

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    @property
    def shape(self):
        return self._data.shape

    def transpose(self):
        self._data = self._data.T

    def invert(self):
        self._data = np.linalg.inv(self._data)

    def __matmul__(self, other):
        if not isinstance(other, MathMatrix):
            raise TypeError("Operand must be a MathMatrix")
        return MathMatrix(self._data @ other._data)
