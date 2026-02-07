from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Point3D import Point3D

from ..config import FLOAT_PRINT_PRECISION
from ._TrsfForm import TrsfForm
from ._Xyz import Xyz
from ._Matrix3D import Matrix3D


class Trsf3D:
    _scale: float
    _trsf_form: TrsfForm
    _matrix: Matrix3D
    _loc: Xyz

    def __init__(
        self,
        scale: float = 1.0,
        trsf_form: TrsfForm = TrsfForm.IDENTITY,
        matrix: Matrix3D = Matrix3D(),
        loc: Xyz = Xyz(0.0, 0.0, 0.0),
    ) -> None:
        self._scale = scale
        self._trsf_form = trsf_form
        self._matrix = matrix
        self._loc = loc

    def __str__(self) -> str:
        return (
            f"Trsf3D(scale={self._scale:.{FLOAT_PRINT_PRECISION}f}, "
            f"trsf_form={self._trsf_form}, "
            f"matrix={self._matrix}, "
            f"loc={self._loc})"
        )

    @property
    def scale(self) -> float:
        return self._scale

    def set_scale(self, point: Point3D, factor: float) -> None:
        if factor < sys.float_info.epsilon:
            raise ValueError("Scale factor must be greater than zero.")
        self._trsf_form = TrsfForm.SCALE
        self._scale = factor
        self._loc = point.coord.copy()
        self._matrix.set_identity()
        self._loc *= 1 - factor

    @property
    def trsf_form(self) -> TrsfForm:
        return self._trsf_form

    @trsf_form.setter
    def trsf_form(self, value: TrsfForm) -> None:
        self._trsf_form = value
        # TODO

    @property
    def matrix(self) -> Matrix3D:
        return self._matrix

    @matrix.setter
    def matrix(self, value: Matrix3D) -> None:
        self._matrix = value

    @property
    def loc(self) -> Xyz:
        return self._loc

    @loc.setter
    def loc(self, value: Xyz) -> None:
        self._loc = value
        # TODO

    def copy(self) -> Trsf3D:
        return Trsf3D(
            self._scale, self._trsf_form, self._matrix.copy(), self._loc.copy()
        )

    def is_negative(self) -> bool:
        return self._scale < 0.0

    def set_point_mirror(self, point: Point3D):
        self._trsf_form = TrsfForm.PNTMIRROR
        self._scale = -1.0
        self._loc = point.coord.copy()
        self._matrix.set_identity()

    def transforms(self, xyz: Xyz) -> Xyz:
        xyz_tmp = self._matrix @ xyz
        if self._scale != 1.0:
            xyz_tmp *= self._scale
        xyz_tmp += self._loc
        xyz.x = xyz_tmp.x
        xyz.y = xyz_tmp.y
        xyz.z = xyz_tmp.z
        return xyz
