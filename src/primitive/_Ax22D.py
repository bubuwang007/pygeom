from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ._Ax2D import Ax2D
    from ._Trsf2D import Trsf2D

from ._Point2D import Point2D
from ._Ax2D import Ax2D
from ._Dir2D import Dir2D


class Ax22D:
    _loc: Point2D
    _xdir: Dir2D
    _ydir: Dir2D

    def __init__(
        self,
        loc: Point2D = Point2D(),
        xdir: Dir2D = Dir2D(1.0, 0.0),
        ydir: Dir2D = Dir2D(0.0, 1.0),
    ) -> None:
        self._loc = loc
        self._xdir = xdir
        self._ydir = ydir

        v = self._xdir.cross(self._ydir)
        if v >= 0.0:
            self._ydir.x = -self._xdir.y
            self._ydir.y = self._xdir.x
        else:
            self._ydir.x = self._xdir.y
            self._ydir.y = -self._xdir.x

    def __str__(self) -> str:
        return f"Ax22D(loc={self._loc}, xdir={self._xdir}, ydir={self._ydir})"

    def copy(self) -> Ax22D:
        return Ax22D(self._loc.copy(), self._xdir.copy(), self._ydir.copy())

    @property
    def loc(self) -> Point2D:
        return self._loc

    @loc.setter
    def loc(self, value: Point2D) -> None:
        self._loc = value

    @property
    def xdir(self) -> Dir2D:
        return self._xdir

    @xdir.setter
    def xdir(self, value: Dir2D) -> None:
        is_sign = self._xdir.cross(value) >= 0.0
        self._xdir = value
        if is_sign:
            self._ydir.x = -self._xdir.y
            self._ydir.y = self._xdir.x
        else:
            self._ydir.x = self._xdir.y
            self._ydir.y = -self._xdir.x

    @property
    def xaxis(self) -> Ax2D:
        return Ax2D(self._loc, self._xdir)

    @xaxis.setter
    def xaxis(self, value: Ax2D) -> None:
        is_sign = self._xdir.cross(self._ydir) >= 0.0
        self._loc = value.loc
        self._xdir = value.dir
        if is_sign:
            self.ydir.x, self.ydir.y = -value.dir.y, value.dir.x
        else:
            self.ydir.x, self.ydir.y = value.dir.y, -value.dir.x

    @property
    def ydir(self) -> Dir2D:
        return self._ydir

    @ydir.setter
    def ydir(self, value: Dir2D) -> None:
        is_sign = self._xdir.cross(value) >= 0.0
        self._ydir = value
        if is_sign:
            self._xdir.x = self._ydir.y
            self._xdir.y = -self._ydir.x
        else:
            self._xdir.x = -self._ydir.y
            self._xdir.y = self._ydir.x

    @property
    def yaxis(self) -> Ax2D:
        return Ax2D(self._loc, self._ydir)

    @yaxis.setter
    def yaxis(self, value: Ax2D) -> None:
        is_sign = self._xdir.cross(self._ydir) >= 0.0
        self._loc = value.loc
        self._ydir = value.dir
        if is_sign:
            self._xdir.x, self._xdir.y = value.dir.y, -value.dir.x
        else:
            self._xdir.x, self._xdir.y = -value.dir.y, value.dir.x

    def mirror_by_point(self, point: Point2D) -> Ax22D:
        self._loc.mirror_by_point(point)
        self._xdir.reverse()
        self._ydir.reverse()
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D) -> Ax22D:
        self._loc.mirror_by_ax2d(ax2d)
        self._xdir.mirror_by_ax2d(ax2d)
        self._ydir.mirror_by_ax2d(ax2d)
        return self

    def rotate(self, point: Point2D, angle: float) -> Ax22D:
        self._loc.rotate(point, angle)
        self._xdir.rotate(angle)
        self._ydir.rotate(angle)
        return self

    def scale(self, point: Point2D, factor: float) -> Ax22D:
        self._loc.scale(point, factor)
        if factor < 0.0:
            self._xdir.reverse()
            self._ydir.reverse()
        return self

    def transform(self, trsf2d: Trsf2D) -> Ax22D:
        self._loc.transform(trsf2d)
        self._xdir.transform(trsf2d)
        self._ydir.transform(trsf2d)
        return self
