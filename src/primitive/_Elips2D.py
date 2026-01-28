from __future__ import annotations

import sys
from math import pi, sqrt

from ._Point2D import Point2D
from ._Dir2D import Dir2D
from ._Ax2D import Ax2D
from ._Ax22D import Ax22D
from ._Trsf2D import Trsf2D


class Elips2D:
    _pos: Ax22D
    _major_radius: float
    _minor_radius: float

    def __init__(
        self,
        pos: Ax22D = Ax22D(),
        major_radius: float = 2.0,
        minor_radius: float = 1.0,
    ) -> None:
        self._pos = pos.copy()
        if major_radius <= 0.0 or minor_radius <= 0.0:
            raise ValueError("Radii must be positive.")
        self._major_radius = major_radius
        self._minor_radius = minor_radius

    @property
    def pos(self) -> Ax22D:
        return self._pos

    @pos.setter
    def pos(self, value: Ax22D) -> None:
        self._pos = value.copy()

    @property
    def major_radius(self) -> float:
        return self._major_radius

    @major_radius.setter
    def major_radius(self, value: float) -> None:
        if value <= 0.0:
            raise ValueError("Major radius must be positive.")
        self._major_radius = value

    @property
    def minor_radius(self) -> float:
        return self._minor_radius

    @minor_radius.setter
    def minor_radius(self, value: float) -> None:
        if value <= 0.0:
            raise ValueError("Minor radius must be positive.")
        self._minor_radius = value

    def __str__(self) -> str:
        return f"Elips2D(major_radius={self._major_radius}, minor_radius={self._minor_radius}, pos={self._pos})"

    def copy(self) -> Elips2D:
        return Elips2D(self._pos.copy(), self._major_radius, self._minor_radius)

    @property
    def location(self) -> Point2D:
        return self._pos.loc

    @location.setter
    def location(self, point: Point2D) -> None:
        self._pos.loc = point.copy()

    @property
    def major_axis(self) -> Dir2D:
        return self._pos.xdir

    @major_axis.setter
    def major_axis(self, direction: Dir2D) -> None:
        self._pos._xdir = direction.copy()

    @property
    def minor_axis(self) -> Dir2D:
        return self._pos.ydir

    @minor_axis.setter
    def minor_axis(self, direction: Dir2D) -> None:
        self._pos._ydir = direction.copy()

    @property
    def area(self) -> float:
        return pi * self._major_radius * self._minor_radius

    @property
    def eccentricity(self) -> float:

        if self._major_radius == 0.0:
            return 0.0
        a = self._major_radius
        b = self._minor_radius
        return sqrt(1.0 - (b * b) / (a * a))

    @property
    def focus1(self) -> Point2D:
        ac = sqrt(self._major_radius**2 - self._minor_radius**2)
        ap = self._pos.loc
        ad = self._pos.xdir
        return Point2D(ap.x + ac * ad.x, ap.y + ac * ad.y)

    @property
    def focus2(self) -> Point2D:
        ac = sqrt(self._major_radius**2 - self._minor_radius**2)
        ap = self._pos.loc
        ad = self._pos.xdir
        return Point2D(ap.x - ac * ad.x, ap.y - ac * ad.y)

    @property
    def focal(self):
        return 2.0 * sqrt(self._major_radius**2 - self._minor_radius**2)

    @property
    def directrix1(self) -> Ax2D:
        e = self.eccentricity
        if e <= sys.float_info.epsilon:
            raise ValueError("Eccentricity is zero, directrix is undefined.")

        o = self._pos.xdir.coord
        o *= self._major_radius / e
        o += self._pos.loc.coord
        return Ax2D(Point2D(o.x, o.y), self._pos.ydir)

    @property
    def directrix2(self) -> Ax2D:
        e = self.eccentricity
        if e <= sys.float_info.epsilon:
            raise ValueError("Eccentricity is zero, directrix is undefined.")

        o = self._pos.xdir.coord
        o *= -(self._major_radius / e)
        o += self._pos.loc.coord
        return Ax2D(Point2D(o.x, o.y), self._pos.ydir)

    @property
    def coefficients(self) -> tuple[float, float, float, float, float, float]:
        # a * (X**2) + b * (Y**2) + 2*c*(X*Y) + 2*d*X + 2*e*Y + f = 0.
        dmin = self._minor_radius**2
        dmaj = self._major_radius**2

        if dmin <= sys.float_info.epsilon or dmaj <= sys.float_info.epsilon:
            return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        t = Trsf2D()
        t.set_transformation_by_ax2d(self._pos.xaxis)
        t11 = t.matrix[0][0]
        t12 = t.matrix[0][1]
        t13 = t.loc.x
        if dmin <= sys.float_info.epsilon:
            a = t11 * t11
            b = t12 * t12
            c = t11 * t12
            d = t11 * t13
            e = t12 * t13
            f = t13 * t13 - dmaj
        else:
            t21 = t.matrix[1][0]
            t22 = t.matrix[1][1]
            t23 = t.loc.y
            a = (t11 * t11) / dmaj + (t21 * t21) / dmin
            b = (t12 * t12) / dmaj + (t22 * t22) / dmin
            c = (t11 * t12) / dmaj + (t21 * t22) / dmin
            d = (t11 * t13) / dmaj + (t21 * t23) / dmin
            e = (t12 * t13) / dmaj + (t22 * t23) / dmin
            f = (t13 * t13) / dmaj + (t23 * t23) / dmin - 1.0

        return (a, b, c, d, e, f)

    @property
    def parameter(self):
        if self._major_radius == 0.0:
            return 0.0
        else:
            return (self._minor_radius**2) / self._major_radius

    def scale(self, point: Point2D, factor: float) -> Elips2D:
        self._pos.loc.scale(point, factor)
        self._major_radius *= abs(factor)
        self._minor_radius *= abs(factor)
        return self

    def mirror_by_point(self, point: Point2D) -> Elips2D:
        self._pos.mirror_by_point(point)
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D) -> Elips2D:
        self._pos.mirror_by_ax2d(ax2d)
        return self

    def reverse(self) -> Elips2D:
        tmp = self._pos.ydir.copy()
        tmp.reverse()

        self._pos = Ax22D(
            self._pos.loc.copy(),
            self._pos.xdir.copy(),
            tmp,
        )
        return self

    def translate_by_vec(self, vec2d: Dir2D) -> Elips2D:
        self._pos.loc.translate_by_vec(vec2d)
        return self

    def translate_by_2points(self, p1: Point2D, p2: Point2D) -> Elips2D:
        self._pos.loc.translate_by_2points(p1, p2)
        return self

    def transform(self, trsf2d: Trsf2D) -> Elips2D:
        self._major_radius *= trsf2d.scale
        self._minor_radius *= trsf2d.scale
        self._pos.transform(trsf2d)
        return self

    def rotate(self, point: Point2D, angle: float) -> Elips2D:
        self._pos.rotate(point, angle)
        return self

    @property
    def is_direct(self) -> bool:
        return self._pos.xdir.cross(self._pos.ydir) >= 0.0
