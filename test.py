from src.primitive import *
from src.math import *

# trsf = Trsf2D()
# trsf.set_rotation(Point2D(0.0, 0.0), 90/180*3.1415926)
# trsf = trsf @ trsf @ trsf
# # trsf.set_scale(Point2D(0.0, 0.0), 0.1)
# # trsf.set_translation_by_2point(Point2D(0, 0), Point2D(10, 10))

# point = Point2D(1, 0)

# point.transform(trsf)

# print(point)
# trsf.invert()

# point.transform(trsf)

# print(point)

### Ax2d coaxial test

# ax2d_1 = Ax2d(Point2D(10, 11), Dir2d(0, 1))
# ax2d_2 = Ax2d(Point2D(10, 5), Dir2d(0, 1))

# print(ax2d_1.is_coaxial_to(ax2d_2))

###

j = Jocobi(MathMatrix([[5, 1, 0], [1, 3, 0], [0, 0, 4]]))
print(j.eigen_values)
print(j.eigen_vectors)
