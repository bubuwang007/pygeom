import math
from src.primitive import *
from src.math import *

trsf = Trsf2D()
trsf._matrix = Matrix2D([[10, 1], [2, 5]])

trsf.orthogonalize()

print(trsf.matrix)