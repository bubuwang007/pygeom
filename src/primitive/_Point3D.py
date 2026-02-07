from __future__ import annotations

from ._Xyz import Xyz

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Trsf3D import Trsf3D


class Point3D:
    _coord: Xyz

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self._coord = Xyz(x, y, z)

    def __str__(self) -> str:
        return f"Point3D(x={self._coord.x}, y={self._coord.y}, z={self._coord.z})"

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

    def copy(self) -> Point3D:
        return Point3D(self._coord.x, self._coord.y, self._coord.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point3D):
            return NotImplemented
        return self._coord == other._coord

    def __getitem__(self, index: int) -> float:
        return self._coord[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._coord[index] = value

    def to_tuple(self) -> tuple[float, float, float]:
        return (self._coord.x, self._coord.y, self._coord.z)

    def distance(self, other: Point3D) -> float:
        dx = self._coord.x - other._coord.x
        dy = self._coord.y - other._coord.y
        dz = self._coord.z - other._coord.z
        return (dx**2 + dy**2 + dz**2) ** 0.5

    def mirror_by_point(self, point: Point3D) -> Point3D:
        self._coord.reverse()
        self._coord += point._coord * 2
        return self

    def mirror_by_ax3d(self):
        raise NotImplementedError
    
    def mirror_by_rax23d(self):
        raise NotImplementedError

    def scale(self, point: Point3D, factor: float) -> Point3D:
        coord = point._coord.copy()
        coord *= 1 - factor
        self._coord *= factor
        self._coord += coord
        return self

    def rotate(self, point: Point3D, angle: float) -> Point3D:
        raise NotImplementedError("rotate method is not implemented yet.")

    def transform(self) -> Point3D:
        raise NotImplementedError("transform method is not implemented yet.")

    def translate_by_vec(self):
        raise NotImplementedError("translate_by_vec method is not implemented yet.")

    def translate_by_2points(self):
        raise NotImplementedError("translate_by_2point method is not implemented yet.")
