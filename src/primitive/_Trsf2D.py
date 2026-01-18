from __future__ import annotations

import sys
import numpy as np

from ._TrsfForm import TrsfForm
from ._Matrix2D import Matrix2D
from ._Point2D import Point2D
from ._Xy import Xy
from ._Vec2d import Vec2d


# Defines a non-persistent transformation in 2D space.
# The following transformations are implemented :
# - Translation, Rotation, Scale
# - Symmetry with respect to a point and a line.
# Complex transformations can be obtained by combining the
# previous elementary transformations using the method Multiply.
# The transformations can be represented as follow :
# @code
#    V1   V2   T       XY        XY
# | a11  a12  a13 |   | x |     | x'|
# | a21  a22  a23 |   | y |     | y'|
# |  0    0    1  |   | 1 |     | 1 |
# @endcode
# where {V1, V2} defines the vectorial part of the transformation
# and T defines the translation part of the transformation.
# This transformation never change the nature of the objects.
class Trsf2D:
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
        self._matrix = matrix
        self._loc = loc

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        self._scale = value

    @property
    def trsf_form(self) -> TrsfForm:
        return self._trsf_form

    @trsf_form.setter
    def trsf_form(self, value: TrsfForm) -> None:
        self._trsf_form = value

    @property
    def matrix(self) -> Matrix2D:
        return self._matrix

    @matrix.setter
    def matrix(self, value: Matrix2D) -> None:
        self._matrix = value

    @property
    def loc(self) -> Xy:
        return self._loc

    @loc.setter
    def loc(self, value: Xy) -> None:
        self._loc = value

    def copy(self) -> Trsf2D:
        return Trsf2D(
            self._scale,
            self._trsf_form,
            self._matrix.copy(),
            self._loc.copy(),
        )

    def is_negative(self) -> bool:
        return self._matrix.determinant < 0.0

    def set_point_mirror(self, point: Point2D) -> None:
        self._trsf_form = TrsfForm.PNTMIRROR
        self._scale = -1.0
        self._matrix.set_identity()
        self._loc = point.coord * 2

    def set_ax2d_mirror(self, point: Point2D, ax2d_dir) -> None:
        raise NotImplementedError("set_ax2d_mirror method is not implemented yet.")

    def set_rotation(self, point: Point2D, angle: float) -> None:
        self._trsf_form = TrsfForm.ROTATION
        self._scale = 1.0
        self._loc = point.coord.copy()
        self._loc.reverse()
        self._matrix.set_rotation(angle)
        self._loc = self._matrix @ self._loc

    def set_scale(self, point: Point2D, factor: float) -> None:
        self._trsf_form = TrsfForm.SCALE
        self._scale = factor
        self._matrix.set_identity()
        self._loc = point.coord.copy()
        self._loc *= 1 - factor

    def set_translation_by_vec2d(self, vec: Vec2d) -> None:
        self._trsf_form = TrsfForm.TRANSLATION
        self._scale = 1.0
        self._matrix.set_identity()
        self._loc = vec.coord.copy()

    def set_translation_by_2point(self, p1: Point2D, p2: Point2D) -> None:
        self._trsf_form = TrsfForm.TRANSLATION
        self._scale = 1.0
        self._matrix.set_identity()
        self._loc = p2.coord - p1.coord

    def set_transformation_by_2ax2d(self):
        pass

    def set_transformation_by_ax2d(self):
        pass

    def transforms(self, xy: Xy):
        xy_tmp = xy.copy()
        xy_tmp = self._matrix @ xy_tmp
        if self._scale != 1.0:
            xy_tmp *= self._scale
        xy_tmp += self._loc
        xy.x = xy_tmp.x
        xy.y = xy_tmp.y
        return xy

    def invert(self):
        # X' = scale * R * X + T  =>  X = (R  / scale)  * ( X' - T)
        if self._trsf_form == TrsfForm.IDENTITY:
            return
        elif (
            self._trsf_form == TrsfForm.TRANSLATION
            or self._trsf_form == TrsfForm.PNTMIRROR
        ):
            self._loc.reverse()
        elif self._trsf_form == TrsfForm.SCALE:
            if self._scale < sys.float_info.epsilon:
                raise ValueError("Cannot invert a transformation with zero scale.")
            self._scale = 1.0 / self._scale
            self._matrix.transpose()
            self._loc = (self._matrix @ self._loc) * -self._scale
        else:
            if self._scale < sys.float_info.epsilon:
                raise ValueError("Cannot invert a transformation with zero scale.")
            self._scale = 1.0 / self._scale
            self._matrix.transpose()
            self._loc = (self._matrix @ self._loc) * -self._scale

    def __matmul__(self, other: Trsf2D):
        if not isinstance(other, Trsf2D):
            return NotImplemented

        if other._trsf_form == TrsfForm.IDENTITY:
            return self.copy()
        elif self._trsf_form == TrsfForm.IDENTITY:
            return other.copy()
        elif (
            self._trsf_form == TrsfForm.ROTATION
            and self._trsf_form == TrsfForm.ROTATION
        ):
            new = self.copy()
            if new._loc != Xy(0.0, 0.0):
                new._loc += self._matrix @ other._loc
            new._matrix = self._matrix @ other._matrix
            return new
