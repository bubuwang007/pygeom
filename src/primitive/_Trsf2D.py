from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._Ax2D import Ax2D
    from ._Point2D import Point2D
    from ._Vec2D import Vec2D

from ..config import FLOAT_PRINT_PRECISION
from ._TrsfForm import TrsfForm
from ._Xy import Xy
from ._Matrix2D import Matrix2D


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

    def __str__(self):
        return (
            f"Trsf2D(scale={self._scale:.{FLOAT_PRINT_PRECISION}f}, trsf_form={self._trsf_form.name}, "
            f"matrix={self._matrix}, loc={self._loc})"
        )

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        if value == 1.0:
            x = abs(self._loc.x)
            y = abs(self._loc.y)
            if (x < sys.float_info.epsilon) and (y < sys.float_info.epsilon):
                if self._trsf_form in {
                    TrsfForm.IDENTITY,
                    TrsfForm.ROTATION,
                }:
                    pass
                elif self._trsf_form == TrsfForm.SCALE:
                    self._trsf_form = TrsfForm.IDENTITY
                elif self._trsf_form == TrsfForm.PNTMIRROR:
                    self._trsf_form = TrsfForm.TRANSLATION
                else:
                    self._trsf_form = TrsfForm.COMPOUNDTRSF
            else:
                if self._trsf_form in {
                    TrsfForm.IDENTITY,
                    TrsfForm.ROTATION,
                    TrsfForm.SCALE,
                }:
                    pass
                elif self._trsf_form == TrsfForm.PNTMIRROR:
                    self._trsf_form = TrsfForm.TRANSLATION
                else:
                    self._trsf_form = TrsfForm.COMPOUNDTRSF
        elif value == -1.0:
            if self._trsf_form in {
                TrsfForm.IDENTITY,
                TrsfForm.AX1MIRROR,
            }:
                pass
            elif self._trsf_form in {TrsfForm.IDENTITY, TrsfForm.SCALE}:
                self._trsf_form = TrsfForm.PNTMIRROR
            else:
                self._trsf_form = TrsfForm.COMPOUNDTRSF
        else:
            if self._trsf_form == TrsfForm.SCALE:
                pass
            elif self._trsf_form in {
                TrsfForm.IDENTITY,
                TrsfForm.TRANSLATION,
                TrsfForm.PNTMIRROR,
            }:
                self._trsf_form = TrsfForm.SCALE
            else:
                self._trsf_form = TrsfForm.COMPOUNDTRSF
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
        self._loc.x = value.x
        self._loc.y = value.y

        if (abs(self._loc.x) < sys.float_info.epsilon) and (
            abs(self._loc.y) < sys.float_info.epsilon
        ):
            if self._trsf_form in {
                TrsfForm.IDENTITY,
                TrsfForm.PNTMIRROR,
                TrsfForm.SCALE,
                TrsfForm.ROTATION,
                TrsfForm.AX1MIRROR,
            }:
                pass
            elif self._trsf_form == TrsfForm.TRANSLATION:
                self._trsf_form = TrsfForm.IDENTITY
            else:
                self._trsf_form = TrsfForm.COMPOUNDTRSF
        else:
            if self._trsf_form in {
                TrsfForm.TRANSLATION,
                TrsfForm.SCALE,
                TrsfForm.PNTMIRROR,
            }:
                pass
            elif self._trsf_form == TrsfForm.IDENTITY:
                self._trsf_form = TrsfForm.TRANSLATION
            else:
                self._trsf_form = TrsfForm.COMPOUNDTRSF

    def copy(self) -> Trsf2D:
        return Trsf2D(
            self._scale,
            self._trsf_form,
            self._matrix.copy(),
            self._loc.copy(),
        )

    @property
    def is_negative(self) -> bool:
        return self._matrix.determinant < 0.0

    def set_point_mirror(self, point: Point2D) -> None:
        self._trsf_form = TrsfForm.PNTMIRROR
        self._scale = -1.0
        self._matrix.set_identity()
        self._loc = point.coord * 2

    def set_ax2d_mirror(self, ax2d: Ax2D) -> None:
        self._trsf_form = TrsfForm.AX1MIRROR
        self._scale = -1.0
        v = ax2d.dir
        p = ax2d.loc
        vx, vy = v.x, v.y
        x0, y0 = p.x, p.y

        self._matrix[0, 0] = 1.0 - 2.0 * vx * vx
        self._matrix[1, 0] = -2.0 * vx * vy
        self._matrix[0, 1] = -2.0 * vx * vy
        self._matrix[1, 1] = 1.0 - 2.0 * vy * vy

        self._loc.x = -2.0 * ((vx * vy - 1.0) * x0 + vx * vy * y0)
        self._loc.y = -2.0 * (vx * vy * x0 + (vy * vx - 1.0) * y0)

    def set_rotation(self, point: Point2D, angle: float) -> None:
        self._trsf_form = TrsfForm.ROTATION
        self._scale = 1.0
        self._loc = point.coord.copy()
        self._loc.reverse()
        self._matrix.set_rotation(angle)
        self._loc = self._matrix @ self._loc
        self._loc += point.coord

    def set_scale(self, point: Point2D, factor: float) -> None:
        self._trsf_form = TrsfForm.SCALE
        self._scale = factor
        self._matrix.set_identity()
        self._loc = point.coord.copy()
        self._loc *= 1 - factor

    def set_translation_by_vec(self, vec: Vec2D) -> None:
        self._trsf_form = TrsfForm.TRANSLATION
        self._scale = 1.0
        self._matrix.set_identity()
        self._loc = vec.coord.copy()

    def set_translation_by_2points(self, p1: Point2D, p2: Point2D) -> None:
        self._trsf_form = TrsfForm.TRANSLATION
        self._scale = 1.0
        self._matrix.set_identity()
        self._loc = p2.coord - p1.coord

    def set_transformation_by_2ax2d(self, a1: Ax2D, a2: Ax2D):
        self._trsf_form = TrsfForm.COMPOUNDTRSF
        self.scale = 1.0

        v1 = a2.dir.coord
        v2 = Xy(-v1.y, v1.x)
        self._matrix[0, 0] = v1.x
        self._matrix[1, 0] = v1.y
        self._matrix[0, 1] = v2.x
        self._matrix[1, 1] = v2.y

        self.loc = a2.loc.coord.copy()
        self._matrix.transpose()
        self.loc -= self._matrix @ a1.loc.coord
        self.loc.reverse()

        v3 = a1.dir.coord
        v4 = Xy(-v3.y, v3.x)
        mat1 = Matrix2D([[v3.x, v4.x], [v3.y, v4.y]])
        mat1_loc = a1.loc.coord.copy()

        mat1_loc = mat1 @ mat1_loc
        self.loc += mat1_loc
        self._matrix @= mat1

    def set_transformation_by_ax2d(self, a: Ax2D):
        self._trsf_form = TrsfForm.COMPOUNDTRSF
        self.scale = 1.0
        v1 = a.dir.coord
        v2 = Xy(-v1.y, v1.x)
        self._matrix[0, 0] = v1.x
        self._matrix[1, 0] = v1.y
        self._matrix[0, 1] = v2.x
        self._matrix[1, 1] = v2.y

        self._loc = a.loc.coord.copy()
        self._matrix.transpose()
        self._loc = self._matrix @ self._loc
        self._loc.reverse()

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

    def multiply(self, other: Trsf2D):
        if not isinstance(other, Trsf2D):
            return NotImplemented

        if other._trsf_form == TrsfForm.IDENTITY:
            pass
        elif self._trsf_form == TrsfForm.IDENTITY:
            self._scale = other._scale
            self._trsf_form = other._trsf_form
            self._matrix = other._matrix.copy()
            self._loc = other._loc.copy()
        elif (
            self._trsf_form == TrsfForm.ROTATION
            and other._trsf_form == TrsfForm.ROTATION
        ):
            # print(1)
            if self._loc != Xy(0.0, 0.0):
                self._loc += self._matrix @ other._loc
            self._matrix @= other._matrix
        elif (
            self._trsf_form == TrsfForm.TRANSLATION
            and other._trsf_form == TrsfForm.TRANSLATION
        ):
            # print(2)
            self._loc += other._loc
        elif self._trsf_form == TrsfForm.SCALE and other._trsf_form == TrsfForm.SCALE:
            # print(3)
            self._loc += other._loc * self._scale
            self._scale *= other._scale
        elif (
            self._trsf_form == TrsfForm.PNTMIRROR
            and other._trsf_form == TrsfForm.PNTMIRROR
        ):
            # print(4)
            self._scale = 1.0
            self._trsf_form = TrsfForm.TRANSLATION
            self._loc += -other._loc
        elif (
            self._trsf_form == TrsfForm.AX1MIRROR
            and other._trsf_form == TrsfForm.AX1MIRROR
        ):
            # print(5)
            self._trsf_form = TrsfForm.ROTATION
            tloc = other.loc.copy()
            tloc = (self._matrix @ tloc) * other.scale
            self._scale *= other.scale
            self._loc += tloc
            self._matrix @= other._matrix
        elif (
            self._trsf_form
            in {TrsfForm.COMPOUNDTRSF, TrsfForm.ROTATION, TrsfForm.AX1MIRROR}
            and other._trsf_form == TrsfForm.TRANSLATION
        ):
            # print(6)
            tloc = other.loc.copy()
            tloc = (self._matrix @ tloc) * self._scale
            self._loc += tloc
        elif (
            self._trsf_form in {TrsfForm.SCALE, TrsfForm.PNTMIRROR}
            and other._trsf_form == TrsfForm.TRANSLATION
        ):
            # print(7)
            tloc = other.loc.copy()
            tloc *= self._scale
            self._loc += tloc
        elif self._trsf_form == TrsfForm.TRANSLATION and other._trsf_form in {
            TrsfForm.COMPOUNDTRSF,
            TrsfForm.ROTATION,
            TrsfForm.AX1MIRROR,
        }:
            # print(8)
            self._trsf_form = TrsfForm.COMPOUNDTRSF
            self._scale = other._scale
            self._loc += other._loc
            self._matrix = other._matrix.copy()
        elif self._trsf_form == TrsfForm.TRANSLATION and (
            other._trsf_form in {TrsfForm.SCALE, TrsfForm.PNTMIRROR}
        ):
            # print(9)
            self._trsf_form = other._trsf_form
            self._loc += other._loc
            self._scale = other._scale
        elif self._trsf_form in {
            TrsfForm.PNTMIRROR,
            TrsfForm.SCALE,
        } and other._trsf_form in {
            TrsfForm.PNTMIRROR,
            TrsfForm.SCALE,
        }:
            # print(10)
            self._trsf_form = TrsfForm.COMPOUNDTRSF
            tloc = other.loc.copy()
            tloc *= self._scale
            self._loc += tloc
            self._scale *= other._scale
        elif self._trsf_form in {
            TrsfForm.COMPOUNDTRSF,
            TrsfForm.ROTATION,
            TrsfForm.AX1MIRROR,
        } and other._trsf_form in {TrsfForm.SCALE, TrsfForm.PNTMIRROR}:
            # print(11)
            self._trsf_form = TrsfForm.COMPOUNDTRSF
            tloc = other.loc.copy()
            tloc = self._matrix @ tloc
            if self._scale == 1.0:
                self._scale = other._scale
            else:
                tloc *= self._scale
                self._scale *= other._scale
            self._loc += tloc
        elif self._trsf_form in {
            TrsfForm.COMPOUNDTRSF,
            TrsfForm.ROTATION,
            TrsfForm.AX1MIRROR,
        } and other._trsf_form in {
            TrsfForm.SCALE,
            TrsfForm.PNTMIRROR,
        }:
            # print(12)
            self._trsf_form = TrsfForm.COMPOUNDTRSF
            tloc = other.loc.copy()
            tloc = self._matrix @ self._scale
            self._scale *= other._scale
            self._loc += tloc
            self._matrix = other._matrix.copy()
        else:
            # print(13)
            self._trsf_form = TrsfForm.COMPOUNDTRSF
            tloc = other.loc.copy()
            tloc = self._matrix @ tloc

            if self._scale != 1.0:
                tloc *= self._scale
                self._scale *= other._scale
            else:
                self._scale = other._scale
            self._loc += tloc
            self._matrix @= other._matrix

    def __matmul__(self, other: Trsf2D):
        result = self.copy()
        result.multiply(other)
        return result

    def power(self, n: int):
        from itertools import repeat

        if self._trsf_form == TrsfForm.IDENTITY:
            return
        else:
            if n == 0:
                self._scale = 1.0
                self._trsf_form = TrsfForm.IDENTITY
                self._matrix.set_identity()
                self._loc.x = 0.0
                self._loc.y = 0.0
            elif n == 1:
                return
            elif n == -1:
                self.invert()
            else:
                if n < 0:
                    self.invert()
                if self._trsf_form == TrsfForm.TRANSLATION:
                    npower = n
                    if n < 0:
                        npower = -n
                    npower -= 1
                    tmp_loc = self._loc.copy()
                    for _ in repeat(None):
                        if npower % 2 == 1:
                            self._loc += tmp_loc
                        if npower == 1:
                            break
                        tmp_loc += tmp_loc
                        npower //= 2
                elif self._trsf_form == TrsfForm.SCALE:
                    npower = n
                    if n < 0:
                        npower = -n
                    npower -= 1
                    tmp_loc = self._loc.copy()
                    tmp_scale = self._scale
                    for _ in repeat(None):
                        if npower % 2 == 1:
                            self._loc += tmp_loc * self._scale
                            self._scale *= tmp_scale
                        if npower == 1:
                            break
                        tmp_loc += tmp_loc * tmp_scale
                        tmp_scale *= tmp_scale
                        npower //= 2
                elif self._trsf_form == TrsfForm.ROTATION:
                    npower = n
                    if n < 0:
                        npower = -n
                    npower -= 1
                    temp_matrix = self._matrix.copy()
                    if self._loc == Xy(0.0, 0.0):
                        for _ in repeat(None):
                            if npower % 2 == 1:
                                self._matrix @= temp_matrix
                            if npower == 1:
                                break
                            temp_matrix @= temp_matrix
                            npower //= 2
                    else:
                        tmp_loc = self._loc.copy()
                        for _ in repeat(None):
                            if npower % 2 == 1:
                                self._loc += self._matrix @ tmp_loc
                                self._matrix @= temp_matrix
                            if npower == 1:
                                break
                            tmp_loc += temp_matrix @ tmp_loc
                            temp_matrix @= temp_matrix
                            npower //= 2
                elif self._trsf_form in {TrsfForm.PNTMIRROR, TrsfForm.AX1MIRROR}:
                    if n % 2 == 0:
                        self._scale = 1.0
                        self._trsf_form = TrsfForm.IDENTITY
                        self._matrix.set_identity()
                        self._loc.x = 0.0
                        self._loc.y = 0.0
                else:
                    self._trsf_form = TrsfForm.COMPOUNDTRSF
                    npower = n
                    if n < 0:
                        npower = -n
                    npower -= 1
                    self._matrix.set_diagonal(
                        self._scale * self._matrix[0, 0],
                        self._scale * self._matrix[1, 1],
                    )
                    tmp_loc = self._loc.copy()
                    tmp_scale = self._scale
                    tmp_matrix = self._matrix.copy()

                    for _ in repeat(None):
                        if npower % 2 == 1:
                            self._loc += (self._matrix @ tmp_loc) * self._scale
                            self._scale *= tmp_scale
                            self._matrix @= tmp_matrix
                        if npower == 1:
                            break
                        tmp_scale *= tmp_scale
                        tmp_loc += (tmp_matrix @ tmp_loc) * tmp_scale
                        tmp_matrix @= tmp_matrix
                        npower //= 2

    def orthogonalize(self):
        tmp_matrix = self._matrix.copy()
        v1 = Xy(tmp_matrix[0, 0], tmp_matrix[1, 0])
        v2 = Xy(tmp_matrix[0, 1], tmp_matrix[1, 1])

        v1.normalize()
        v2 -= v1 * (v1 @ v2)
        v2.normalize()

        tmp_matrix[0, 0] = v1.x
        tmp_matrix[1, 0] = v1.y
        tmp_matrix[0, 1] = v2.x
        tmp_matrix[1, 1] = v2.y

        v1 = Xy(tmp_matrix[0, 0], tmp_matrix[0, 1])
        v2 = Xy(tmp_matrix[1, 0], tmp_matrix[1, 1])

        v1.normalize()
        v2 -= v1 * (v1 @ v2)
        v2.normalize()

        tmp_matrix[0, 0] = v1.x
        tmp_matrix[0, 1] = v2.x
        tmp_matrix[1, 0] = v1.y
        tmp_matrix[1, 1] = v2.y

        self._matrix = tmp_matrix