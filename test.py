import math
from shapely.geometry import Polygon
from reflect_calculation import divide_points

polygon = Polygon([(0, 2), (2, 2), (0, 0), (2, 0)])
print(polygon.is_empty)
# print(type(polygon))
#
# for coord in polygon.exterior.coords:
#     print(coord)

# subsets = divide_points([(0, 0), (0.5, 1), (1, 0), (1, 1)])

# subsets = divide_points([(-1, 2), (0, 0), (1, 2), (1, 1), (0, 0.5), (-1, 1)])
#
# for subset in subsets:
#     print(subset)