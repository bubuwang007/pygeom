from __future__ import annotations

from ..config import TOLERANCE
from ._Point2D import Point2D
from ._Dir2d import Dir2d


class Ax2d:
    _loc: Point2D
    _dir: Dir2d

    def __init__(self, loc: Point2D = Point2D(), dir: Dir2d = Dir2d()) -> None:
        self._loc = loc
        self._dir = dir

    def __str__(self) -> str:
        return f"Ax2d(loc={self._loc}, dir={self._dir})"

    @property
    def loc(self) -> Point2D:
        return self._loc

    @loc.setter
    def loc(self, value: Point2D) -> None:
        self._loc = value

    @property
    def dir(self) -> Dir2d:
        return self._dir

    @dir.setter
    def dir(self, value: Dir2d) -> None:
        self._dir = value

    def copy(self) -> Ax2d:
        return Ax2d(self._loc.copy(), self._dir.copy())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ax2d):
            return NotImplemented
        return self._loc == other._loc and self._dir == other._dir

    def is_coaxial_to(self, other: Ax2d):
        xy1 = self._loc._coord - other._loc._coord
        d1 = abs(xy1.cross(self._dir._coord))
        xy2 = other._loc._coord - self._loc._coord
        d2 = abs(xy2.cross(other._dir._coord))

        print(d1, d2)

        return self._dir.is_parallel_to(other._dir) and d1 < TOLERANCE and d2 < TOLERANCE

        