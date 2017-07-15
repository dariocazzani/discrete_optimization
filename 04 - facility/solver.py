#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
import numpy as np
import cvxopt
import cvxopt.glpk
cvxopt.glpk.options['msg_lev'] = 'GLP_MSG_OFF'
cvxopt.glpk.options['tm_lim'] = 3600 * 10 ** 3 #1hr
#cvxopt.glpk.options['mip_gap'] = 0.10

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    def trivial_solver(facilities, customers):
        # build a trivial solution
        # pack the facilities one by one until all the customers are served
        # ==========
        solution = [-1]*len(customers)
        capacity_remaining = [f.capacity for f in facilities]

        facility_index = 0
        for customer in customers:
           if capacity_remaining[facility_index] >= customer.demand:
               solution[customer.index] = facility_index
               capacity_remaining[facility_index] -= customer.demand
           else:
               facility_index += 1
               assert capacity_remaining[facility_index] >= customer.demand
               solution[customer.index] = facility_index
               capacity_remaining[facility_index] -= customer.demand
        return solution

    print('We have {} customers'.format(len(customers)))

    # mip for 1, 2, 3, 4, 5, 6
    if len(customers) == 50 or len(customers) == 100 or len(customers) == 200 or len(customers) == 1000 or len(customers) == 800 or len(customers) == 3000 or len(customers) == 1500:
        solution = mip(facilities, customers)
    else:
        solution = trivial_solver(facilities, customers)

    # calculate the cost of the solution
    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def mip(facilities, customers):
    M = len(customers)
    N = len(facilities)
    c = []
    for j in range(N):
        c.append(facilities[j].setup_cost)
    for j in range(N):
        for i in range(M):
            c.append(length(facilities[j].location, customers[i].location))

    xA = []
    yA = []
    valA = []
    for i in range(M):
        for j in range(N):
            xA.append(i)
            yA.append(N + M * j + i)
            valA.append(1)

    b = np.ones(M)

    xG = []
    yG = []
    valG = []
    for i in range(N):
        for j in range(M):
            xG.append(M * i + j)
            yG.append(i)
            valG.append(-1)
            xG.append(M * i + j)
            yG.append(N + M * i + j)
            valG.append(1)

    for i in range(N):
        for j in range(M):
            xG.append(N * M + i)
            yG.append(N + M * i + j)
            valG.append(customers[j].demand)
    h = np.hstack([np.zeros(N * M),
                   np.array([fa.capacity for fa in facilities], dtype = 'd')])

    binVars=set()
    for var in range(N + M * N):
        binVars.add(var)

    status, isol = cvxopt.glpk.ilp(c = cvxopt.matrix(c),
                                   G = cvxopt.spmatrix(valG, xG, yG),
                                   h = cvxopt.matrix(h),
                                   A = cvxopt.spmatrix(valA, xA, yA),
                                   b = cvxopt.matrix(b),
                                   I = binVars,
                                   B = binVars)
    soln = []
    for i in range(M):
        for j in range(N):
            if isol[N + M * j + i] == 1:
                soln.append(j)
    return soln

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')
