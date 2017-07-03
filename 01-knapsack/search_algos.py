from __future__ import division
import numpy as np
from operator import attrgetter
import time

from tree_utils import Node

def get_values_and_weights(items):
    values = []
    weights = []
    for item in items:
        values.append(item.value)
        weights.append(item.weight)
    values = np.asarray(values)
    weights = np.asarray(weights)
    return values, weights

def branch_and_bound(capacity, item_count, items):
    """
    Take a node N off the queue.
    If N represents a single candidate solution x and f(x) < B
        then x is the best solution so far. Record it and set B = f(x).
    Else, branch on N to produce 2 nodes Ni. For each of these:
        If g(Ni) > B,
            do nothing; since the lower bound on this node is greater than the upper bound of the problem, it will never lead to the optimal solution, and can be discarded.
        Else,
            store Ni on the queue.
    """
    MAX_PATIENCE = 10 * 60
    new_items = sorted(items, key=attrgetter('value_weight'), reverse=True)
    values, weights = get_values_and_weights(items)

    LIFO = []
    _id = []
    negative_id = []
    global_best = 0
    node_counter = 0
    skipped_nodes = 0
    taken = 0
    value = [0]*len(items)
    tot_nodes = 2**((item_count+1) - 1)
    LIFO.append(Node(_id, negative_id, items, capacity, values, weights))

    start = time.time()
    try:
        while len(LIFO) > 0:
            if time.time() - start > MAX_PATIENCE:
                break
            current_node = LIFO.pop()
            node_counter += 1
            if current_node.is_leaf() and \
                    current_node.get_node_value() > global_best and \
                    current_node.get_node_room() >= 0:
                global_best = current_node.get_node_value()
                taken, value, room = current_node.get_node_solution()
            else:
                if current_node.get_node_estimate() < global_best or \
                            current_node.get_node_room <= 0:
                    skipped_nodes += (2**(item_count + 1 - current_node.get_node_depth()))
                else:
                    left_brach, right_branch = current_node.branch()
                    # branch produces None when it's not possible to branch
                    if left_brach:
                        _id, negative_id = left_brach
                        LIFO.append(Node(_id, negative_id, items, capacity, values, weights))
                    if right_branch:
                        _id, negative_id = right_branch
                        LIFO.append(Node(_id, negative_id, items, capacity, values, weights))
                    else:
                        skipped_nodes += (2**(item_count + 1 - current_node.get_node_depth()))

            if node_counter % 10000 == 0:
                print('Explored {} nodes'.format(node_counter))
                print('Skipped {} nodes'.format(skipped_nodes))
                print('progress: {:.2f}%'.format((node_counter + skipped_nodes) / tot_nodes * 100))
                print('Global best so far: {}'.format(global_best))

    except KeyboardInterrupt:
        print('stopping at ...')
        print('Maybe non optimal solution: {}\nValue: {}'.format(taken, value))
        print('Explored {} nodes'.format(node_counter))
        print('Skipped {} nodes'.format(skipped_nodes))
        print('Global best thus far: {}'.format(global_best))
        return taken, value

    print('Optimal solution: {}\nValue: {}'.format(taken, value))
    print('Explored {} nodes'.format(node_counter))
    print('Skipped {} nodes'.format(skipped_nodes))
    print('Global best: {}'.format(global_best))
    return taken, value

def trivial_greedy(capacity, item_count, items):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    try:
        for item in items:
            # print('item index: {}'.format(item.index))
            if weight + item.weight <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight
    except KeyboardInterrupt:
        print('stopping at item {}'.format(item))
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
    try:
        for trial in range(2**len(items)):
            taken = list(format(trial, '#0{}b'.format(item_count+2)))[2:]
            taken = np.asarray(map(int, taken))
            value = np.sum(taken * values)
            weight = np.sum(taken * weights)
            if trial % 100 == 0:
                print('value: {}, weight: {}'.format(value, weight))
                print('trial {} over {}'.format(trial, 2**len(items)))
            if value > max_value and weight <= capacity:
                max_value = value
                return_taken = list(taken)
            del(taken)
            del(value)
    except KeyboardInterrupt:
        print('stopping at trial {}'.format(trial))

    return return_taken, max_value
