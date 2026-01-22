from __future__ import annotations
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

    @property
    def is_square(self):
        return self._data.shape[0] == self._data.shape[1]

    def transpose(self):
        self._data = self._data.T

    def invert(self):
        self._data = np.linalg.inv(self._data)

    def __matmul__(self, other):
        if not isinstance(other, MathMatrix):
            raise TypeError("Operand must be a MathMatrix")
        return MathMatrix(self._data @ other._data)

    def __add__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            return MathMatrix(self._data + other._data)
        else:
            return MathMatrix(self._data + other)

    def __radd__(self, other: int | float):
        return self.__add__(other)

    def __iadd__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            self._data += other._data
        else:
            self._data += other
        return self

    def __sub__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            return MathMatrix(self._data - other._data)
        else:
            return MathMatrix(self._data - other)

    def __rsub__(self, other: int | float):
        if isinstance(other, MathMatrix):
            return MathMatrix(other._data - self._data)
        else:
            return MathMatrix(other - self._data)

    def __isub__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            self._data -= other._data
        else:
            self._data -= other
        return self

    def __mul__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            return MathMatrix(self._data * other._data)
        else:
            return MathMatrix(self._data * other)

    def __rmul__(self, other: int | float):
        return self.__mul__(other)

    def __imul__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            self._data *= other._data
        else:
            self._data *= other
        return self

    def __truediv__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            return MathMatrix(self._data / other._data)
        else:
            return MathMatrix(self._data / other)

    def __rtruediv__(self, other: int | float):
        if isinstance(other, MathMatrix):
            return MathMatrix(other._data / self._data)
        else:
            return MathMatrix(other / self._data)

    def __itruediv__(self, other: MathMatrix | int | float):
        if isinstance(other, MathMatrix):
            self._data /= other._data
        else:
            self._data /= other
        return self

    def to_list(self):
        return self._data.tolist()
