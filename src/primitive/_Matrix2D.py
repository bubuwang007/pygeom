from __future__ import annotations

import sys
import numpy as np


class Matrix2D:
    _data: np.ndarray

    def __init__(self, data=[[1.0, 0.0], [0.0, 1.0]]):
        self._data = np.array(data, dtype=float)

    def __str__(self) -> str:
        return f"Matrix2D(data={self._data.tolist()})"

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, value: np.ndarray) -> None:
        self._data = value

    @property
    def determinant(self) -> float:
        return np.linalg.det(self._data)

    def is_singular(self) -> bool:
        if abs(self.determinant) < sys.float_info.epsilon:
            return True
        return False

    def copy(self) -> Matrix2D:
        return Matrix2D(self._data.copy())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix2D):
            return NotImplemented
        return np.array_equal(self._data, other._data)

    def get_col(self, index: int) -> np.ndarray:
        return self._data[:, index]

    def get_row(self, index: int) -> np.ndarray:
        return self._data[index, :]

    def set_col(self, index: int, value: np.ndarray) -> None:
        self._data[:, index] = value

    def set_row(self, index: int, value: np.ndarray) -> None:
        self._data[index, :] = value

    def get_diagonal(self) -> np.ndarray:
        return np.diagonal(self._data)

    def set_diagonal(self, value: np.ndarray) -> None:
        np.fill_diagonal(self._data, value)

    def set_identity(self) -> None:
        self._data = np.identity(2)

    def set_rotation(self, angle):
        c = np.cos(angle)
        s = np.sin(angle)
        self._data = np.array([[c, -s], [s, c]])

    def set_scale(self, sx: float, sy: float = None) -> None:
        if sy is None:
            sy = sx
        self._data = np.array([[sx, 0.0], [0.0, sy]])

    def __getitem__(self, index: tuple[int, int]) -> float:
        return self._data[index]

    def __setitem__(self, index: tuple[int, int], value: float) -> None:
        self._data[index] = value

    def to_list(self) -> list[list[float]]:
        return self._data.tolist()

    def __add__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            return Matrix2D(self._data + other._data)
        elif isinstance(other, (int, float)):
            return Matrix2D(self._data + other)
        else:
            return NotImplemented

    def __radd__(self, other: int | float) -> Matrix2D:
        return self.__add__(other)

    def __iadd__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            self._data += other._data
        elif isinstance(other, (int, float)):
            self._data += other
        else:
            return NotImplemented
        return self

    def __sub__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            return Matrix2D(self._data - other._data)
        elif isinstance(other, (int, float)):
            return Matrix2D(self._data - other)
        else:
            return NotImplemented

    def __rsub__(self, other: int | float) -> Matrix2D:
        if isinstance(other, (int, float)):
            return Matrix2D(other - self._data)
        else:
            return NotImplemented

    def __isub__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            self._data -= other._data
        elif isinstance(other, (int, float)):
            self._data -= other
        else:
            return NotImplemented
        return self

    def __mul__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            return Matrix2D(self._data * other._data)
        elif isinstance(other, (int, float)):
            return Matrix2D(self._data * other)
        else:
            return NotImplemented

    def __rmul__(self, other: int | float) -> Matrix2D:
        if isinstance(other, (int, float)):
            return Matrix2D(self._data * other)
        else:
            return NotImplemented

    def __imul__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            self._data *= other._data
        elif isinstance(other, (int, float)):
            self._data *= other
        else:
            return NotImplemented
        return self

    def __matmul__(self, other: Matrix2D) -> Matrix2D:
        if isinstance(other, Matrix2D):
            return Matrix2D(self._data @ other._data)
        else:
            return NotImplemented

    def __imatmul__(self, other: Matrix2D) -> Matrix2D:
        if isinstance(other, Matrix2D):
            self._data @= other._data
            return self
        else:
            return NotImplemented

    def __truediv__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            return Matrix2D(self._data / other._data)
        elif isinstance(other, (int, float)):
            return Matrix2D(self._data / other)
        else:
            return NotImplemented

    def __rtruediv__(self, other: int | float) -> Matrix2D:
        if isinstance(other, (int, float)):
            return Matrix2D(other / self._data)
        else:
            return NotImplemented

    def __itruediv__(self, other: Matrix2D | int | float) -> Matrix2D:
        if isinstance(other, Matrix2D):
            self._data /= other._data
        elif isinstance(other, (int, float)):
            self._data /= other
        else:
            return NotImplemented
        return self

    def __pow__(self, power: int) -> Matrix2D:
        return Matrix2D(np.linalg.matrix_power(self._data, power))

    def __ipow__(self, power: int) -> Matrix2D:
        self._data = np.linalg.matrix_power(self._data, power)
        return self

    def transpose(self) -> Matrix2D:
        self._data = self._data.T
        return self

    def invert(self) -> Matrix2D:
        if self.is_singular():
            raise ValueError("Matrix is singular and cannot be inverted.")
        self._data = np.linalg.inv(self._data)
        return self
