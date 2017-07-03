#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

from collections import namedtuple
import numpy as np
import time

from search_algos import branch_and_bound, trivial_greedy, weighted_greedy, exhaustive_search
Item = namedtuple("Item", ['index', 'value', 'weight', 'value_weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), int(parts[0]) / int(parts[1])))

    print('Solving for {} items'.format(item_count))
    now = time.time()
    w_taken, w_value = weighted_greedy(capacity, item_count, items)
    b_taken, b_value = branch_and_bound(capacity, item_count, items)
    print('Elapsed time: {:.2f} seconds'.format(time.time() - now))
    print('B&B value: {}\nweightded_greedy: {}'.format(b_value, w_value))
    if b_value > w_value:
        value = b_value
        taken = b_taken
    else:
        value = w_value
        taken = w_taken
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
