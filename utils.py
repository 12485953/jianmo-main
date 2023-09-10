import shapely
import math
import numpy as np
from mirror import Glass

def length(vector):
    return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2) + math.pow(vector[2], 2))

def standardize(vector):
    return vector / length(vector)

def apply_transform_for_point(point, transform_matrix):

    point = np.array([point[0], point[1], point[2], 1])
    point_trans = np.dot(transform_matrix, point)
    result = np.array([point_trans[0], point_trans[1], point_trans[2]])
    return result

def apply_transform_for_vector(vector, transform_matrix):
    trans = transform_matrix[:3, :3]

    return np.dot(trans, vector)

class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getnp(self):
        return np.array([self.x, self.y, self.z])

    def getlen(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
def sin_sun_elevation_angle(D: float, latitude: float, ST: float) -> float:
    """
    计算太阳高度角的正弦值
    :param D: 以3月21日为0起算的天数
    :param latitude: 纬度
    :param ST: 当地时间
    :return: 太阳高度角的正弦值
    """
    return (1 - math.pow(sin_sun_declination_angle(D), 2)) * 0.5 * math.cos(latitude) * math.cos(sun_time_angle(ST)) + sin_sun_declination_angle(D) * math.sin(latitude)


def sin_sun_declination_angle(D: float) -> float:
    """
    计算太阳赤纬角的正弦值
    :param D: 以3月21日为0起算的天数
    :return: 太阳赤纬角的正弦值
    """
    return math.sin(2 * math.pi * D / 365) * math.sin(2 * math.pi * 23.45 / 360)

def sun_time_angle(ST: float) -> float:
    """
    计算太阳时角
    :param ST: 当地时间
    :return: 太阳时角
    """
    return math.pi / 12 * (ST - 12)

def cos_sun_fangwei_angle(sin_sun_declination_angle, sin_sun_elevation_angle, latitute):
    return (sin_sun_declination_angle - sin_sun_elevation_angle * math.sin(latitute)) / ((math.sqrt(1 - math.pow(sin_sun_elevation_angle),2)) * math.cos(latitute))


def DNI(D: float, latitude: float, ST: float, height: float) -> float:
    """
    计算直接Normal Irradiance（直接垂直辐射）
    :param D: 以3月21日为0起算的天数
    :param latitude: 纬度
    :param ST: 当地时间
    :param height: 观测地点海拔高度（单位：千米）
    :return: 直接垂直辐射
    """
    H = height * 1000
    G0 = 1.366
    sin_sun_elevation = sin_sun_elevation_angle(D, latitude, ST)
    a = 0.4237 - .00821 * math.pow((6 - H), 2)
    b = 0.5055 + .00595 * math.pow((6.5 - H), 2)
    c = 0.2711 + .01868 * math.pow((2.5 - H), 2)
    return G0 * (a + b * math.exp(-c / sin_sun_elevation))


def atmospheric_transmissivity(dhr: float) -> float:
    """
    计算大气透射率
    :param dhr: 相对湿度（%）
    :return: 大气透射率
    """
    return 0.99321 - 0.0001176 * dhr + 1.97 * math.pow(10, -8) * math.pow(dhr, 2)

def vlight(sin_alphas, cos_rs):
    x = math.sqrt(1 - math.pow(sin_alphas, 2)) * math.sqrt(1 - math.pow(cos_rs, 2))
    y = math.sqrt(1 - math.pow(sin_alphas, 2)) * cos_rs
    z = sin_alphas
    len = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
    x = x / len
    y = y / len
    z = z / len
    return point(x, y, z)

def get_vlight(D, latitude, ST):
    sin_sun_declination_angle_value = sin_sun_declination_angle(D)
    sin_alphas = sin_sun_elevation_angle(D, latitude, ST)
    cos_rs = cos_sun_fangwei_angle(sin_sun_declination_angle_value, sin_alphas, latitude)
    return vlight(sin_alphas, cos_rs)

def yita_sb(glass):
    valid_area = 0
    if not glass.valid_polygon:
        valid_area = 0
    else:
        for polygon in glass.valid_polygon:
            valid_area += polygon.area


def optical_efficiency(yita_sb, yita_cos, yita_at, yita_trunc):
    return yita_at * yita_trunc * yita_cos * yita_sb * 0.92

def yita_at(center_land:point, tower_center_land:point):
    distance = math.sqrt(math.pow(center_land.x - tower_center_land.x, 2) + math.pow(center_land.y - tower_center_land.y, 2) + math.pow(center_land.z - tower_center_land.z, 2))
    return 0.99321 - 0.0001176 * distance + math.pow(10, -8) * 1.97 * math.pow(distance, 2)

def yita_trunc(glass: Glass):
    return glass.valid_area_to_absorb / glass.valid_area_to_reflect

def yita_cos(vlight:point, norm:point):
    return math.abs((vlight.x * norm.x + vlight.y * norm.y + vlight.z * norm.z) / (vlight.getlen() * norm.getlen()), 2)

def cal_optical_efficiency_for_a_glass(glass, tower_center_land):
    yita_sb_value = yita_sb(glass)
    yita_cos_value = yita_cos(glass.vlight, glass.norm)
    yita_at_value = yita_at(glass.center_land, tower_center_land)
    yita_trunc_value = yita_trunc(glass)
    return optical_efficiency(yita_sb_value, yita_cos_value, yita_at_value, yita_trunc_value)
def cal_optical_efficiency_for_all_glasses(glasses, tower_center_land):
    for glass in glasses:
        optical_eff = cal_optical_efficiency_for_a_glass(glass, tower_center_land)
        glass.optical_efficiency = optical_eff
def E_field(DNI, glasses:list(Glass)):
    toatl = 0
    for glass in glasses:
       area = glass.width * glass.height
       toatl += area * glass.yita

    toatl = toatl * DNI
    return toatl

import openpyxl

def read_coordinates_from_excel(file_path='supplement.xlsx', sheet_name="Sheet1"):
    """
    从Excel文件中读取坐标点信息。

    参数:
    file_path (str): Excel文件的路径。
    sheet_name (str): 要读取数据的工作表名称。

    返回:
    list: 包含坐标点信息的列表，每个元素是一个包含x和y坐标的元组。
    """
    coordinates = []

    try:
        # 打开Excel文件
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]

        # 从Excel中读取坐标点信息
        for row in sheet.iter_rows(values_only=True):
            if len(row) >= 2:  # 确保至少有两列数据
                x, y = row[0], row[1]
                coordinates.append((x, y))

        return coordinates

    except Exception as e:
        print(f"读取Excel文件时发生错误：{str(e)}")
        return None


def create_glasses(coordinates, glass_height, vlight, heights, widths, tower_center_land):
    glasses = []
    for index, coordinate in enumerate(coordinates):
        glass = Glass(point(coordinate[0], coordinate[1], glass_height[index]), vlight, heights[index], widths[index], tower_center_land)
        glasses.append(glass)

    return glasses

