from __future__ import division

import numpy as np

class Node(object):
    def __init__(self, _id, negative_id, items, capacity, values, weights):
        # _id is a list of the taken elements. i.e.: [0, 3, 4]
        self._id = _id
        self.negative_id = negative_id
        self.items = items
        self.capacity = capacity
        self.leaf = False

        self.values = values
        self.weights = weights

        self._get_depth()
        self._get_taken_and_removed()
        self._get_estimate()
        self._get_args()
        self.is_leaf()

    def _get_depth(self):
        len_id = len(self._id)
        len_negative_id = len(self.negative_id)
        self.depth = len_id + len_negative_id

    def _get_taken_and_removed(self):
        taken = [0]*len(self.items)
        removed = [0]*len(self.items)
        for i in range(self.depth):
            if i in self._id:
                taken[i] = 1
            elif i in self.negative_id:
                removed[i] = 1
        self.taken = np.asarray(taken)
        self.removed = np.asarray(removed)

    def _get_estimate(self):
        optimistic_estimate = 0.
        value = 0
        weight = 0
        removed = list(self.removed)

        # Assuming they are in descending order ov value/weight
        # for item in self.items:
        #     if weight + item.weight <= self.capacity:
        #         if item.index not in removed:
        #             value += item.value
        #             weight += item.weight
        #     else:
        #         if item.index not in removed:
        #             room_left = self.capacity - weight
        #             ratio = room_left / item.weight
        #             value += (item.value * ratio)
        #             break
        #     #     break
        #     # elif weight + item.weight > self.capacity and item.index not in removed:
        #
        # self.estimate = value
        for item in self.items:
            optimistic_estimate += item.value
        self.estimate = optimistic_estimate - np.sum(self.removed * self.values)
        # print('Estimate 1: {}\nEstimate 2: {}'.format(value, self.estimate))

    def _get_args(self):
        self.value = np.sum(self.taken * self.values)
        weight = np.sum(self.taken * self.weights)
        self.room = self.capacity - weight

    def is_leaf(self):
        if self.depth == len(self.items):
            self.leaf = True
        return self.leaf

    def get_node_estimate(self):
        return self.estimate

    def get_node_room(self):
        return self.room

    def get_node_value(self):
        return self.value

    def get_node_solution(self):
        return self.taken, self.value, self.room

    def get_node_depth(self):
        return self.depth

    def branch(self):
        if not self.leaf and self.room > 0:
            left_branch =  (self._id + [self.depth], self.negative_id)
            right_branch = (self._id, self.negative_id + [self.depth])

            return left_branch, right_branch
        return None, None
