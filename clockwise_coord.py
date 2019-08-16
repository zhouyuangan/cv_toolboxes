"""
code for checking if a polygon is cockwise or counter-clockwise
There are two versions:
is_clockwise_convex only works for convex polygons -- but is faster,
it only needs to check three points.
is_clockwise checks all points, but works for convex and cocave
  (note: that's the same as the area calculation)
from:
http://paulbourke.net/geometry/clockwise/
"""

from functools import reduce
import operator
import math
import numpy as np


def is_clockwise(poly):
    """
    returns True if the polygon is clockwise ordered, false if not
    expects a sequence of tuples, or something like it (Nx2 array for instance),
    of the points:
    [ (x1, y1), (x2, y2), (x3, y3), ...(xi, yi) ]
    See: http://paulbourke.net/geometry/clockwise/
    """

    total = poly[-1][0] * poly[0][1] - poly[0][0] * poly[-1][1]  # last point to first point
    for i in range(len(poly) - 1):
        total += poly[i][0] * poly[i + 1][1] - poly[i + 1][0] * poly[i][1]

    if total <= 0:
        return True
    else:
        return False


def is_clockwise_convex(poly):
    """
    returns True if the polygon is clockwise ordered, false if not
    expects a sequence of tuples, or something like it, of the points:
    [ (x1, y1), (x2, y2), (x3, y3), ...(xi, yi) ]
    This only works for concave polygons. See:
    http://paulbourke.net/geometry/clockwise/
    """

    x0 = poly[0][0]
    y0 = poly[0][1]
    x1 = poly[1][0]
    y1 = poly[1][1]
    x2 = poly[2][0]
    y2 = poly[2][1]

    cp = (x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)
    if cp <= 0:
        return True
    else:
        return False


def validate_clockwise(coord: np.array):
    """
    return:
        True: clockwise
        False: counter-clockwise
    example:

    point[0] = (5,0)   edge[0]: (6-5)(4+0) =   4
    point[1] = (6,4)   edge[1]: (4-6)(5+4) = -18
    point[2] = (4,5)   edge[2]: (1-4)(5+5) = -30
    point[3] = (1,5)   edge[3]: (1-1)(0+5) =   0
    point[4] = (1,0)   edge[4]: (5-1)(0+0) =   0
                                           ---
                                           -44  counter-clockwise
    from https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order?answertab=votes
    """
    t1 = (coord[1, 0] - coord[0, 0]) * (coord[1, 1] + coord[0, 1])
    t2 = (coord[2, 0] - coord[1, 0]) * (coord[2, 1] + coord[1, 1])
    t3 = (coord[3, 0] - coord[2, 0]) * (coord[3, 1] + coord[2, 1])
    t4 = (coord[0, 0] - coord[3, 0]) * (coord[0, 1] + coord[3, 1])
    res = t1 + t2 + t3 + t4
    if res > 0:
        return True
    return False


def change_clock_wise(coords: np.array):
    """将索引1和4调换位置，即从逆时针变换为顺时针"""
    tmp = coords.copy()
    coords[1, :], coords[3, :] = tmp[3, :], tmp[1, :]
    return coords


# coords = np.array([457,862,731,865,720,900,457,894]).reshape(4, 2)
# print(validate_clockwise(coords))
# coords = [[0, 1], [1, 0], [1, 1], [0, 0]]
# center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))
# print(sorted(coords, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360))
# print(change_clock_wise(coords.copy()).reshape(8).tolist())
# print(validate_clockwise(change_clock_wise(coords.copy())))

import glob

txts = [x.replace("\\", "/") for x in glob.glob("./train_images/*.txt")]

for idx, p in enumerate(txts):
    print(p, end=" ")
    coords = []
    with open(p, "r", encoding="utf-8") as f:
        list(map(lambda x: coords.append([int(y) for y in x.strip("\n").strip(",###").split(",")]), f.readlines()))
    # print(coords)
    # break
    f_w = open(p, "w", encoding="utf-8")
    for coord in coords:
        coord = np.array(coord).reshape(4, 2)
        flag = validate_clockwise(coord.copy())
        print(flag)
        if not flag:
            coord = change_clock_wise(coord.copy()).reshape(8).tolist()
        else:
            coord = coord.copy().reshape(8).tolist()
        f_w.write(",".join([str(x) for x in coord]) + ",###\n")
    f_w.close()
    print(idx + 1, len(txts))

