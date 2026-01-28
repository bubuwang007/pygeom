from __future__ import annotations

import sys

from ._Point2D import Point2D
from ._Dir2D import Dir2D
from ._Ax2D import Ax2D
from ._Trsf2D import Trsf2D


class Lin2D:
    _pos: Ax2D

    def __init__(self, pos: Ax2D = Ax2D()) -> None:
        self._pos = pos.copy()

    @staticmethod
    def from_point_dir(point: Point2D, direction: Dir2D) -> Lin2D:
        ax2d = Ax2D(loc=point, dir=direction)
        return Lin2D(pos=ax2d)

    @staticmethod
    def from_abc(a: float, b: float, c: float) -> Lin2D:
        norm2 = a * a + b * b
        if norm2 < sys.float_info.epsilon:
            raise ValueError("Invalid line coefficients: a and b cannot both be zero.")
        p = Point2D(-a * c / norm2, -b * c / norm2)
        d = Dir2D(-b, a)
        return Lin2D.from_point_dir(p, d)

    def __str__(self) -> str:
        return f"Lin2D(pos={self._pos})"

    @property
    def pos(self) -> Ax2D:
        return self._pos

    @pos.setter
    def pos(self, value: Ax2D) -> None:
        self._pos = value

    def copy(self) -> Lin2D:
        return Lin2D(self._pos.copy())

    @property
    def loc(self) -> Point2D:
        return self._pos.loc

    @loc.setter
    def location(self, point: Point2D) -> None:
        self._pos.loc = point

    @property
    def dir(self) -> Dir2D:
        return self._pos.dir

    @dir.setter
    def dir(self, direction: Dir2D) -> None:
        self._pos.dir = direction

    def reverse(self):
        self._pos.reverse()

    @property
    def coefficients(self):
        a = self._pos.dir.y
        b = -self._pos.dir.x
        c = -(a * self._pos.loc.x + b * self._pos.loc.y)
        return (a, b, c)

    def angle(self, other: Lin2D) -> float:
        return self._pos.dir.angle(other.pos.dir)

    def distance_to_point(self, point: Point2D) -> float:
        xy = point.coord.copy()
        xy -= self._pos.loc.coord
        return abs(xy.cross(self._pos.dir.coord))

    def distance_to_line(self, other: Lin2D) -> float:
        d = 0.0
        if self._pos.is_parallel_to(other.pos):
            d = other.distance_to_point(self._pos.loc)
        return d

    def normal_line(self, point: Point2D) -> Lin2D:
        dir_perp = Dir2D(-self._pos.dir.y, self._pos.dir.x)
        return Lin2D.from_point_dir(point, dir_perp)

    def mirror_by_point(self, point: Point2D) -> Lin2D:
        self._pos.mirror_by_point(point)
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D) -> Lin2D:
        self._pos.mirror_by_ax2d(ax2d)
        return self

    def rotate(self, point: Point2D, angle: float) -> Lin2D:
        self._pos.rotate(point, angle)
        return self

    def scale(self, point: Point2D, factor: float) -> Lin2D:
        self._pos.loc.scale(point, factor)
        return self

    def transform(self, trsf2d: Trsf2D) -> Lin2D:
        self._pos.transform(trsf2d)
        return self

    def translate_by_vec(self, vec2d: Dir2D) -> Lin2D:
        self._pos.loc.translate_by_vec(vec2d)
        return self

    def translate_by_2points(self, p1: Point2D, p2: Point2D) -> Lin2D:
        self._pos.loc.translate_by_2points(p1, p2)
        return self
