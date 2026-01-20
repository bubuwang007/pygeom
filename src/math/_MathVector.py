import numpy as np
from ..primitive import Xy, Xyz


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

    @staticmethod
    def from_xy(xy: Xy, dtype=np.float64):
        return MathVector([xy.x, xy.y], dtype=dtype)

    @staticmethod
    def from_xyz(xyz: Xyz, dtype=np.float64):
        return MathVector([xyz.x, xyz.y, xyz.z], dtype=dtype)

    def copy(self):
        return MathVector(self._data.copy())

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return f"MathVector({self._data})"

    @property
    def norm(self):
        return np.linalg.norm(self._data)

    @property
    def norm2(self):
        return self._data.dot(self._data)

    @property
    def max(self):
        return np.max(self._data)

    @property
    def min(self):
        return np.min(self._data)

    def normalize(self):
        self._data = self._data / self.norm

    def reverse(self):
        self._data = self._data[::-1]

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
