import matplotlib.pyplot as plt
import numpy as np

def plot_scatter_with_labels(points_list):
    """
    绘制散点图，并在每个点旁标出数字

    参数:
    points_list (list): 包含点坐标的列表，每个元素是一个NumPy数组，数组包含一个点的坐标，第一个元素是X坐标，第二个元素是Y坐标。
    """
    # 初始化空的NumPy数组来存储所有点的坐标
    all_points = np.array(points_list)

    # 分离X坐标和Y坐标
    x_values = all_points[:, 0]
    y_values = all_points[:, 1]

    # 使用Matplotlib创建散点图
    plt.scatter(x_values, y_values, label='Data Points', color='blue', marker='o')

    # 添加数字标签
    for i, point in enumerate(points_list):
        x, y, _ = point
        plt.annotate(f'{i + 1}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 添加标题和标签
    plt.title('Scatter Plot of Data Points with Labels')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.show()

import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def plot_polygon(shapely_polygon, color='blue'):
    """
    绘制Shapely中的Polygon对象

    参数:
    shapely_polygon (shapely.geometry.Polygon): 要绘制的Polygon对象。
    """
    # 提取多边形的坐标
    x, y = shapely_polygon.exterior.xy

    # 使用Matplotlib绘制多边形
    #plt.figure()
    plt.plot(x, y, color=color)
    plt.fill(x, y, alpha=0.2, color=color)
    plt.title('Polygon with Shapely')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid()
    #plt.show()




# 示例用法
# data_points_list = [np.array([ 3.45818118, -4.2590126 ,  0.        ]), np.array([ 3.47190701, -4.31229854,  0.        ]), np.array([ 3.43873917, -5.55197178,  0.        ]), np.array([ 3.06896358, -6.7193626 ,  0.        ]), np.array([ 2.39877645, -7.70019866,  0.        ]), np.array([ 1.49378036, -8.39846889,  0.        ]), np.array([ 0.44256265, -8.74582174,  0.        ]), np.array([-0.65197617, -8.70825588,  0.        ]), np.array([-1.68269503, -8.28944853,  0.        ]), np.array([-2.54869997, -7.53039547,  0.        ]), np.array([-2.54869997, -6.96409613,  0.        ]), np.array([-1.68269503, -7.72314919,  0.        ]), np.array([-0.65197617, -8.14195654,  0.        ]), np.array([ 0.44256265, -8.1795224 ,  0.        ]), np.array([ 1.49378036, -7.83216955,  0.        ]), np.array([ 2.39877645, -7.13389932,  0.        ]), np.array([ 3.06896358, -6.15306326,  0.        ]), np.array([ 3.43873917, -4.98567243,  0.        ])]
# plot_scatter_with_labels(data_points_list)

