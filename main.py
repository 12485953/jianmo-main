from utils import *
from mirror import *
from shadow_calculation import *
import argparse
from reflect_calculation import *

parser = argparse.ArgumentParser(description='Parameters that can be changed in this experiment')
parser.add_argument('--tower_center_land', type=point, default=point(0, 0, 84))
parser.add_argument('--tower_height', type=float, default=8)
parser.add_argument('--tower_r', type=float, default=3.5)
parser.add_argument('--divide_num', type=int, default=100)
parser.add_argument('--D', type=int, default=100)
parser.add_argument('--latitude', type=float, default=100)
parser.add_argument('--ST', type=float, default=100)

args = parser.parse_args()

vlight = get_vlight(args.D, args.latitude, args.ST)
print('vlight； ', vlight.getnp())

coordinates = read_coordinates_from_excel()

# center1 = point(0, 1, 4)
# glass1 = Glass(center1, vlight, 6, 6, args.tower_center_land)
#
# center2 = point(0, 1.5, 4)
# glass2 = Glass(center2, vlight, 6, 6, args.tower_center_land)
#
# glasses = [glass1, glass2]



cal_valid_area_for_all_glasses(glasses, vlight, args.cos_rs)

# for polygon in glass1.valid_polygon:
#     for coord in polygon.exterior.coords:
#         print(coord)
#     print('----------------------')
#
# print('---------------------------------------------------------')
#
# for polygon in glass2.valid_polygon:
#     for coord in polygon.exterior.coords:
#         print(coord)
#     print('----------------------')

cal_valid_reflect_area_for_all_glasses(glasses, args.tower_center, args.tower_height, args.tower_r, args.divide_num)


# for polygon in glass1.valid_polygon:
#     for coord in polygon.exterior.coords:
#         print(coord)
#     print('----------------------')
#
# print('---------------------------------------------------------')
#
# for polygon in glass2.valid_polygon:
#     for coord in polygon.exterior.coords:
#         print(coord)
#     print('----------------------')

cal_optical_efficiency_for_all_glasses(glasses)

