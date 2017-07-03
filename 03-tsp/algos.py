from __future__ import division

from utils import distance
import numpy as np
import copy
import operator

def find_distances(origin, points):
    distances = {}
    for point in points:
        distances[point.index] = distance(origin, point)
    sorted_distances = sorted(distances.items(), key=operator.itemgetter(1))
    return sorted_distances

def find_point_by_index(next_point, points):
    for index, point in enumerate(points):
        if point.index == next_point:
            return index

def greedy_solver(points):
    new_points = []
    old_points = copy.deepcopy(points)
    next_point = np.random.randint(0, len(points))
    current_point = old_points.pop(next_point)
    new_points.append(current_point)
    while old_points:
        # find distances from current point to all other available points
        distances = find_distances(current_point, old_points)
        # select the shortest distance
        next_point = distances[0][0]
        # pop and add
        index = find_point_by_index(next_point, old_points)
        current_point= old_points.pop(index)
        new_points.append(current_point)
        # reorder points py index
        # print(distances)

    solution = []
    for point in new_points:
        solution.append(point.index)

    return solution, new_points


def trivial_solver(points):
    node_count = len(points)
    solution = range(0, node_count)
    return solution, points
