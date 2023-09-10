from utils import *
from shadow_calculation import *
import argparse
from reflect_calculation import *
import shapely

parser = argparse.ArgumentParser(description='Parameters that can be changed in this experiment')
parser.add_argument('--tower_center_land', type=point, default=point(0, 0, 84))
parser.add_argument('--tower_height', type=float, default=8)
parser.add_argument('--tower_r', type=float, default=3.5)
parser.add_argument('--divide_num', type=int, default=100)
parser.add_argument('--D', type=int, default=-28)
parser.add_argument('--latitude', type=float, default=math.pi * 39.45 / 180)
parser.add_argument('--ST', type=float, default=10.5, help='当地时间')
parser.add_argument('--glass_height', type=list, default=[])
parser.add_argument('--widths', type=list, default=[])
parser.add_argument('--heights', type=list, default=[])
parser.add_argument('--height', type=float, default=3, help='海拔高度（单位：km）')

args = parser.parse_args()



vlight, cos_rs = get_vlight(args.D, args.latitude, args.ST)
print('vlight； ', vlight.getnp())

DNI = DNI(args.D, args.latitude, args.ST, args.height)

coordinates = read_coordinates_from_excel()
for i in range(len(coordinates)):
    args.glass_height.append(4)
    args.widths.append(6)
    args.heights.append(6)

glasses = create_glasses(coordinates, args.glass_height, vlight, args.heights, args.widths, args.tower_center_land)

print('--------------- glasses set -------------------')


cal_valid_area_for_all_glasses(glasses, vlight, cos_rs)

print('---------------------- shadow calculation step 1 finish ---------------------------')

cal_valid_reflect_area_for_all_glasses(glasses, args.tower_center_land, args.tower_height, args.tower_r, args.divide_num)

print('---------------------- shadow calculation step 2 finish ---------------------------')
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

cal_optical_efficiency_for_all_glasses(glasses, args.tower_center_land)
average_optical_efficiency = cal_average_optical_efficiency(glasses)

E_field = E_field(DNI, glasses)

print('average_optical_efficiency: ', average_optical_efficiency)
print('E_field: ', E_field)



