import math
from src.primitive import *
from src.math import *

eli = Elips2D(
    pos=Ax22D(
        Point2D(0.0, 0.0),
        Dir2D(1.0, 0.0),
        Dir2D(0.0, 1.0),
    ),
    major_radius=5.0,
    minor_radius=3.0,
)

eli.scale(Point2D(1.0, 1.0), 1.0)

print(eli.focal)
