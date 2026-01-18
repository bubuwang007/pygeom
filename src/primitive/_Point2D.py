from __future__ import annotations

from ._Xy import Xy


class Point2D:
    _coord: Xy

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._coord = Xy(x, y)

    def __str__(self) -> str:
        return f"Point2D(x={self._coord.x}, y={self._coord.y})"

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

    def mirror_by_ax2d(self):
        raise NotImplementedError("mirror_by_ax2d method is not implemented yet.")

    def scale(self, point: Point2D, factor: float) -> Point2D:
        coord = point._coord.copy()
        coord *= 1 - factor
        self._coord *= factor
        self._coord += coord
        return self

    def rotate(self, point: Point2D, angle: float) -> Point2D:
        raise NotImplementedError("rotate method is not implemented yet.")

    def transform(self, trsf2d):
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

    def translate_by_vec(self):
        raise NotImplementedError("translate_by_vec method is not implemented yet.")

    def translate_by_2point(self):
        raise NotImplementedError("translate_by_2point method is not implemented yet.")
