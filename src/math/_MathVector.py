from __future__ import annotations

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

    def __add__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            return MathVector(self._data + other._data)
        else:
            return MathVector(self._data + other)

    def __radd__(self, other: int | float):
        return self.__add__(other)

    def __iadd__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            self._data += other._data
        else:
            self._data += other
        return self

    def __sub__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            return MathVector(self._data - other._data)
        else:
            return MathVector(self._data - other)

    def __rsub__(self, other: int | float):
        if isinstance(other, MathVector):
            return MathVector(other._data - self._data)
        else:
            return MathVector(other - self._data)

    def __isub__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            self._data -= other._data
        else:
            self._data -= other
        return self

    def __mul__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            return MathVector(self._data * other._data)
        else:
            return MathVector(self._data * other)

    def __rmul__(self, other: int | float):
        return self.__mul__(other)

    def __imul__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            self._data *= other._data
        else:
            self._data *= other
        return self

    def __truediv__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            return MathVector(self._data / other._data)
        else:
            return MathVector(self._data / other)

    def __rtruediv__(self, other: int | float):
        if isinstance(other, MathVector):
            return MathVector(other._data / self._data)
        else:
            return MathVector(other / self._data)

    def __itruediv__(self, other: MathVector | int | float):
        if isinstance(other, MathVector):
            self._data /= other._data
        else:
            self._data /= other
        return self

    def __neg__(self):
        return MathVector(-self._data)

    def __matmul__(self, other: MathVector):
        if not isinstance(other, MathVector):
            raise TypeError("Operand must be a MathVector")
        return self._data.dot(other._data)

    def to_matrix(self, row=None, col=1):
        from ._MathMatrix import MathMatrix
        if row is None:
            row = len(self._data)
        mat = np.array(self._data).reshape((row, col))
        
        return MathMatrix(mat)