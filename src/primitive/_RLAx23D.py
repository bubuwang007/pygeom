from __future__ import annotations

import sys
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ._Ax3D import Ax3D
    from ._Trsf3D import Trsf3D

from ..config import TOLERANCE
from ._Point3D import Point3D
from ._Ax3D import Ax3D
from ._Dir3D import Dir3D
from ._Vec3D import Vec3D


# 描述三维空间中的一个坐标系。
# 与 gp_Ax2 坐标系不同，gp_Ax3 可以是：
# - 右手系（direct sense）
# - 左手系（indirect sense）
#
# 一个坐标系由以下内容定义：
# - 原点（也称为“位置点 Location point”）
# - 三个相互正交的单位向量：
#   * X 方向（X Direction）
#   * Y 方向（Y Direction）
#   * 主方向（Direction，也称为 main Direction）
#
# 之所以称为“主方向（main Direction）”，是因为：
# - 当该单位向量被修改时，X 方向和 Y 方向会被重新计算；
# - 但当修改 X 方向或 Y 方向时，主方向不会被修改。
#
# 主方向同时也是坐标系的 Z 方向（Z Direction）。
#
# 主方向始终与 X 方向和 Y 方向的叉积方向平行。
#
# 如果坐标系是右手系，则满足：
#     main Direction = X Direction × Y Direction
#
# 如果坐标系是左手系，则满足：
#     main Direction = -(X Direction × Y Direction)
#
# 坐标系的用途包括：
# - 描述几何实体，尤其用于对几何实体进行定位。
#   一个几何实体的局部坐标系，与 STEP 标准中的
#   “axis placement three axes” 具有相同的语义。
# - 定义几何变换。
#
# 说明：
# - 我们将 X 轴、Y 轴、Z 轴分别定义为：
#   * 以坐标系原点为起点，
#   * 以 X Direction、Y Direction、main Direction
#     作为对应的单位方向向量。
# - Z 轴同时也是主轴（main Axis）。
# - gp_Ax2 仅用于定义始终为右手系的坐标系统。
class RLAx23D:
    _axis: Ax3D
    _xdir: Dir3D
    _ydir: Dir3D

    def __init__(
        self,
        point: Point3D = Point3D(),
        ndir: Dir3D = Dir3D(0.0, 0.0, 1.0),
        xdir: Dir3D = Dir3D(1.0, 0.0, 0.0),
    ) -> None:
        self._axis = Ax3D(point, ndir)
        self._xdir = ndir.cross_cross(xdir, ndir)
        self._ydir = ndir.cross(self._xdir)

    def __str__(self) -> str:
        return f"Ax23D(axis={self._axis}, xdir={self._xdir}, ydir={self._ydir})"

    def copy(self) -> RLAx23D:
        return RLAx23D(self._axis.loc.copy(), self._axis.dir.copy(), self._xdir.copy())

    @property
    def is_direct(self) -> bool:
        # Returns True if the coordinate system is right-handed.
        return self._xdir.cross(self._ydir) @ self._axis.dir > 0.0

    @property
    def direction(self) -> Dir3D:
        return self._axis.dir

    @direction.setter
    def direction(self, dir: Dir3D) -> Ax3D:
        dot = dir @ self._xdir
        if abs(dot) >= 1.0 - TOLERANCE:
            if dot > 0.0:
                self._xdir = self._ydir
                self._ydir = self._axis._dir
            else:
                self._xdir = self._axis._dir
            self._axis._dir = dir.copy()
        else:
            direct = self.is_direct
            self._axis._dir = dir.copy()
            self._xdir = dir.cross_cross(self._xdir, dir)
            if direct:
                self._ydir = dir.cross(self._xdir)
            else:
                self._ydir = self._xdir.cross(dir)

    @property
    def loc(self) -> Point3D:
        return self._axis.loc

    @loc.setter
    def loc(self, value: Point3D) -> None:
        self._axis.loc = value

    @property
    def axis(self) -> Ax3D:
        return self._axis

    @axis.setter
    def axis(self, value: Ax3D) -> None:
        self._axis._loc = value.loc
        self.direction = value.dir

    @property
    def xdir(self) -> Dir3D:
        return self._xdir

    @xdir.setter
    def xdir(self, dir: Dir3D) -> None:
        dot = dir @ self._axis.dir
        if abs(dot) >= 1.0 - TOLERANCE:
            if dot > 0.0:
                self._axis._dir = self._xdir
                self._ydir = -self._ydir
            else:
                self._axis._dir = self._xdir
            self._xdir = dir
        else:
            direct = self.is_direct
            self._xdir = self._axis.dir.cross_cross(dir, self._axis.dir)
            if direct:
                self._ydir = self._axis.dir.cross(self._xdir)
            else:
                self._ydir = self._xdir.cross(self._axis.dir)

    @property
    def ydir(self) -> Dir3D:
        return self._ydir

    @ydir.setter
    def ydir(self, dir: Dir3D) -> None:
        dot = self._ydir @ self._axis.dir
        if abs(dot) >= 1.0 - TOLERANCE:
            if dot > 0.0:
                self._axis._dir = self._ydir
                self._xdir = -self._xdir
            else:
                self._axis._dir = self._ydir
            self._ydir = dir
        else:
            direct = self.is_direct
            self._xdir = dir.cross(self._axis.dir)
            self._ydir = self._axis.dir.cross(self._xdir)
            if not direct:
                self._xdir = -self._xdir

    def x_reverse(self) -> Ax3D:
        self._xdir = self._xdir.reverse()
        return self

    def y_reverse(self) -> Ax3D:
        self._ydir = self._ydir.reverse()
        return self

    def z_reverse(self) -> Ax3D:
        self._axis.dir = self._axis.dir.reverse()
        return self

    def angle(self, other: RLAx23D) -> float:
        return self._axis.angle(other._axis)

    def is_coplanar_to_ax23d(self, other: RLAx23D) -> bool:
        vec = Vec3D.from_2points(self._axis.loc, other._axis.loc)
        d1 = abs(Vec3D.from_dir(self._axis.dir) @ vec)
        d2 = abs(Vec3D.from_dir(other._axis.dir) @ vec)
        return (
            self._axis.is_parallel_to(other._axis) and d1 < TOLERANCE and d2 < TOLERANCE
        )
