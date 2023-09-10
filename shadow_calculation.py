import math

import shapely
import numpy as np
from shapely.geometry import Polygon
from utils import *

def is_front(glass1, glass2, cos_rs):
    direction = np.array([-math.sqrt(1-math.pow(cos_rs, 2)), -cos_rs])
    vector = glass1.center_land.getnp() - glass2.center_land.getnp()
    vector = vector[:2]
    cos_value = np.dot(direction, vector)
    if cos_value > 0:
        return False
    return True







def cal_shadow_on_surface(glass, obstacle, vlight, cos_rs):
    obstacle_vertex_in_obstacle = [np.array([obstacle.width / 2, obstacle.height / 2, 0]), np.array([-obstacle.width / 2, obstacle.height / 2, 0]), np.array([-obstacle.width / 2, -obstacle.height / 2, 0]), np.array([obstacle.width / 2, -obstacle.height / 2, 0])]
    obstacle_vertex_in_land = [apply_transform_for_point(i, obstacle.transform_to_land) for i in obstacle_vertex_in_obstacle]

    obstacle_vertex_in_glass = [apply_transform_for_point(i, glass.transform_from_land) for i in obstacle_vertex_in_land]

    if is_front(obstacle, glass, cos_rs):
        vlight_in_glass = apply_transform_for_vector(vlight.getnp(), glass.transform_from_land)
        shadow_vertex_on_glass_in_glass = []
        for obstacle_vertex in obstacle_vertex_in_glass:
            k = obstacle_vertex[2] / vlight_in_glass[2]
            y = obstacle_vertex[1] - k * vlight_in_glass[1]
            x = obstacle_vertex[0] - k * vlight_in_glass[0]
            shadow_vertex_on_glass_in_glass.append(np.array([x, y, 0]))

        shadow_polygon_vertex_2d = [(shadow_vertex[0], shadow_vertex[1]) for shadow_vertex in shadow_vertex_on_glass_in_glass]
        shadow_polygon = Polygon(shadow_polygon_vertex_2d)


        glass_valid_polygon = []
        for glass_polygon_piece in glass.valid_polygon:
            glass_polygon_piece_own = glass_polygon_piece.difference(shadow_polygon)
            if isinstance(glass_polygon_piece_own, shapely.geometry.base.GeometrySequence):
                geoms = glass_polygon_piece_own.geoms
                for geom in geoms:
                    glass_valid_polygon.append(geom)
            else:
                if not glass_polygon_piece_own.is_empty:
                    glass_valid_polygon.append(glass_polygon_piece_own)

        glass.valid_polygon = glass_valid_polygon

        vreflect_in_glass = apply_transform_for_vector(glass.vreflict.getnp(), glass.transform_from_land)
        shadow_vertex_on_glass_in_glass = []
        for obstacle_vertex in obstacle_vertex_in_glass:
            k = obstacle_vertex[2] / vreflect_in_glass[2]
            y = obstacle_vertex[1] - k * vreflect_in_glass[1]
            x = obstacle_vertex[0] - k * vreflect_in_glass[0]
            shadow_vertex_on_glass_in_glass.append(np.array([x, y, 0]))

        shadow_polygon_vertex_2d = [(shadow_vertex[0], shadow_vertex[1]) for shadow_vertex in
                                    shadow_vertex_on_glass_in_glass]
        shadow_polygon = Polygon(shadow_polygon_vertex_2d)


        glass_valid_polygon = []
        for glass_polygon_piece in glass.valid_polygon:
            glass_polygon_piece_own = glass_polygon_piece.difference(shadow_polygon)
            if isinstance(glass_polygon_piece_own, shapely.geometry.base.GeometrySequence):
                geoms = glass_polygon_piece_own.geoms
                for geom in geoms:
                    glass_valid_polygon.append(geom)
            else:
                glass_valid_polygon.append(glass_polygon_piece_own)

        glass.valid_polygon = glass_valid_polygon





def cal_valid_area_in_one_glass(glasses, index, vlight, cos_rs):
    #print('----------------- new glass -----------------------')
    glass = glasses[index]
    for i, obstacle in enumerate(glasses):
        if i == index:
            continue
        cal_shadow_on_surface(glass, obstacle, vlight, cos_rs)


def cal_valid_area_for_all_glasses(glasses, vlight, cos_rs):
    for i in range(len(glasses)):
        cal_valid_area_in_one_glass(glasses, i, vlight, cos_rs)
    for glass in glasses:
        valid_area_to_reflect = 0
        if not glass.valid_polygon:
            valid_area_to_reflect = 0
        else:
            for polygon in glass.valid_polygon:
                valid_area_to_reflect += polygon.area
        glass.valid_area_to_reflect = valid_area_to_reflect



