from __future__ import division

from utils import distance, progress
import numpy as np
import copy
import operator
import matplotlib.pyplot as plt

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

def plot_points(points):
    for point in points:
        plt.scatter(point.x, point.y, alpha=0.5)
    plt.show()

def greedy_solver(points):
    new_points = []
    old_points = copy.deepcopy(points)
    next_point = 0#np.random.randint(0, len(points))
    current_point = old_points.pop(next_point)
    new_points.append(current_point)
    counter = 0
    total_points = len(old_points)
    while old_points:
        progress(counter, total_points)
        counter += 1
        # find distances from current point to all other available points
        distances = find_distances(current_point, old_points)
        # select the shortest distance
        next_point = distances[0][0]
        # pop and add
        index = find_point_by_index(next_point, old_points)
        current_point= old_points.pop(index)
        new_points.append(current_point)
        # print(distances)
    print('')

    plot_points(points)

    solution = []
    for point in new_points:
        solution.append(point.index)

    return solution, points


def trivial_solver(points):
    node_count = len(points)
    solution = range(0, node_count)
    return solution, points
