from __future__ import annotations

from math import pi

from ._Point2D import Point2D
from ._Dir2D import Dir2D
from ._Ax2D import Ax2D
from ._Ax22D import Ax22D
from ._Trsf2D import Trsf2D


class Circ2D:
    _pos: Ax22D
    _radius: float

    def __init__(self, pos: Ax22D = Ax22D(), radius: float = 1.0) -> None:
        self._pos = pos
        if radius <= 0.0:
            raise ValueError("Radius must be positive.")
        self._radius = radius

    def __str__(self) -> str:
        return f"Circ2D(radius={self._radius}, pos={self._pos})"

    @property
    def pos(self) -> Ax22D:
        return self._pos

    @pos.setter
    def pos(self, value: Ax22D) -> None:
        self._pos = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0.0:
            raise ValueError("Radius must be positive.")
        self._radius = value

    @property
    def diameter(self) -> float:
        return 2.0 * self._radius

    @diameter.setter
    def diameter(self, value: float) -> None:
        if value <= 0.0:
            raise ValueError("Diameter must be positive.")
        self._radius = value / 2.0

    def copy(self) -> Circ2D:
        return Circ2D(self._pos.copy(), self._radius)

    @property
    def location(self) -> Point2D:
        return self._pos.loc

    @location.setter
    def location(self, point: Point2D) -> None:
        self._pos.loc = point

    @property
    def xdir(self) -> Dir2D:
        return self._pos.xdir

    @xdir.setter
    def xdir(self, dir: Dir2D) -> None:
        self._pos.xdir = dir

    @property
    def ydir(self) -> Dir2D:
        return self._pos.ydir

    @ydir.setter
    def ydir(self, dir: Dir2D) -> None:
        self._pos.ydir = dir

    @property
    def area(self) -> float:
        return pi * self._radius**2

    @property
    def length(self) -> float:
        return 2.0 * pi * self._radius

    def distance_to_point(self, point: Point2D) -> float:
        dx = point.x - self._pos.loc.x
        dy = point.y - self._pos.loc.y
        dist_to_center = (dx**2 + dy**2) ** 0.5
        return abs(dist_to_center - self._radius)

    def contains(self, point: Point2D, tol: 1e-6):
        return self.distance_to_point(point) <= tol

    @property
    def coefficients(self):
        # a * (X**2) + b * (Y**2) + 2*c*(X*Y) + 2*d*X + 2*e*Y + f = 0.0
        ax, ay = self._pos.loc.x, self._pos.loc.y
        return (
            1.0,
            1.0,
            0.0,
            -ax,
            -ay,
            ax**2 + ay**2 - self._radius**2,
        )

    def reverse(self):
        tmp = self._pos.ydir.copy()
        tmp.reverse()

        self._pos = Ax22D(
            self._pos.loc.copy(),
            self._pos.xdir.copy(),
            tmp,
        )

    def is_direct(self):
        return self._pos.xdir.cross(self._pos.ydir) >= 0.0

    def mirror_by_point(self, point: Point2D) -> Circ2D:
        self._pos.mirror_by_point(point)
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D) -> Circ2D:
        self._pos.mirror_by_ax2d(ax2d)
        return self

    def rotate(self, point: Point2D, angle: float) -> Circ2D:
        self._pos.rotate(point, angle)
        return self

    def scale(self, point: Point2D, factor: float) -> Circ2D:
        self._pos.loc.scale(point, factor)
        self._radius *= abs(factor)
        return self

    def translate_by_vec(self, vec2d: Dir2D) -> Circ2D:
        self._pos.loc.translate_by_vec(vec2d)
        return self

    def translate_by_2points(self, p1: Point2D, p2: Point2D) -> Circ2D:
        self._pos.loc.translate_by_2points(p1, p2)
        return self

    def transform(self, trsf2d: Trsf2D) -> Circ2D:
        self._radius *= trsf2d.scale
        self._pos.transform(trsf2d)
        return self
