from __future__ import annotations
import math

from ..config import TOLERANCE, FLOAT_PRINT_PRECISION


class Xy:
    _x: float
    _y: float

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._x = float(x)
        self._y = float(y)

    def __str__(self) -> str:
        return f"Xy(x={self._x:.{FLOAT_PRINT_PRECISION}f}, y={self._y:.{FLOAT_PRINT_PRECISION}f})"

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise IndexError("Index out of range for Xy object")

    def __setitem__(self, index: int, value: float) -> None:
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise IndexError("Index out of range for Xy object")

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def modulus(self) -> float:
        return math.sqrt(self._x**2 + self._y**2)

    @property
    def square_modulus(self) -> float:
        return self._x**2 + self._y**2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Xy):
            return NotImplemented
        return self._x - other._x < TOLERANCE and self._y - other._y < TOLERANCE

    def __add__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            return Xy(self._x + other, self._y + other)
        return Xy(self._x + other._x, self._y + other._y)

    def __iadd__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            self._x += other
            self._y += other
            return self
        self._x += other._x
        self._y += other._y
        return self

    def __radd__(self, other: int | float) -> Xy:
        return self.__add__(other)

    def __sub__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            return Xy(self._x - other, self._y - other)
        return Xy(self._x - other._x, self._y - other._y)

    def __isub__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            self._x -= other
            self._y -= other
            return self
        self._x -= other._x
        self._y -= other._y
        return self

    def __rsub__(self, other: int | float) -> Xy:
        return self.__sub__(other)

    def __mul__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            return Xy(self._x * other, self._y * other)
        return Xy(self._x * other._x, self._y * other._y)

    def __imul__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            self._x *= other
            self._y *= other
            return self
        self._x *= other._x
        self._y *= other._y
        return self

    def __rmul__(self, other: int | float) -> Xy:
        return self.__mul__(other)

    def __truediv__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            return Xy(self._x / other, self._y / other)
        return Xy(self._x / other._x, self._y / other._y)

    def __itruediv__(self, other: Xy | int | float) -> Xy:
        if isinstance(other, (int, float)):
            self._x /= other
            self._y /= other
            return self
        self._x /= other._x
        self._y /= other._y
        return self

    def __rtruediv__(self, other: int | float) -> Xy:
        return Xy(other / self._x, other / self._y)

    def __neg__(self) -> Xy:
        return Xy(-self._x, -self._y)

    def reverse(self):
        self._x = -self._x
        self._y = -self._y

    def __matmul__(self, other: Xy) -> float:
        return self._x * other._x + self._y * other._y

    def __rmatmul__(self, other) -> float:
        from ._Matrix2D import Matrix2D

        if isinstance(other, Matrix2D):
            return Xy(*(other.data @ self.to_tuple()))

    def cross(self, other: Xy) -> float:
        return self._x * other._y - self._y * other._x

    def normalize(self) -> None:
        modulus = self.modulus
        if modulus > TOLERANCE:
            self._x /= modulus
            self._y /= modulus
        else:
            raise ValueError("Cannot normalize a zero-length vector")

    def __xor__(self, other: Xy) -> float:
        return self.cross(other)

    def cross_magnitude(self, other: Xy) -> float:
        return abs(self.cross(other))

    def square_cross_magnitude(self, other: Xy) -> float:
        return self.cross(other) ** 2

    def copy(self) -> Xy:
        return Xy(self._x, self._y)

    def to_tuple(self) -> tuple[float, float]:
        return (self._x, self._y)

    def a1_xy1_a2_xy2(self, a1: float, xy1: Xy, a2: float, xy2: Xy) -> None:
        self._x = a1 * xy1._x + a2 * xy2._x
        self._y = a1 * xy1._y + a2 * xy2._y

    def a1_xy1_a2_xy2_xy3(
        self, a1: float, xy1: Xy, a2: float, xy2: Xy, xy3: Xy
    ) -> None:
        self._x = a1 * xy1._x + a2 * xy2._x + xy3._x
        self._y = a1 * xy1._y + a2 * xy2._y + xy3._y

    def a1_xy1_xy2(self, a1: float, xy1: Xy, xy2: Xy) -> None:
        self._x = a1 * xy1._x + xy2._x
        self._y = a1 * xy1._y + xy2._y

    def xy1_xy2(self, xy1: Xy, xy2: Xy) -> None:
        self._x = xy1._x + xy2._x
        self._y = xy1._y + xy2._y
