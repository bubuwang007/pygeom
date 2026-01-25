from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Trsf2D import Trsf2D

from ..config import FLOAT_PRINT_PRECISION
from ._Xy import Xy
from ._Point2D import Point2D
from ._Ax2D import Ax2D
from ..config import TOLERANCE


class Vec2D:
    _coord: Xy

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._coord = Xy(x, y)

    def __str__(self) -> str:
        return f"Vec2D(x={self._coord.x:.{FLOAT_PRINT_PRECISION}f}, y={self._coord.y:.{FLOAT_PRINT_PRECISION}f})"

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

    def copy(self) -> Vec2D:
        return Vec2D(self._coord.x, self._coord.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2D):
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

    def is_normal_to(self, other: Vec2D) -> bool:
        dot_product = self._coord @ other._coord
        return abs(dot_product) < 1e-9

    def get_normal(self) -> Vec2D:
        return Vec2D(-self._coord.y, self._coord.x)

    def reverse(self) -> Vec2D:
        self._coord.x = -self._coord.x
        self._coord.y = -self._coord.y
        return self

    def is_opposite_to(self, other: Vec2D) -> bool:
        return (self._coord.x == -other._coord.x) and (self._coord.y == -other._coord.y)

    def is_parallel_to(self, other: Vec2D) -> bool:
        cross_product = self._coord.cross(other._coord)
        return abs(cross_product) < TOLERANCE

    def normalize(self) -> Vec2D:
        mod = self.modulus()
        if mod < sys.float_info.epsilon:
            raise ValueError("Cannot normalize a zero-length vector")
        self._coord /= mod
        return self

    def cross(self, other: Vec2D) -> float:
        return self._coord.cross(other._coord)

    def __mul__(self, other: Vec2D | int | float) -> Vec2D:
        coord = self._coord * other
        return Vec2D(coord.x, coord.y)

    def __rmul__(self, other: int | float) -> Vec2D:
        return Vec2D(self._coord.x * other, self._coord.y * other)

    def __imul__(self, other: Vec2D | int | float) -> Vec2D:
        self._coord *= other
        return self

    def __truediv__(self, other: Vec2D | int | float) -> Vec2D:
        coord = self._coord / other
        return Vec2D(coord.x, coord.y)

    def __rtruediv__(self, other: int | float) -> Vec2D:
        return Vec2D(other / self._coord.x, other / self._coord.y)

    def __itruediv__(self, other: Vec2D | int | float) -> Vec2D:
        self._coord /= other
        return self

    def __add__(self, other: Vec2D | int | float) -> Vec2D:
        coord = self._coord + other
        return Vec2D(coord.x, coord.y)

    def __radd__(self, other: int | float) -> Vec2D:
        return self.__add__(other)

    def __iadd__(self, other: Vec2D | int | float) -> Vec2D:
        self._coord += other
        return self

    def __sub__(self, other: Vec2D | int | float) -> Vec2D:
        coord = self._coord - other
        return Vec2D(coord.x, coord.y)

    def __rsub__(self, other: int | float) -> Vec2D:
        return Vec2D(other - self._coord.x, other - self._coord.y)

    def __isub__(self, other: Vec2D | int | float) -> Vec2D:
        self._coord -= other
        return self

    def __matmul__(self, other: Vec2D) -> float:
        return self._coord @ other._coord

    def a1_v1_a2_v2_v3(
        self, a1: float, v1: Vec2D, a2: float, v2: Vec2D, v3: Vec2D
    ) -> Vec2D:
        self._coord.a1_xy1_a2_xy2_xy3(a1, v1._coord, a2, v2._coord, v3._coord)
        return self

    def a1_v1_a2_v2(self, a1: float, v1: Vec2D, a2: float, v2: Vec2D) -> Vec2D:
        self._coord.a1_xy1_a2_xy2(a1, v1._coord, a2, v2._coord)
        return self

    def a1_v1_v2(self, a1: float, v1: Vec2D, v2: Vec2D) -> Vec2D:
        self._coord.a1_xy1_xy2(a1, v1._coord, v2._coord)
        return self

    def v1_v2(self, v1: Vec2D, v2: Vec2D) -> Vec2D:
        self._coord.xy1_xy2(v1._coord, v2._coord)
        return self

    def mirror_by_vec2d(self, vec: Vec2D) -> Vec2D:
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

    def mirror_by_ax2d(self, ax2d: Ax2D):
        xy = ax2d.dir.coord
        ox, oy = self._coord.x, self._coord.y
        dx, dy = xy.x, xy.y

        crosss_term = 2 * dx * dy
        xx = 2 * dx * dx - 1
        yy = 2 * dy * dy - 1

        self.x = ox * xx + oy * crosss_term
        self.y = ox * crosss_term + oy * yy
        return self

    def rotate(self, angle: float) -> Vec2D:
        from ._Trsf2D import Trsf2D

        trsf = Trsf2D()
        trsf.set_rotation(Point2D(0.0, 0.0), angle)
        self._coord = trsf.matrix @ self._coord
        return self

    def transform(self, trsf2d: Trsf2D):
        from ._TrsfForm import TrsfForm

        if trsf2d.trsf_form == TrsfForm.IDENTITY:
            return
        elif trsf2d.trsf_form == TrsfForm.TRANSLATION:
            return
        elif trsf2d.trsf_form == TrsfForm.SCALE:
            self._coord *= trsf2d.scale
        elif trsf2d.trsf_form == TrsfForm.PNTMIRROR:
            self.reverse()
        else:
            self._coord = trsf2d.matrix @ self._coord
        return self
