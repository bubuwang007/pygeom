import math
from src.primitive import *
from src.math import *

ax = Ax3D(
    loc=Point3D(0.0, 0.0, 0.0),
    dir=Dir3D(0.0, 0.0, 1.0)
)

ax1 = Ax3D(
    loc=Point3D(0.0, 0.0, 0.0),
    dir=Dir3D(0.0, 1.0, 1.0)
)

print(ax.angle(ax1))