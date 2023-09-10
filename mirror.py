import math

import numpy as np

from utils import *
from shapely.geometry import Polygon


class Glass:
    def __init__(self, center, vlight, height, width, tower_center_land):
        self.width = width
        self.height = height
        self.center_land = center
        self.vlight = vlight
        self.vreflict = point(tower_center_land.x - center.x, tower_center_land.y - center.y, tower_center_land.z - center.z)
        total = math.sqrt(math.pow(self.vreflict.x, 2) + math.pow(self.vreflict.y, 2) + math.pow(self.vreflict.z, 2))
        self.vreflict.x = self.vreflict.x / total
        self.vreflict.y = self.vreflict.y / total
        self.vreflict.z = self.vreflict.z / total
        self.coord_z_land = self.norm(vlight)
        self.coord_x_land = self.coord_x()
        self.coord_y_land = self.coord_y()
        self.valid_polygon = list()
        poly = Polygon([(width / 2, height / 2), (-width / 2, height / 2), (-width / 2, -height / 2), (width / 2, -height / 2)])
        self.valid_polygon = [poly]
        self.transform_to_land = np.column_stack([self.coord_x_land.getnp(), self.coord_y_land.getnp(), self.coord_z_land.getnp(), self.center_land.getnp()])
        self.transform_to_land = np.row_stack([self.transform_to_land, np.array([0, 0, 0, 1])])
        self.transform_from_land = np.linalg.inv(self.transform_to_land)
        self.valid_area_to_reflect = poly.area
        self.valid_area_to_absorb = 1
        self.optical_efficiency = 0

    def norm(self, vlight):
        fir = point(self.center_land.x + self.vreflict.x, self.center_land.y + self.vreflict.y, self.center_land.z + self.vreflict.z)
        sec = point(self.center_land.x + vlight.x, self.center_land.y + vlight.y, self.center_land.z + vlight.z)
        mid = point((fir.x + sec.x) / 2, (fir.y + sec.y) / 2, (fir.z + sec.z) / 2)
        res = point(mid.x - self.center_land.x, mid.y - self.center_land.y, mid.z - self.center_land.z)
        len = math.sqrt(math.pow(res.x, 2) + math.pow(res.y, 2) + math.pow(res.z, 2))
        res.x = res.x / len
        res.y = res.y / len
        res.z = res.z / len
        return res

    def coord_x(self):
        len = math.sqrt(1 + math.pow(self.coord_z_land.x / self.coord_z_land.y, 2))
        cx = point(1 / len, -self.coord_z_land.x / self.coord_z_land.y, 0)
        return cx

    def coord_y(self):
        y = np.cross(self.coord_x_land.getnp(), self.coord_z_land.getnp())
        length = math.sqrt(math.pow(y[0], 2) + math.pow(y[1], 2) + math.pow(y[2], 2))
        y = y / length
        return point(y[0], y[1], y[2])
        # x = 1
        # y = -self.coord_x_land.x / self.coord_x_land.y
        # z = (-y - self.coord_z_land.x) / self.coord_z_land.z
        # re = point(x, y, z)
        # len = re.getlen()
        # re.x = re.x / len
        # re.y = re.y / len
        # re.z = re.z / len
        # return re



