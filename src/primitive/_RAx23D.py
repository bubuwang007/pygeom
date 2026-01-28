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


# 描述三维空间中的一个右手坐标系。
#
# 一个坐标系由以下内容定义：
# - 原点（也称为“位置点 Location point”）
# - 三个相互正交的单位向量，分别称为：
#   * X 方向（X Direction）
#   * Y 方向（Y Direction）
#   * 方向（Direction，也称为主方向 main Direction）
#
# 坐标系中的“方向（Direction）”被称为“主方向（main Direction）”，
# 是因为：
# - 当该单位向量被修改时，X 方向和 Y 方向会被重新计算；
# - 但当修改 X 方向或 Y 方向时，主方向不会被修改。
#
# 主方向同时也是坐标系的 Z 方向（Z Direction）。
#
# 由于 RAx23D 坐标系始终是右手系，
# 因此其主方向始终等于 X 方向与 Y 方向的叉积：
#     main Direction = X Direction × Y Direction
#
# （若需要定义左手坐标系，应使用 RLAx23D。）
#
# 坐标系的用途包括：
# - 描述几何实体，尤其用于对几何实体进行定位。
#   一个几何实体的局部坐标系，在语义上等同于
#   STEP 标准中的 “axis placement two axes”。
# - 定义几何变换。
#
# 说明：
# - 我们将 X 轴、Y 轴、Z 轴分别定义为：
#   * 以坐标系原点作为轴的起点；
#   * 分别以 X Direction、Y Direction、main Direction
#     作为对应的单位方向向量。
# - Z 轴同时也是主轴（main Axis）。
class RAx23D:
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
        return f"RAx23D(axis={self._axis}, xdir={self._xdir}, ydir={self._ydir})"

    def copy(self) -> RAx23D:
        return RAx23D(self._axis.loc.copy(), self._axis.dir.copy(), self._xdir.copy())

    @property
    def axis(self) -> Ax3D:
        return self._axis
    
    @axis.setter
    def axis(self, ax: Ax3D) -> None:
        a = ax._dir * self._xdir
        if abs(abs(a) - 1.0) < TOLERANCE:
            if a > 0.0:
                self._xdir = self._ydir
                self._ydir = self._axis.dir
                self._axis = ax.copy()
            else:
                self._xdir = self._
