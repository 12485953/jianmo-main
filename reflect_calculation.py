import math

from utils import *
from shadow_calculation import *
import shapely
from shapely.geometry import LineString
from plot import *

def find_valid_cylinder_for_a_glass(glass, tower_center, tower_height, tower_r, divide_num):
    vreflect_land = glass.vreflict.getnp()
    vreflect_land_z = np.dot(vreflect_land, np.array([0, 0, 1]))
    vreflect_shadow = vreflect_land - vreflect_land_z

    if vreflect_shadow[1] == 0:
        start_vector = np.array([0, 1, 0])
    else:
        start_vector = np.array([1, -vreflect_shadow[0] / vreflect_shadow[1], 0])
        length = math.sqrt(math.pow(start_vector[0], 2) + math.pow(start_vector[1], 2) + math.pow(start_vector[2], 2))
        start_vector = start_vector / length

    cos_value = np.dot(start_vector, np.array([0, 1, 0]))
    start_angle = math.acos(cos_value)

    divide_num = divide_num
    delta_angle = math.pi / divide_num
    current_angle = start_angle + delta_angle
    current_vector = np.array([math.sin(current_angle), math.cos(current_angle), 0])
    current_vector = standardize(current_vector)
    cos_with_reflect = np.dot(current_vector, standardize(vreflect_land))

    points = []
    if cos_with_reflect < 0:
        for i in range(divide_num + 1):
            current_angle = start_angle + delta_angle * i
            current_vector = np.array([math.sin(current_angle), math.cos(current_angle), 0])
            current_vector = standardize(current_vector)
            current_point = tower_r * current_vector + tower_center.getnp() + np.array([0, 0, tower_height / 2])
            points.append(current_point)
    else:
        for i in range(divide_num + 1):
            current_angle = start_angle - delta_angle * i
            current_vector = np.array([math.sin(current_angle), math.cos(current_angle), 0])
            current_vector = standardize(current_vector)
            current_point = tower_r * current_vector + tower_center.getnp() + np.array([0, 0, tower_height / 2])
            points.append(current_point)

    points_len = len(points)
    for i in range(len(points)):
        index = points_len - i - 1
        points.append(points[index] - np.array([0, 0, tower_height]))

    points_in_glass = [apply_transform_for_point(i, glass.transform_from_land) for i in points]
    vreflect_in_glass = apply_transform_for_vector(glass.vreflict.getnp(), glass.transform_from_land)
    shadow_vertex_on_glass_in_glass = []
    for point in points_in_glass:
        k = point[2] / vreflect_in_glass[2]
        y = point[1] - k * vreflect_in_glass[1]
        x = point[0] - k * vreflect_in_glass[0]
        shadow_vertex_on_glass_in_glass.append(np.array([x, y, 0]))

    return shadow_vertex_on_glass_in_glass

def divide_points(points):
    points.append(points[0])
    line_set = []
    point_set = []
    intersection_point_index = []
    line_set.append(LineString([points[0], points[1]]))
    point_set.append(points[0])
    point_set.append(points[1])
    intersection_count = 0
    intersection_points = []
    for i in range(1, len(points)-1):
        current_line = LineString([points[i], points[i+1]])

        for j in range(len(line_set)-1):
            if i == len(points) - 2 and j == 0:
                continue
            if current_line.intersects(line_set[j]):
                intersection = current_line.intersection(line_set[j])
                if intersection.geom_type == 'Point':
                    intersection_count += 1
                    intersection_point = np.array([intersection.x, intersection.y, 0])
                    intersection_points.append(intersection_point)
                    point_set.insert(j + 1, intersection_point)
                    point_set.append(intersection_point)


        point_set.append(points[i+1])
        line_set.append(current_line)
    for index, point in enumerate(point_set):
        isIntersection = False
        for intersection_point in intersection_points:
            if np.array_equal(point, intersection_point):
                isIntersection = True
        if isIntersection:
            intersection_point_index.append(index)

    # print(point_set)
    # print(intersection_point_index)

    subsets = []
    if intersection_count == 1:
        subset1 = []
        subset2 = []
        subset1 += point_set[:intersection_point_index[0]+1]
        subset2 += point_set[intersection_point_index[0]:intersection_point_index[1]]
        subset1 += point_set[intersection_point_index[1]+1:len(point_set)-1]
        subsets.append(subset1)
        subsets.append(subset2)
    elif intersection_count == 2:
        subset1 = []
        subset2 = []
        subset3 = []
        subset1 += point_set[:intersection_point_index[0]]
        subset2 += point_set[intersection_point_index[0]:intersection_point_index[1]]
        subset3 += point_set[intersection_point_index[1]:intersection_point_index[2]]
        subset2 += point_set[intersection_point_index[2]:intersection_point_index[3]]
        subset1 += point_set[intersection_point_index[3]:len(point_set)-1]
        subsets.append(subset1)
        subsets.append(subset2)
        subsets.append(subset3)


    return subsets


def cal_valid_area_for_a_glass(subsets, glass, vreflect):
    #print('------------- new glass --------------------')
    for subset in subsets:
        cal_valid_area_for_a_subset(subset, glass, vreflect)


def cal_valid_area_for_a_subset(points, glass, vreflect):
    #print('------------- new shadow subset --------------------')
    shadow_polygon_vertex_2d = [(shadow_vertex[0], shadow_vertex[1]) for shadow_vertex in
                                points]
    shadow_polygon = Polygon(shadow_polygon_vertex_2d)
    #plot_polygon(shadow_polygon, 'black')

    glass_valid_polygon = []
    for glass_polygon_piece in glass.valid_polygon:

        #plot_polygon(glass_polygon_piece)
        glass_polygon_piece_own = glass_polygon_piece.intersection(shadow_polygon)
        if isinstance(glass_polygon_piece_own, shapely.geometry.base.GeometrySequence):
            geoms = glass_polygon_piece_own.geoms
            for geom in geoms:
                glass_valid_polygon.append(geom)
        else:
            if not glass_polygon_piece_own.is_empty:
                glass_valid_polygon.append(glass_polygon_piece_own)

    glass.valid_polygon = glass_valid_polygon
    plt.show()
def cal_valid_reflect_area_for_all_glasses(glasses, tower_center, tower_height, tower_r, divide_num):
    for glass in glasses:
        shadow_vertex_on_glass_in_glass = find_valid_cylinder_for_a_glass(glass, tower_center, tower_height, tower_r, divide_num)
        #plot_scatter_with_labels(shadow_vertex_on_glass_in_glass)
        subsets = divide_points(shadow_vertex_on_glass_in_glass)

        cal_valid_area_for_a_glass(subsets, glass, glass.vreflict)

    for glass in glasses:
        valid_area_to_absorb = 0
        if not glass.valid_polygon:
            valid_area_to_absorb = 0
        else:
            for polygon in glass.valid_polygon:
                valid_area_to_absorb += polygon.area
        glass.valid_area_to_absorb = valid_area_to_absorb




