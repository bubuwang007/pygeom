from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Vec3D import Vec3D

from ..config import TOLERANCE
from ._Point3D import Point3D
from ._Dir3D import Dir3D


class Ax3D:
    _loc: Point3D
    _dir: Dir3D

    def __init__(self, loc: Point3D = Point3D(), dir: Dir3D = Dir3D()) -> None:
        self._loc = loc
        self._dir = dir

    def __str__(self) -> str:
        return f"Ax3D(loc={self._loc}, dir={self._dir})"

    @property
    def loc(self) -> Point3D:
        return self._loc

    @loc.setter
    def loc(self, value: Point3D) -> None:
        self._loc = value

    @property
    def dir(self) -> Dir3D:
        return self._dir

    @dir.setter
    def dir(self, value: Dir3D) -> None:
        self._dir = value

    def copy(self) -> Ax3D:
        return Ax3D(self._loc.copy(), self._dir.copy())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ax3D):
            return NotImplemented
        return self._loc == other._loc and self._dir == other._dir

    def is_coaxial_to(self, other: Ax3D):
        xyz1 = self._loc._coord - other._loc._coord
        d1 = abs(xyz1.cross(self._dir._coord))
        xyz2 = other._loc._coord - self._loc._coord
        d2 = abs(xyz2.cross(other._dir._coord))
        return (
            self._dir.is_parallel_to(other._dir) and d1 < TOLERANCE and d2 < TOLERANCE
        )

    def is_normal_to(self, other: Ax3D):
        return self._dir.is_normal_to(other._dir)

    def is_opposite_to(self, other: Ax3D):
        return self._dir.is_opposite_to(other._dir)

    def is_parallel_to(self, other: Ax3D):
        return self._dir.is_parallel_to(other._dir)

    def angle(self, other: Ax3D) -> float:
        return self._dir.angle(other._dir)

    def reverse(self) -> None:
        self._dir.reverse()
        return self

    def mirror_by_point(self, point: Point3D) -> Ax3D:
        self._loc.mirror_by_point(point)
        self._dir.reverse()
        return self

    def mirror_by_ax3d(self, a1: Ax3D) -> Ax3D:
        self._loc.mirror_by_ax3d(a1)
        self._dir.mirror_by_ax3d(a1)
        return self

    def mirror_by_rax23d(self, a2: Ax3D) -> Ax3D:
        self._loc.mirror_by_rax23d(a2)
        self._dir.mirror_by_rax23d(a2)
        return self

    def rotate(self, point: Point3D, angle: float) -> Ax3D:
        self._loc.rotate(point, angle)
        self._dir.rotate(point, angle)
        return self

    def scale(self, point: Point3D, factor: float) -> Ax3D:
        self._loc.scale(point, factor)
        if factor < 0:
            self._dir.reverse()
        return self

    def transform(self, trsf3d) -> Ax3D:
        self._loc.transform(trsf3d)
        self._dir.transform(trsf3d)
        return self

    def translate_by_vec(self, vec3d: Vec3D) -> Ax3D:
        self._loc.translate_by_vec(vec3d)
        return self

    def translate_by_2points(self, p1: Point3D, p2: Point3D) -> Ax3D:
        self._loc.translate_by_2points(p1, p2)
        return self
