from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Vec2D import Vec2D
    from ._Ax2D import Ax2D
    from ._Trsf2D import Trsf2D

from ..config import FLOAT_PRINT_PRECISION
from ._Xy import Xy


class Point2D:
    _coord: Xy

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._coord = Xy(x, y)

    def __str__(self) -> str:
        return f"Point2D(x={self._coord.x:.{FLOAT_PRINT_PRECISION}f}, y={self._coord.y:.{FLOAT_PRINT_PRECISION}f})"

    @property
    def coord(self) -> Xy:
        return self._coord

    @coord.setter
    def coord(self, value: Xy) -> None:
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

    def copy(self) -> Point2D:
        return Point2D(self._coord.x, self._coord.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self._coord == other._coord

    def __getitem__(self, index: int) -> float:
        return self._coord[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._coord[index] = value

    def to_tuple(self) -> tuple[float, float]:
        return (self._coord.x, self._coord.y)

    def distance(self, other: Point2D) -> float:
        dx = self._coord.x - other._coord.x
        dy = self._coord.y - other._coord.y
        return (dx**2 + dy**2) ** 0.5

    def mirror_by_point(self, point: Point2D) -> Point2D:
        self._coord.reverse()
        self._coord += point._coord * 2
        return self

    def mirror_by_ax2d(self, ax2d: Ax2D) -> Point2D:
        from ._Trsf2D import Trsf2D

        trsf = Trsf2D()
        trsf.set_ax2d_mirror(ax2d)
        trsf.transforms(self._coord)
        return self

    def scale(self, point: Point2D, factor: float) -> Point2D:
        coord = point._coord.copy()
        coord *= 1 - factor
        self._coord *= factor
        self._coord += coord
        return self

    def rotate(self, point: Point2D, angle: float) -> Point2D:
        from ._Trsf2D import Trsf2D

        trsf = Trsf2D()
        trsf.set_rotation(point, angle)
        trsf.transforms(self._coord)
        return self

    def transform(self, trsf2d: Trsf2D):
        from ._TrsfForm import TrsfForm

        if trsf2d.trsf_form == TrsfForm.IDENTITY:
            return
        elif trsf2d.trsf_form == TrsfForm.TRANSLATION:
            self._coord += trsf2d.loc
        elif trsf2d.trsf_form == TrsfForm.SCALE:
            self._coord *= trsf2d.scale
            self._coord += trsf2d.loc
        elif trsf2d.trsf_form == TrsfForm.PNTMIRROR:
            self._coord.reverse()
            self._coord += trsf2d.loc
        else:
            trsf2d.transforms(self._coord)
        return self

    def translate_by_vec(self, vec: Vec2D):
        self._coord += vec.coord
        return self

    def translate_by_2points(self, p1: Point2D, p2: Point2D):
        self._coord += p2._coord
        self._coord -= p1._coord
        return self
