from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Point2D import Point2D
    from ._Trsf2D import Trsf2D

from ..config import FLOAT_PRINT_PRECISION
from ._TrsfForm import TrsfForm
from ._Xy import Xy
from ._Matrix2D import Matrix2D


class GTrsf2D:
    _scale: float
    _trsf_form: TrsfForm
    _matrix: Matrix2D
    _loc: Xy

    def __init__(
        self,
        scale: float = 1.0,
        trsf_form: TrsfForm = TrsfForm.IDENTITY,
        matrix: Matrix2D = Matrix2D(),
        loc: Xy = Xy(0.0, 0.0),
    ) -> None:
        self._scale = scale
        self._trsf_form = trsf_form
        self._matrix = matrix.copy()
        self._loc = loc.copy()

    @staticmethod
    def from_trsf(trsf: Trsf2D) -> GTrsf2D:
        return GTrsf2D(
            scale=trsf.scale,
            trsf_form=trsf.trsf_form,
            matrix=trsf.matrix,
            loc=trsf.loc,
        )

    def transforms(self, xy: Xy):
        xy_tmp = xy.copy()
        xy_tmp = self._matrix @ xy_tmp
        if self._scale != 1.0:
            xy_tmp *= self._scale
        xy_tmp += self._loc
        xy.x = xy_tmp.x
        xy.y = xy_tmp.y
        return xy
