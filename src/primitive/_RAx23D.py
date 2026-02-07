from __future__ import annotations

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
                self._xdir = self._axis._dir
                self._axis = ax.copy()
        else:
            self._axis = ax.copy()
            self._xdir = self._axis._dir.cross_cross(self._xdir, self._axis._dir)
            self._ydir = self._axis._dir.cross(self._xdir)

    @property
    def dir(self) -> Dir3D:
        return self._axis.dir

    @dir.setter
    def dir(self, ndir: Dir3D) -> None:
        a = ndir * self._xdir
        if abs(abs(a) - 1.0) < TOLERANCE:
            if a > 0.0:
                self._xdir = self._ydir
                self._ydir = self._axis.dir
                self._axis._dir = ndir.copy()
            else:
                self._xdir = self._axis._dir
                self._axis._dir = ndir.copy()
        else:
            self._axis._dir = ndir.copy()
            self._xdir = ndir.cross_cross(self._xdir, ndir)
            self._ydir = ndir.cross(self._xdir)

    @property
    def loc(self) -> Point3D:
        return self._axis.loc

    @loc.setter
    def loc(self, value: Point3D) -> None:
        self._axis.loc = value

    @property
    def xdir(self) -> Dir3D:
        return self._xdir

    @xdir.setter
    def xdir(self, dir: Dir3D) -> None:
        self._xdir = self._axis._dir.cross_cross(dir, self._axis._dir)
        self._ydir = self._axis._dir.cross(self._xdir)

    @property
    def ydir(self) -> Dir3D:
        return self._ydir

    @ydir.setter
    def ydir(self, dir: Dir3D) -> None:
        self._ydir = dir.cross(self._axis._dir)
        self._xdir = self._axis._dir.cross(self._xdir)

    def angle(self, other: RAx23D) -> float:
        return self._axis.angle(other)

    def is_coplanar_to_rax23d(self, other: RAx23D) -> bool:
        dd = self._axis._dir
        pp = other._axis._loc
        op = self._axis._loc
        d1 = (dd.x * (op.x - pp.x)) + dd.y * (op.y - pp.y) + dd.z * (op.z - pp.z)
        d1 = abs(d1)
        return d1 < TOLERANCE and self._axis.is_parallel_to(other._axis)

    def is_coplanar_to_ax3d(self, other: Ax3D) -> bool:
        dd = self._axis._dir
        pp = self._axis._loc
        ap = other._loc
        d1 = (dd.x * (ap.x - pp.x)) + dd.y * (ap.y - pp.y) + dd.z * (ap.z - pp.z)
        d1 = abs(d1)

        return d1 < TOLERANCE and self._axis.is_parallel_to(other)

    def mirror_by_point(self, point: Point3D) -> RAx23D:
        tmp = self.loc.copy()
        self.mirror_by_point(point)
        self._axis._loc = tmp
        self._xdir.reverse()
        self._ydir.reverse()
        return self

    def mirror_by_ax3d(self, ax3d: Ax3D) -> RAx23D:
        self._ydir.mirror_by_ax3d(ax3d)
        self._xdir.mirror_by_ax3d(ax3d)
        tmp = self.loc.copy()
        tmp.mirror_by_ax3d(ax3d)
        self._axis._loc = tmp
        self._axis._dir = self._xdir.cross(self._ydir)
        return self

    def mirror_by_rax23d(self, rax23d: RAx23D) -> RAx23D:
        self._ydir.mirror_by_rax23d(rax23d)
        self._xdir.mirror_by_rax23d(rax23d)
        tmp = self.loc.copy()
        tmp.mirror_by_rax23d(rax23d)
        self._axis._loc = tmp
        self._axis._dir = self._xdir.cross(self._ydir)
        return self

    def rotate(self, ax3d: Ax3D, angle: float) -> RAx23D:
        tmp = self._axis._loc.copy()
        tmp.rotate(ax3d, angle)
        self._axis._loc = tmp
        self._xdir.rotate(ax3d, angle)
        self._ydir.rotate(ax3d, angle)
        self._axis._dir = self._xdir.cross(self._ydir)
        return self

    def scale(self, point: Point3D, factor: float) -> RAx23D:
        tmp = self._axis._loc.copy()
        tmp.scale(point, factor)
        self._axis._loc = tmp
        if factor < 0.0:
            self._xdir.reverse()
            self._ydir.reverse()
        return self

    def transform(self, trsf3d: Trsf3D) -> RAx23D:
        tmp = self._axis._loc.copy()
        tmp.transform(trsf3d)
        self._axis._loc = tmp
        self._xdir.transform(trsf3d)
        self._ydir.transform(trsf3d)
        self._axis._dir = self._xdir.cross(self._ydir)
        return self

    def translate_by_vec(self, vec: Vec3D) -> RAx23D:
        self._axis.translate_by_vec(vec)
        return self

    def translate_by_2points(self, p1: Point3D, p2: Point3D) -> RAx23D:
        self._axis.translate_by_2points(p1, p2)
        return self
