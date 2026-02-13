import math
from src.primitive import *
from src.math import *

q = Quaternion(1.0, 2.0, 3.0, 4.0)

q.normalize()
print(q)
