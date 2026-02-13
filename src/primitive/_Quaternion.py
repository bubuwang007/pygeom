from __future__ import annotations

import sys

from ..config import FLOAT_PRINT_PRECISION
from ._Vec3D import Vec3D


class Quaternion:
    _x: float
    _y: float
    _z: float
    _w: float

    def __init__(
        self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0
    ) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._w = w

    def __str__(self) -> str:
        return f"Quaternion(x={self._x:.{FLOAT_PRINT_PRECISION}f}, y={self._y:.{FLOAT_PRINT_PRECISION}f}, z={self._z:.{FLOAT_PRINT_PRECISION}f}, w={self._w:.{FLOAT_PRINT_PRECISION}f})"

    def copy(self) -> Quaternion:
        return Quaternion(self._x, self._y, self._z, self._w)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z

    @property
    def square_norm(self) -> float:
        return self._x**2 + self._y**2 + self._z**2 + self._w**2

    @property
    def norm(self) -> float:
        return self.square_norm**0.5

    def stabilize_length(self) -> float:
        cs = abs(self._x) + abs(self._y) + abs(self._z) + abs(self._w)
        if cs > 0.0:
            self._x /= cs
            self._y /= cs
            self._z /= cs
            self._w /= cs
        else:
            self.set_identity()

    @staticmethod
    def from_vecfromto(vec_from: Vec3D, vec_to: Vec3D) -> Quaternion:
        pass

    def normalize(self):
        magn = self.norm
        if magn < sys.float_info.epsilon:
            self.stabilize_length()
            magn = self.norm
        self.scale(1.0 / magn)

    def reverse(self):
        self._x = -self._x
        self._y = -self._y
        self._z = -self._z

    def invert(self):
        inv = 1.0 / self.square_norm
        self.set(-self._x * inv, -self._y * inv, -self._z * inv, self._w * inv)

    def set(self, x: float, y: float, z: float, w: float) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._w = w

    def set_by_quaternion(self, other: Quaternion) -> None:
        self._x = other._x
        self._y = other._y
        self._z = other._z
        self._w = other._w

    def scale(self, factor: float) -> None:
        self._x *= factor
        self._y *= factor
        self._z *= factor
        self._w *= factor

    def set_identity(self) -> None:
        self.set(0.0, 0.0, 0.0, 1.0)

    def set_rotation(self, vec_from: Vec3D, vec_to: Vec3D):
        vec_cross = vec_from.copy().cross(vec_to)
        self.set(vec_cross.x, vec_cross.y, vec_cross.z, vec_from @ vec_to)
        self.normalize()

    def set_rotation_with_ref(self):
        pass

    def __neg__(self, q: Quaternion) -> Quaternion:
        return Quaternion(-q._x, -q._y, -q._z, -q._w)
