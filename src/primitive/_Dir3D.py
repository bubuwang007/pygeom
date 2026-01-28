from __future__ import annotations

import sys
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from ..config import FLOAT_PRINT_PRECISION, TOLERANCE
from ._Xyz import Xyz


class Dir3D:
    _coord: Xyz

    def __init__(self, x: float = 1.0, y: float = 0.0, z: float = 0.0) -> None:
        self._coord = Xyz(x, y, z)
        self.normalize()

    def normalize(self) -> None:
        mod = self._coord.modulus
        if mod < sys.float_info.epsilon:
            raise ValueError("Cannot normalize a zero-length direction vector.")
        self._coord /= mod

    def __str__(self) -> str:
        return f"Dir3D(x={self._coord.x:.{FLOAT_PRINT_PRECISION}f}, y={self._coord.y:.{FLOAT_PRINT_PRECISION}f}, z={self._coord.z:.{FLOAT_PRINT_PRECISION}f})"

    @property
    def coord(self) -> Xyz:
        return self._coord

    @coord.setter
    def coord(self, value: Xyz) -> None:
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

    @property
    def z(self) -> float:
        return self._coord.z

    @z.setter
    def z(self, value: float) -> None:
        self._coord.z = value
        self.normalize()

    def copy(self) -> Dir3D:
        return Dir3D(self._coord.x, self._coord.y, self._coord.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dir3D):
            return NotImplemented
        return self._coord == other._coord

    def __getitem__(self, index: int) -> float:
        return self._coord[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._coord[index] = value
        self.normalize()

    def to_tuple(self) -> tuple[float, float, float]:
        return (self._coord.x, self._coord.y, self._coord.z)

    def is_normal_to(self, other: Dir3D) -> bool:
        dot_product = (
            self._coord.x * other._coord.x
            + self._coord.y * other._coord.y
            + self._coord.z * other._coord.z
        )
        return abs(dot_product) < TOLERANCE

    def is_opposite_to(self, other: Dir3D) -> bool:
        return math.pi - self.angle(other) < TOLERANCE

    def is_parallel_to(self, other: Dir3D) -> bool:
        angle = self.angle(other)
        return angle < TOLERANCE or math.pi - angle < TOLERANCE

    def angle(self, other: Dir3D) -> float:
        # 当角度大于 45 度时，使用 arccos 来计算角度能获得更好的精度。
        # 否则（角度较小），使用 arcsin 会更合适。
        # 当角度接近 0 度或接近 90 度时，所产生的误差都远非可以忽略。
        # 在三维空间中，角度值始终为正，并且位于 0 到 PI 之间。
        cos = self._coord @ other._coord
        if cos > -0.70710678118655 and cos < 0.70710678118655:
            return math.acos(cos)
        else:
            sin = (self._coord.cross(other._coord)).modulus
            if cos < 0.0:
                return math.pi - math.asin(sin)
            else:
                return math.asin(sin)

    def angle_with_ref(self, other: Dir3D, ref: Dir3D):
        # 计算向量 <me> 与 <other> 之间的有向角。
        # <ref> 是一个参考方向，垂直于 <me> 与 <other> 所在的平面，
        # 它的方向决定了旋转的正方向。
        # 如果叉积 <me> ^ <other> 的方向与 <ref> 相同，
        # 则角度值为正；否则为负。
        # 返回的角度值范围为 [-PI, PI]（单位：弧度）。

        xyz = self._coord.cross(other._coord)
        cos = self._coord @ other._coord
        sin = xyz.modulus

        if cos > -0.70710678118655 and sin < 0.70710678118655:
            angle = math.acos(cos)
        else:
            if cos < 0.0:
                angle = math.pi - math.asin(sin)
            else:
                angle = math.asin(sin)
        if xyz @ ref._coord >= 0:
            return angle
        else:
            return -angle

    def cross(self, other: Dir3D) -> Dir3D:
        xyz = self._coord.cross(other._coord)
        return Dir3D(xyz.x, xyz.y, xyz.z)

    def __matmul__(self, other: Dir3D) -> float:
        return self._coord @ other._coord

    def __neg__(self) -> Dir3D:
        return Dir3D(-self._coord.x, -self._coord.y, -self._coord.z)

    def reverse(self) -> Dir3D:
        self._coord.x = -self._coord.x
        self._coord.y = -self._coord.y
        self._coord.z = -self._coord.z
        return self

    def cross_cross(self, dir1: Dir3D, dir2: Dir3D) -> Dir3D:
        xyz = self._coord.cross_cross(dir1._coord, dir2._coord)
        return Dir3D(xyz.x, xyz.y, xyz.z)

    def rotate(self, ax1, angle):
        raise NotImplementedError

    def mirror_by_ax3d(self):
        raise NotImplementedError

    def mirror_by_ax23d(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError
