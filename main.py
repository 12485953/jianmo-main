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
parser.add_argument('--glass_height', type=list)
parser.add_argument('--widths', type=list)
parser.add_argument('--heights', type=list)
parser.add_argument('--height', type=float, help='海拔高度')

args = parser.parse_args()

vlight = get_vlight(args.D, args.latitude, args.ST)
print('vlight； ', vlight.getnp())

DNI = DNI(args.D, args.latitude, args.ST, args.height)

coordinates = read_coordinates_from_excel()
glasses = create_glasses(coordinates, args.glass_height, vlight, args.heights, args.widths, args.tower_center_land)


cal_valid_area_for_all_glasses(glasses, vlight, args.cos_rs)

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
average_optical_efficiency = cal_average_optical_efficiency(glasses)

E_field = E_field(DNI, glasses)

print('average_optical_efficiency: ', average_optical_efficiency)
print('E_field: ', E_field)



