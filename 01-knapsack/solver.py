#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

from operator import attrgetter
from collections import namedtuple
import numpy as np
Item = namedtuple("Item", ['index', 'value', 'weight', 'value_weight'])

def trivial_greedy(capacity, item_count, items):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        print('item index: {}'.format(item.index))
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return taken, value

def weighted_greedy(capacity, item_count, items):
    new_items = sorted(items, key=attrgetter('value_weight'), reverse=True)
    return trivial_greedy(capacity, item_count, new_items)

def exhaustive_search(capacity, item_count, items):
    print('number of items: {}'.format(item_count))
    values = []
    weights = []
    for item in items:
        values.append(item.value)
        weights.append(item.weight)
    values = np.asarray(values)
    weights = np.asarray(weights)

    max_value = 0
    return_taken = None
    for trial in range(2**len(items)):
        taken = list(format(trial, '#06b'))[2:]
        taken = np.asarray(map(int, taken))
        value = np.sum(taken * values)
        weight = np.sum(taken * weights)
        print('value: {}, weight: {}'.format(value, weight))
        if value > max_value and weight <= capacity:
            max_value = value
            return_taken = list(taken)

    return return_taken, max_value

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

    taken, value = exhaustive_search(capacity, item_count, items)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
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
