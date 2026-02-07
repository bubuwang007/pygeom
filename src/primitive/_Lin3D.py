from __future__ import annotations

import sys

from ..config import TOLERANCE
from ._Point3D import Point3D
from ._Dir3D import Dir3D
from ._Ax3D import Ax3D
from ._Trsf3D import Trsf3D
from ._Vec3D import Vec3D
from ._RAx23D import RAx23D


class Lin3D:
    _pos: Ax3D

    def __init__(self, pos: Ax3D = Ax3D()) -> None:
        self._pos = pos.copy()

    @staticmethod
    def from_point_dir(point: Point3D, direction: Dir3D) -> Lin3D:
        ax3d = Ax3D(loc=point, dir=direction)
        return Lin3D(pos=ax3d)

    @staticmethod
    def from_2points(p1: Point3D, p2: Point3D) -> Lin3D:
        direction = Dir3D.from_2points(p1, p2)
        return Lin3D.from_point_dir(p1, direction)

    def __str__(self) -> str:
        return f"Lin3D(pos={self._pos})"

    @property
    def pos(self) -> Ax3D:
        return self._pos

    @pos.setter
    def pos(self, value: Ax3D) -> None:
        self._pos = value

    def copy(self) -> Lin3D:
        return Lin3D(self._pos.copy())

    @property
    def loc(self) -> Point3D:
        return self._pos.loc

    @loc.setter
    def loc(self, point: Point3D) -> None:
        self._pos.loc = point

    @property
    def dir(self) -> Dir3D:
        return self._pos.dir

    @dir.setter
    def dir(self, direction: Dir3D) -> None:
        self._pos.dir = direction

    def reverse(self) -> None:
        self._pos.reverse()

    def angle(self, other: Lin3D) -> float:
        return self._pos.angle(other._pos)

    def contains(self, point: Point3D) -> bool:
        return self.distance_to_point(point) < TOLERANCE

    def distance_to_point(self, point: Point3D) -> float:
        xyz = point.coord.copy()
        xyz -= self._pos.loc.coord
        return abs(xyz.cross(self._pos.dir.coord).modulus)

    def distance_to_line(self, other: Lin3D) -> float:
        d = 0.0
        if self._pos.is_parallel_to(other.pos):
            d = other.distance_to_point(self._pos.loc)
        return d

    def normal_line(self, point: Point3D) -> Lin3D:
        dir = Dir3D(
            point.x - self._pos.loc.x,
            point.y - self._pos.loc.y,
            point.z - self._pos.loc.z,
        )
        dir = self.dir.cross_cross(dir, self.dir)
        return Lin3D.from_point_dir(point, dir)

    def mirror_by_point(self, point: Point3D) -> Lin3D:
        self._pos.mirror_by_point(point)
        return self

    def mirror_by_ax3d(self, axis: Ax3D) -> Lin3D:
        self._pos.mirror_by_ax3d(axis)
        return self

    def mirror_by_rax23d(self, rax2: RAx23D) -> Lin3D:
        self._pos.mirror_by_rax23d(rax2)
        return self

    def rotate(self, ax3d: Ax3D, angle: float) -> Lin3D:
        self._pos.rotate(ax3d, angle)
        return self