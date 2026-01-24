import sys
from ._MathVector import MathVector
from ._MathMatrix import MathMatrix


class Jocobi:
    _matrix: MathMatrix
    _done: bool
    _nb_rotations: int
    _eigen_values: MathVector
    _eigen_vectors: MathMatrix
    _error: float

    def __init__(self, matrix: MathMatrix) -> None:
        if not matrix.is_square:
            raise ValueError("Input matrix must be square")
        if not matrix.is_symmetric:
            raise ValueError("Input matrix must be symmetric")
        self._matrix = matrix.copy()
        self._done = False
        self._nb_rotations = 0
        self._eigen_values = MathVector.zeros(matrix.shape[0])
        self._eigen_vectors = MathMatrix.identity(matrix.shape[0])
        self._error = self.solve()

    @property
    def eigen_values(self) -> MathVector:
        if not self._done:
            raise RuntimeError("Eigenvalues have not been computed yet")
        return self._eigen_values

    @property
    def eigen_vectors(self) -> MathMatrix:
        if not self._done:
            raise RuntimeError("Eigenvectors have not been computed yet")
        return self._eigen_vectors

    def solve(self):
        n = self._matrix.shape[0]

        b = MathVector.zeros(n)
        z = MathVector.zeros(n)

        for i in range(n):
            b[i] = self._matrix[i, i]
            self._eigen_values[i] = self._matrix[i, i]

        self._nb_rotations = 0

        tresh = 0.0

        for i in range(50):
            sm = 0.0
            for j in range(n):
                for k in range(j + 1, n):
                    sm += abs(self._matrix[j, k])
            if sm < sys.float_info.epsilon:
                self._done = True
                self.eigen_sort()
                return 0

            if i < 4:
                tresh = (0.2 * sm) / (n * n)
            else:
                tresh = 0.0

            for j in range(n):
                for k in range(j + 1, n):
                    g = 100.0 * abs(self._matrix[j, k])
                    if i > 4 and (
                        abs(self._eigen_values[j]) + g == abs(self._eigen_values[j])
                        and abs(self._eigen_values[k]) + g == abs(self._eigen_values[k])
                    ):
                        self._matrix[j, k] = 0.0
                    elif abs(self._matrix[j, k]) > tresh:
                        h = self._eigen_values[k] - self._eigen_values[j]
                        if abs(h) + g == abs(h):
                            t = self._matrix[j, k] / h
                        else:
                            theta = 0.5 * h / self._matrix[j, k]
                            t = 1.0 / (abs(theta) + (1.0 + theta * theta) ** 0.5)
                            if theta < 0.0:
                                t = -t
                        c = 1.0 / (1.0 + t * t) ** 0.5
                        s = t * c
                        tau = s / (1.0 + c)
                        h = t * self._matrix[j, k]
                        z[j] -= h
                        z[k] += h
                        self._eigen_values[j] -= h
                        self._eigen_values[k] += h
                        self._matrix[j, k] = 0.0

                        for l in range(j):
                            self.rotate(l, j, l, k, s, tau)
                        for l in range(j + 1, k):
                            self.rotate(j, l, l, k, s, tau)
                        for l in range(k + 1, n):
                            self.rotate(j, l, k, l, s, tau)

                        for l in range(n):
                            g = self._eigen_vectors[l, j]
                            h = self._eigen_vectors[l, k]
                            self._eigen_vectors[l, j] = g - s * (h + g * tau)
                            self._eigen_vectors[l, k] = h + s * (g - h * tau)

                        self._nb_rotations += 1

            for j in range(n):
                b[j] += z[j]
                self._eigen_values[j] = b[j]
                z[j] = 0.0

        self.eigen_sort()
        raise -1

    def eigen_sort(self):
        n = len(self._eigen_values)

        for i in range(n):
            p = self._eigen_values[i]
            k = i
            for j in range(i + 1, n):
                if self._eigen_values[j] < p:
                    p = self._eigen_values[j]
                    k = j
            if k != i:
                self._eigen_values[i], self._eigen_values[k] = (
                    self._eigen_values[k],
                    self._eigen_values[i],
                )
                for j in range(n):
                    self._eigen_vectors[j, i], self._eigen_vectors[j, k] = (
                        self._eigen_vectors[j, k],
                        self._eigen_vectors[j, i],
                    )

    def rotate(self, i, j, k, l, s, tau):
        g = self._matrix[i, j]
        h = self._matrix[k, l]

        self._matrix[i, j] = g - s * (h + g * tau)
        self._matrix[k, l] = h + s * (g - h * tau)
