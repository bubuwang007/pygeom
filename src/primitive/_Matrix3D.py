from __future__ import annotations

import sys
import numpy as np

from ._Xyz import Xyz


class Matrix3D:
    _data: np.ndarray

    def __init__(self, data=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]):
        self._data = np.array(data, dtype=float)

    def __str__(self) -> str:
        return f"Matrix3D(data={self._data.tolist()})"

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

    def copy(self) -> Matrix3D:
        return Matrix3D(self._data.copy())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix3D):
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
        self._data = np.identity(3)

    def set_cross(self, xyz: Xyz):
        x, y, z = xyz.x, xyz.y, xyz.z
        self._data = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float)

    def set_scale(self, factor: float) -> None:
        self._data = np.array(
            [[factor, 0.0, 0.0], [0.0, factor, 0.0], [0.0, 0.0, factor]], dtype=float
        )

    def set_dot(self, xyz: Xyz):
        x, y, z = xyz.x, xyz.y, xyz.z
        self._data = np.array(
            [[x**2, x * y, x * z], [x * y, y**2, y * z], [x * z, y * z, z**2]],
            dtype=float,
        )

    def __getitem__(self, index: tuple[int, int]) -> float:
        return self._data[index]

    def __setitem__(self, index: tuple[int, int], value: float) -> None:
        self._data[index] = value

    def to_list(self) -> list[list[float]]:
        return self._data.tolist()

    def __add__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            return Matrix3D(self._data + other._data)
        elif isinstance(other, (int, float)):
            return Matrix3D(self._data + other)
        else:
            return NotImplemented

    def __radd__(self, other: int | float) -> Matrix3D:
        return self.__add__(other)

    def __iadd__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            self._data += other._data
        elif isinstance(other, (int, float)):
            self._data += other
        else:
            return NotImplemented
        return self

    def __sub__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            return Matrix3D(self._data - other._data)
        elif isinstance(other, (int, float)):
            return Matrix3D(self._data - other)
        else:
            return NotImplemented

    def __rsub__(self, other: int | float) -> Matrix3D:
        if isinstance(other, (int, float)):
            return Matrix3D(other - self._data)
        else:
            return NotImplemented

    def __isub__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            self._data -= other._data
        elif isinstance(other, (int, float)):
            self._data -= other
        else:
            return NotImplemented
        return self

    def __mul__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            return Matrix3D(self._data * other._data)
        elif isinstance(other, (int, float)):
            return Matrix3D(self._data * other)
        else:
            return NotImplemented

    def __rmul__(self, other: int | float) -> Matrix3D:
        if isinstance(other, (int, float)):
            return Matrix3D(self._data * other)
        else:
            return NotImplemented

    def __imul__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            self._data *= other._data
        elif isinstance(other, (int, float)):
            self._data *= other
        else:
            return NotImplemented
        return self

    def __matmul__(self, other: Matrix3D) -> Matrix3D:
        if isinstance(other, Matrix3D):
            return Matrix3D(np.matmul(self._data, other._data))
        else:
            return NotImplemented

    def __imatmul__(self, other: Matrix3D) -> Matrix3D:
        if isinstance(other, Matrix3D):
            self._data = np.matmul(self._data, other._data)
            return self
        else:
            return NotImplemented

    def __truediv__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            return Matrix3D(self._data / other._data)
        elif isinstance(other, (int, float)):
            return Matrix3D(self._data / other)
        else:
            return NotImplemented

    def __itruediv__(self, other: Matrix3D | int | float) -> Matrix3D:
        if isinstance(other, Matrix3D):
            self._data /= other._data
        elif isinstance(other, (int, float)):
            self._data /= other
        else:
            return NotImplemented
        return self

    def __rtruediv__(self, other: int | float) -> Matrix3D:
        if isinstance(other, (int, float)):
            return Matrix3D(other / self._data)
        else:
            return NotImplemented

    def __pow__(self, power: int) -> Matrix3D:
        return Matrix3D(np.linalg.matrix_power(self._data, power))

    def __ipow__(self, power: int) -> Matrix3D:
        self._data = np.linalg.matrix_power(self._data, power)
        return self

    def transpose(self) -> Matrix3D:
        self._data = self._data.T
        return self

    def invert(self) -> Matrix3D:
        if self.is_singular():
            raise ValueError("Cannot invert a singular matrix.")
        self._data = np.linalg.inv(self._data)
        return self

    def set_rotation(self, axis: Xyz, angle: float) -> None:
        av = axis.copy().normalize()
        a, b, c = av.x, av.y, av.z

        acos = np.cos(angle)
        asin = np.sin(angle)
        aomcos = 1.0 - acos

        a2 = a * a
        b2 = b * b
        c2 = c * c
        ab = a * b
        bc = b * c
        ac = c * a

        self._data = np.array(
            [
                [
                    1.0 + aomcos * (-(b2 + c2)),
                    aomcos * ab - c * asin,
                    aomcos * ac + b * asin,
                ],
                [
                    aomcos * ab + c * asin,
                    1.0 + aomcos * (-(a2 + c2)),
                    aomcos * bc - a * asin,
                ],
                [
                    aomcos * ac - b * asin,
                    aomcos * bc + a * asin,
                    1.0 + aomcos * (-(a2 + b2)),
                ],
            ],
            dtype=float,
        )
