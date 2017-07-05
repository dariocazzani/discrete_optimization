#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

from algos import trivial_solver, solver
from utils import tour_length

Point = namedtuple("Point", ['index', 'x', 'y'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])

    points = []
    for i in range(1, node_count+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(i-1, float(parts[0]), float(parts[1])))

    # print(points)
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution, points = solver(points)
    # solution, points = trivial_solver(points)

    # calculate the length of the tour
    obj = tour_length(points, solution)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
