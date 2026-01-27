from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Vec2D import Vec2D

from ..config import TOLERANCE
from ._Point2D import Point2D
from ._Dir2D import Dir2D


class Ax2D:
    _loc: Point2D
    _dir: Dir2D

    def __init__(self, loc: Point2D = Point2D(), dir: Dir2D = Dir2D()) -> None:
        self._loc = loc
        self._dir = dir

    def __str__(self) -> str:
        return f"Ax2D(loc={self._loc}, dir={self._dir})"

    @property
    def loc(self) -> Point2D:
        return self._loc

    @loc.setter
    def loc(self, value: Point2D) -> None:
        self._loc = value

    @property
    def dir(self) -> Dir2D:
        return self._dir

    @dir.setter
    def dir(self, value: Dir2D) -> None:
        self._dir = value

    def copy(self) -> Ax2D:
        return Ax2D(self._loc.copy(), self._dir.copy())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ax2D):
            return NotImplemented
        return self._loc == other._loc and self._dir == other._dir

    def is_coaxial_to(self, other: Ax2D):
        xy1 = self._loc._coord - other._loc._coord
        d1 = abs(xy1.cross(self._dir._coord))
        xy2 = other._loc._coord - self._loc._coord
        d2 = abs(xy2.cross(other._dir._coord))
        return (
            self._dir.is_parallel_to(other._dir) and d1 < TOLERANCE and d2 < TOLERANCE
        )

    def is_normal_to(self, other: Ax2D):
        return self._dir.is_normal_to(other._dir)

    def is_opposite_to(self, other: Ax2D):
        return self._dir.is_opposite_to(other._dir)

    def is_parallel_to(self, other: Ax2D):
        return self._dir.is_parallel_to(other._dir)

    def angle(self, other: Ax2D) -> float:
        return self._dir.angle(other._dir)

    def reverse(self) -> Ax2D:
        self._dir.reverse()
        return self

    def mirror_by_point(self, point: Point2D) -> Ax2D:
        self._loc.mirror_by_point(point)
        self._dir.reverse()
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D) -> Ax2D:
        self._loc.mirror_by_ax2d(ax2d)
        self.dir.mirror_by_dir2d(ax2d.dir)
        return self

    def rotate(self, point: Point2D, angle: float) -> Ax2D:
        self._loc.rotate(point, angle)
        self._dir.rotate(angle)
        return self

    def scale(self, point: Point2D, factor: float) -> Ax2D:
        self._loc.scale(point, factor)
        if factor < 0.0:
            self._dir.reverse()
        return self

    def transform(self, trsf2d) -> Ax2D:
        self._loc.transform(trsf2d)
        self._dir.transform(trsf2d)
        return self

    def translate_by_vec(self, vec2d: Vec2D) -> Ax2D:
        self._loc.translate_by_vec(vec2d)
        return self

    def translate_by_2points(self, p1: Point2D, p2: Point2D) -> Ax2D:
        self._loc.translate_by_2points(p1, p2)
        return self
