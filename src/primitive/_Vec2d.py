from __future__ import annotations

import sys

from ._Xy import Xy
from ..config import TOLERANCE


class Vec2d:
    _coord: Xy

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._coord = Xy(x, y)

    def __str__(self) -> str:
        return f"Vec2d(x={self._coord.x}, y={self._coord.y})"

    @property
    def coord(self) -> Xy:
        return self._coord

    @coord.setter
    def coord(self, value: Xy) -> None:
        self._coord = value

    @property
    def x(self) -> float:
        return self._coord.x

    @x.setter
    def x(self, value: float) -> None:
        self._coord.x = value

    @property
    def y(self) -> float:
        return self._coord.y

    @y.setter
    def y(self, value: float) -> None:
        self._coord.y = value

    def copy(self) -> Vec2d:
        return Vec2d(self._coord.x, self._coord.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2d):
            return NotImplemented
        return self._coord == other._coord

    def __getitem__(self, index: int) -> float:
        return self._coord[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._coord[index] = value

    def to_tuple(self) -> tuple[float, float]:
        return (self._coord.x, self._coord.y)

    @property
    def modulus(self) -> float:
        return self._coord.modulus

    def is_normal_to(self, other: Vec2d) -> bool:
        dot_product = self._coord @ other._coord
        return abs(dot_product) < 1e-9

    def get_normal(self) -> Vec2d:
        return Vec2d(-self._coord.y, self._coord.x)

    def reverse(self) -> None:
        self._coord.x = -self._coord.x
        self._coord.y = -self._coord.y

    def is_opposite_to(self, other: Vec2d) -> bool:
        return (self._coord.x == -other._coord.x) and (self._coord.y == -other._coord.y)

    def is_parallel_to(self, other: Vec2d) -> bool:
        cross_product = self._coord.cross(other._coord)
        return abs(cross_product) < TOLERANCE

    def normalize(self) -> None:
        mod = self.modulus()
        if mod < sys.float_info.epsilon:
            raise ValueError("Cannot normalize a zero-length vector")
        self._coord /= mod

    def rotate(self, angle: float):
        raise NotImplementedError("Rotation method not implemented yet.")

    def cross(self, other: Vec2d) -> float:
        return self._coord.cross(other._coord)

    def __mul__(self, other: Vec2d | int | float) -> Vec2d:
        coord = self._coord * other
        return Vec2d(coord.x, coord.y)

    def __rmul__(self, other: int | float) -> Vec2d:
        return Vec2d(self._coord.x * other, self._coord.y * other)

    def __imul__(self, other: Vec2d | int | float) -> Vec2d:
        self._coord *= other
        return self

    def __truediv__(self, other: Vec2d | int | float) -> Vec2d:
        coord = self._coord / other
        return Vec2d(coord.x, coord.y)

    def __rtruediv__(self, other: int | float) -> Vec2d:
        return Vec2d(other / self._coord.x, other / self._coord.y)

    def __itruediv__(self, other: Vec2d | int | float) -> Vec2d:
        self._coord /= other
        return self

    def __add__(self, other: Vec2d | int | float) -> Vec2d:
        coord = self._coord + other
        return Vec2d(coord.x, coord.y)

    def __radd__(self, other: int | float) -> Vec2d:
        return self.__add__(other)

    def __iadd__(self, other: Vec2d | int | float) -> Vec2d:
        self._coord += other
        return self

    def __sub__(self, other: Vec2d | int | float) -> Vec2d:
        coord = self._coord - other
        return Vec2d(coord.x, coord.y)

    def __rsub__(self, other: int | float) -> Vec2d:
        return Vec2d(other - self._coord.x, other - self._coord.y)

    def __isub__(self, other: Vec2d | int | float) -> Vec2d:
        self._coord -= other
        return self

    def __matmul__(self, other: Vec2d) -> float:
        return self._coord @ other._coord

    def a1_v1_a2_v2_v3(
        self, a1: float, v1: Vec2d, a2: float, v2: Vec2d, v3: Vec2d
    ) -> None:
        self._coord.a1_xy1_a2_xy2_xy3(a1, v1._coord, a2, v2._coord, v3._coord)

    def a1_v1_a2_v2(self, a1: float, v1: Vec2d, a2: float, v2: Vec2d) -> None:
        self._coord.a1_xy1_a2_xy2(a1, v1._coord, a2, v2._coord)

    def a1_v1_v2(self, a1: float, v1: Vec2d, v2: Vec2d) -> None:
        self._coord.a1_xy1_xy2(a1, v1._coord, v2._coord)

    def v1_v2(self, v1: Vec2d, v2: Vec2d) -> None:
        self._coord.xy1_xy2(v1._coord, v2._coord)

    def mirror_by_vec2d(self, vec: Vec2d) -> Vec2d:
        m = vec.modulus
        if m < sys.float_info.epsilon:
            raise ValueError("Cannot mirror a zero-length vector")

        coord = vec._coord
        ox = self._coord.x
        oy = self._coord.y

        nx = coord.x / m
        ny = coord.y / m

        m1 = 2 * nx * ny
        xx = 2 * nx * nx - 1
        yy = 2 * ny * ny - 1

        self.x = ox * xx + oy * m1
        self.y = ox * m1 + oy * yy
        return self

    def mirror_by_ax2d(self):
        raise NotImplementedError

    def rotate(self, angle: float) -> Vec2d:
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError
