from __future__ import annotations

import sys
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Trsf3D import Trsf3D

from ..config import FLOAT_PRINT_PRECISION, TOLERANCE
from ._Xyz import Xyz
from ._Dir3D import Dir3D
from ._Point3D import Point3D


class Vec3D:
    _coord: Xyz

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self._coord = Xyz(x, y, z)

    def __str__(self) -> str:
        return f"Vec3D(x={self._coord.x:.{FLOAT_PRINT_PRECISION}f}, y={self._coord.y:.{FLOAT_PRINT_PRECISION}f}, z={self._coord.z:.{FLOAT_PRINT_PRECISION}f})"

    @staticmethod
    def from_2points(p1: Point3D, p2: Point3D) -> Vec3D:
        return Vec3D(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

    @staticmethod
    def from_dir(dir: Dir3D, length: float = 1.0) -> Vec3D:
        return Vec3D(dir.x * length, dir.y * length, dir.z * length)

    @property
    def coord(self) -> Xyz:
        return self._coord

    @coord.setter
    def coord(self, value: Xyz) -> None:
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

    @property
    def z(self) -> float:
        return self._coord.z

    @z.setter
    def z(self, value: float) -> None:
        self._coord.z = value

    def copy(self) -> Vec3D:
        return Vec3D(self._coord.x, self._coord.y, self._coord.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3D):
            return NotImplemented
        return self._coord == other._coord

    def __getitem__(self, index: int) -> float:
        return self._coord[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._coord[index] = value

    def to_tuple(self) -> tuple[float, float, float]:
        return (self._coord.x, self._coord.y, self._coord.z)

    @property
    def modulus(self) -> float:
        return self._coord.modulus

    @property
    def square_modulus(self) -> float:
        return self._coord.square_modulus

    def angle(self, other: Vec3D):
        if (
            self.modulus < sys.float_info.epsilon
            or other.modulus < sys.float_info.epsilon
        ):
            raise ValueError("Cannot compute angle with zero-length vector")
        return Dir3D(self._coord.x, self._coord.y, self._coord.z).angle(
            Dir3D(other._coord.x, other._coord.y, other._coord.z)
        )

    def angle_with_ref(self, other: Vec3D, ref: Vec3D) -> float:
        if (
            self.modulus < sys.float_info.epsilon
            or other.modulus < sys.float_info.epsilon
            or ref.modulus < sys.float_info.epsilon
        ):
            raise ValueError("Cannot compute angle with zero-length vector")
        return Dir3D(self._coord.x, self._coord.y, self._coord.z).angle_with_ref(
            Dir3D(other._coord.x, other._coord.y, other._coord.z),
            Dir3D(ref._coord.x, ref._coord.y, ref._coord.z),
        )

    def is_normal_to(self, other: Vec3D) -> bool:
        dot_product = self._coord @ other._coord
        return abs(dot_product) < TOLERANCE

    def is_opposite_to(self, other: Vec3D) -> bool:
        angle = abs(self.angle(other))
        return math.pi - angle < TOLERANCE

    def is_parallel_to(self, other: Vec3D) -> bool:
        angle = abs(self.angle(other))
        return angle < TOLERANCE or math.pi - angle < TOLERANCE

    def nomalize(self) -> Vec3D:
        self._coord.normalize()
        return self

    def cross(self, other: Vec3D) -> Vec3D:
        self._coord = self._coord.cross(other._coord)
        return self

    def cross_magnitude(self, other: Vec3D) -> float:
        return self._coord.cross_magnitude(other._coord)

    def square_cross_magnitude(self, other: Vec3D) -> float:
        return self._coord.square_cross_magnitude(other._coord)

    def cross_cross(self, other1: Vec3D, other2: Vec3D) -> Vec3D:
        self._coord = self._coord.cross_cross(other1._coord, other2._coord)
        return self

    def dot_cross(self, other1: Vec3D, other2: Vec3D) -> float:
        return self._coord.dot_cross(other1._coord, other2._coord)

    def reverse(self) -> Vec3D:
        self._coord.x = -self._coord.x
        self._coord.y = -self._coord.y
        self._coord.z = -self._coord.z
        return self

    def __mul__(self, other: Vec3D | int | float) -> Vec3D:
        coord = self._coord * other
        return Vec3D(coord.x, coord.y, coord.z)

    def __rmul__(self, other: int | float) -> Vec3D:
        return Vec3D(
            self._coord.x * other, self._coord.y * other, self._coord.z * other
        )

    def __imul__(self, other: Vec3D | int | float) -> Vec3D:
        self._coord *= other
        return self

    def __truediv__(self, other: int | float) -> Vec3D:
        coord = self._coord / other
        return Vec3D(coord.x, coord.y, coord.z)

    def __rtruediv__(self, other: int | float) -> Vec3D:
        return Vec3D(
            other / self._coord.x, other / self._coord.y, other / self._coord.z
        )

    def __itruediv__(self, other: int | float) -> Vec3D:
        self._coord /= other
        return self

    def __add__(self, other: Vec3D | int | float) -> Vec3D:
        coord = self._coord + other
        return Vec3D(coord.x, coord.y, coord.z)

    def __radd__(self, other: int | float) -> Vec3D:
        return self.__add__(other)

    def __iadd__(self, other: Vec3D | int | float) -> Vec3D:
        self._coord += other
        return self

    def __sub__(self, other: Vec3D | int | float) -> Vec3D:
        coord = self._coord - other
        return Vec3D(coord.x, coord.y, coord.z)

    def __rsub__(self, other: int | float) -> Vec3D:
        return Vec3D(
            other - self._coord.x, other - self._coord.y, other - self._coord.z
        )

    def __isub__(self, other: Vec3D | int | float) -> Vec3D:
        self._coord -= other
        return self

    def __matmul__(self, other: Vec3D) -> float:
        return self._coord @ other._coord

    def __imatmul__(self, other: Vec3D) -> Vec3D:
        self._coord @= other._coord
        return self

    def __neg__(self) -> Vec3D:
        return Vec3D(-self._coord.x, -self._coord.y, -self._coord.z)

    def a1_v1_a2_v2_v3(
        self, a1: float, v1: Vec3D, a2: float, v2: Vec3D, v3: Vec3D
    ) -> Vec3D:
        self._coord.a1_xyz1_a2_xyz2_xyz3(a1, v1._coord, a2, v2._coord, v3._coord)
        return self

    def a1_v1_a2_v2(self, a1: float, v1: Vec3D, a2: float, v2: Vec3D) -> Vec3D:
        self._coord.a1_xyz1_a2_xyz2(a1, v1._coord, a2, v2._coord)
        return self

    def a1_v1_v2(self, a1: float, v1: Vec3D, v2: Vec3D) -> Vec3D:
        self._coord.a1_xyz1_xyz2(a1, v1._coord, v2._coord)
        return self

    def v1_v2(self, v1: Vec3D, v2: Vec3D) -> Vec3D:
        self._coord.xyz1_xyz2(v1._coord, v2._coord)
        return self

    def mirror_by_vec(self, vec: Vec3D):
        pass

    def mirror_by_ax1(self, ax1):
        pass

    def mirror_by_ax2(self, ax2):
        pass

    def rotate(self, ax1, angle: float):
        pass

    def scale(self, factor: float):
        self._coord *= factor
        return self

    def transform(self, trsf: Trsf3D):
        pass
