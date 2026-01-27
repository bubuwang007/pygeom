from __future__ import annotations

import sys
import math
from typing import TYPE_CHECKING

from ..config import FLOAT_PRINT_PRECISION, TOLERANCE
from ._Xy import Xy

if TYPE_CHECKING:
    from ._Ax2D import Ax2D
    from ._Trsf2D import Trsf2D


class Dir2D:
    _coord: Xy

    def __init__(self, x: float = 1.0, y: float = 0.0) -> None:
        self._coord = Xy(x, y)
        self.normalize()

    def normalize(self) -> None:
        mod = self._coord.modulus
        if mod < sys.float_info.epsilon:
            raise ValueError("Cannot normalize a zero-length direction vector.")
        self._coord /= mod

    def __str__(self) -> str:
        return f"Dir2D(x={self._coord.x:.{FLOAT_PRINT_PRECISION}f}, y={self._coord.y:.{FLOAT_PRINT_PRECISION}f})"

    @property
    def coord(self) -> Xy:
        return self._coord

    @coord.setter
    def coord(self, value: Xy) -> None:
        self._coord = value
        self.normalize()

    @property
    def x(self) -> float:
        return self._coord.x

    @x.setter
    def x(self, value: float) -> None:
        self._coord.x = value
        self.normalize()

    @property
    def y(self) -> float:
        return self._coord.y

    @y.setter
    def y(self, value: float) -> None:
        self._coord.y = value
        self.normalize()

    def copy(self) -> Dir2D:
        return Dir2D(self._coord.x, self._coord.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dir2D):
            return NotImplemented
        return self._coord == other._coord

    def __getitem__(self, index: int) -> float:
        return self._coord[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._coord[index] = value
        self.normalize()

    def to_tuple(self) -> tuple[float, float]:
        return (self._coord.x, self._coord.y)

    def is_normal_to(self, other: Dir2D) -> bool:
        dot_product = self._coord.x * other._coord.x + self._coord.y * other._coord.y
        return abs(dot_product) < sys.float_info.epsilon

    def is_opposite_to(self, other: Dir2D) -> bool:
        angle = abs(self.angle(other))
        return math.pi - angle < TOLERANCE

    def is_parallel_to(self, other: Dir2D) -> bool:
        cross_product = self._coord.x * other._coord.y - self._coord.y * other._coord.x
        return abs(cross_product) < TOLERANCE

    def angle(self, other: Dir2D) -> float:
        """
        当角度大于 45° 时，使用 acos 计算角度能获得更好的精度；
        否则，最好使用 asin。
        当角度接近 0° 或 90° 时，所产生的误差是远非可以忽略的。
        在二维情况下，角度取值范围在 -π 到 π 之间。
        """
        cos = self._coord @ other._coord
        sin = self._coord.cross(other._coord)
        if cos > -0.70710678118655 and cos < 0.70710678118655:
            if sin > 0:
                return math.acos(cos)
            else:
                return -math.acos(cos)
        else:
            if cos > 0:
                return math.asin(sin)
            else:
                if sin > 0:
                    return math.pi - math.asin(sin)
                else:
                    return -math.pi - math.asin(sin)

    def cross(self, other: Dir2D) -> float:
        return self._coord.cross(other._coord)

    def __matmul__(self, other: Dir2D) -> float:
        return self._coord @ other._coord

    def reverse(self) -> Dir2D:
        self._coord.x = -self._coord.x
        self._coord.y = -self._coord.y
        return self

    def mirror_by_dir2d(self, dir: Dir2D) -> Dir2D:
        coord = dir.coord
        a = coord.x
        b = coord.y
        x = self._coord.x
        y = self._coord.y

        m1 = 2 * a * b
        xx = (2 * a * a - 1) * x + m1 * y
        yy = m1 * x + (2 * b * b - 1) * y
        self._coord = Xy(xx, yy)
        self.normalize()
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D):
        xy = ax2d.dir.coord
        a, b = xy.x, xy.y
        x, y = self._coord.x, self._coord.y
        m1 = 2 * a * b
        xx = (2 * a * a - 1) * x + m1 * y
        yy = m1 * x + (2 * b * b - 1) * y
        self._coord = Xy(xx, yy)
        return self

    def rotate(self, angle: float) -> Dir2D:
        from ._Trsf2D import Trsf2D
        from ._Point2D import Point2D

        trsf = Trsf2D()
        trsf.set_rotation(Point2D(0, 0), angle)
        self._coord = trsf.matrix @ self._coord

        return self

    def transform(self, trsf2d: Trsf2D):
        from ._TrsfForm import TrsfForm

        if trsf2d.trsf_form == TrsfForm.IDENTITY:
            return
        elif trsf2d.trsf_form == TrsfForm.PNTMIRROR:
            self.reverse()
        elif trsf2d.trsf_form == TrsfForm.SCALE:
            if trsf2d.scale < 0:
                self.reverse()
        else:
            self._coord = trsf2d.matrix @ self._coord
            self.normalize()
            if trsf2d.scale < 0:
                self.reverse()
        return self
