from __future__ import annotations
import math
from ..config import TOLERANCE, FLOAT_PRINT_PRECISION


class Xyz:
    _x: float
    _y: float
    _z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self._x = x
        self._y = y
        self._z = z

    def __str__(self) -> str:
        return f"Xyz(x={self._x:.{FLOAT_PRINT_PRECISION}f}, y={self._y:.{FLOAT_PRINT_PRECISION}f}, z={self._z:.{FLOAT_PRINT_PRECISION}f})"

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        elif index == 2:
            return self._z
        else:
            raise IndexError("Index out of range for Xyz object")

    def __setitem__(self, index: int, value: float) -> None:
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        elif index == 2:
            self._z = value
        else:
            raise IndexError("Index out of range for Xyz object")

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
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        self._z = value

    @property
    def modulus(self) -> float:
        return math.sqrt(self._x**2 + self._y**2 + self._z**2)

    @property
    def square_modulus(self) -> float:
        return self._x**2 + self._y**2 + self._z**2

    def normalize(self) -> Xyz:
        mod = self.modulus
        if mod > TOLERANCE:
            self._x /= mod
            self._y /= mod
            self._z /= mod
        else:
            raise ValueError("Cannot normalize a zero vector")
        return self

    def cross_magnitude(self, other: Xyz) -> float:
        return math.sqrt(self.square_cross_magnitude(other))

    def square_cross_magnitude(self, other: Xyz) -> float:
        cross_x = self._y * other._z - self._z * other._y
        cross_y = self._z * other._x - self._x * other._z
        cross_z = self._x * other._y - self._y * other._x
        return cross_x**2 + cross_y**2 + cross_z**2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Xyz):
            return NotImplemented
        return (
            abs(self._x - other._x) < TOLERANCE
            and abs(self._y - other._y) < TOLERANCE
            and abs(self._z - other._z) < TOLERANCE
        )

    def __add__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            return Xyz(self._x + other, self._y + other, self._z + other)
        return Xyz(self._x + other._x, self._y + other._y, self._z + other._z)

    def __iadd__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            self._x += other
            self._y += other
            self._z += other
            return self
        self._x += other._x
        self._y += other._y
        self._z += other._z
        return self

    def __radd__(self, other: int | float) -> Xyz:
        return self.__add__(other)

    def __sub__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            return Xyz(self._x - other, self._y - other, self._z - other)
        return Xyz(self._x - other._x, self._y - other._y, self._z - other._z)

    def __isub__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            self._x -= other
            self._y -= other
            self._z -= other
            return self
        self._x -= other._x
        self._y -= other._y
        self._z -= other._z
        return self

    def __rsub__(self, other: int | float) -> Xyz:
        if isinstance(other, (int, float)):
            return Xyz(other - self._x, other - self._y, other - self._z)
        return NotImplemented

    def __mul__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            return Xyz(self._x * other, self._y * other, self._z * other)
        return Xyz(self._x * other._x, self._y * other._y, self._z * other._z)

    def __imul__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            self._x *= other
            self._y *= other
            self._z *= other
            return self
        self._x *= other._x
        self._y *= other._y
        self._z *= other._z
        return self

    def __rmul__(self, other: int | float) -> Xyz:
        return self.__mul__(other)

    def __truediv__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            return Xyz(self._x / other, self._y / other, self._z / other)
        return Xyz(self._x / other._x, self._y / other._y, self._z / other._z)

    def __itruediv__(self, other: Xyz | int | float) -> Xyz:
        if isinstance(other, (int, float)):
            self._x /= other
            self._y /= other
            self._z /= other
            return self
        self._x /= other._x
        self._y /= other._y
        self._z /= other._z
        return self

    def __rtruediv__(self, other: int | float) -> Xyz:
        if isinstance(other, (int, float)):
            return Xyz(other / self._x, other / self._y, other / self._z)
        return NotImplemented

    def __neg__(self) -> Xyz:
        return Xyz(-self._x, -self._y, -self._z)

    def reverse(self) -> None:
        self._x = -self._x
        self._y = -self._y
        self._z = -self._z

    def __matmul__(self, other: Xyz) -> float:
        return self._x * other._x + self._y * other._y + self._z * other._z

    def __imatmul__(self, other: Xyz) -> float:
        return self.__matmul__(other)

    def __rmatmul__(self, other) -> float:
        from ._Matrix3D import Matrix3D

        if isinstance(other, Matrix3D):
            return Xyz(*(other.data @ self.to_tuple()))

    def cross(self, other: Xyz) -> Xyz:
        return Xyz(
            self._y * other._z - self._z * other._y,
            self._z * other._x - self._x * other._z,
            self._x * other._y - self._y * other._x,
        )

    def cross_cross(self, o1: Xyz, o2: Xyz) -> Xyz:
        return self.cross(o1.cross(o2))

    def dot_cross(self, o1: Xyz, o2: Xyz) -> float:
        return self @ (o1.cross(o2))

    def copy(self) -> Xyz:
        return Xyz(self._x, self._y, self._z)

    def to_tuple(self) -> tuple[float, float, float]:
        return (self._x, self._y, self._z)

    def a1_xyz1_a2_xyz2_a3_xyz3_xyz4(
        self,
        a1: float,
        xyz1: Xyz,
        a2: float,
        xyz2: Xyz,
        a3: float,
        xyz3: Xyz,
        xyz4: Xyz,
    ) -> None:
        self._x = a1 * xyz1._x + a2 * xyz2._x + a3 * xyz3._x + xyz4._x
        self._y = a1 * xyz1._y + a2 * xyz2._y + a3 * xyz3._y + xyz4._y
        self._z = a1 * xyz1._z + a2 * xyz2._z + a3 * xyz3._z + xyz4._z

    def a1_xyz1_a2_xyz2_a3_xyz3(
        self,
        a1: float,
        xyz1: Xyz,
        a2: float,
        xyz2: Xyz,
        a3: float,
        xyz3: Xyz,
    ) -> None:
        self._x = a1 * xyz1._x + a2 * xyz2._x + a3 * xyz3._x
        self._y = a1 * xyz1._y + a2 * xyz2._y + a3 * xyz3._y
        self._z = a1 * xyz1._z + a2 * xyz2._z + a3 * xyz3._z

    def a1_xyz1_a2_xyz2_xyz3(
        self, a1: float, xyz1: Xyz, a2: float, xyz2: Xyz, xyz3: Xyz
    ) -> None:
        self._x = a1 * xyz1._x + a2 * xyz2._x + xyz3._x
        self._y = a1 * xyz1._y + a2 * xyz2._y + xyz3._y
        self._z = a1 * xyz1._z + a2 * xyz2._z + xyz3._z

    def a1_xyz1_a2_xyz2(self, a1: float, xyz1: Xyz, a2: float, xyz2: Xyz) -> None:
        self._x = a1 * xyz1._x + a2 * xyz2._x
        self._y = a1 * xyz1._y + a2 * xyz2._y
        self._z = a1 * xyz1._z + a2 * xyz2._z

    def a1_xyz1_xyz2(self, a1: float, xyz1: Xyz, xyz2: Xyz) -> None:
        self._x = a1 * xyz1._x + xyz2._x
        self._y = a1 * xyz1._y + xyz2._y
        self._z = a1 * xyz1._z + xyz2._z

    def xyz1_xyz2(self, xyz1: Xyz, xyz2: Xyz) -> None:
        self._x = xyz1._x + xyz2._x
        self._y = xyz1._y + xyz2._y
        self._z = xyz1._z + xyz2._z
