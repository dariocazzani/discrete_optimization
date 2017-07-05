from __future__ import division

from utils import distance, progress, tour_length
import numpy as np
import copy
import operator
import matplotlib.pyplot as plt
import time
import random

def find_log_patience(x):
	# define static point where the curve passes through
	y1 = 2
	y2 = 1000
	x1 = 51
	x2 = 33800
	a = (y1-y2) / np.log(x1 / x2)
	b = np.exp((y2*np.log(x1)-y1*np.log(x2))/(y1-y2))
	return a*np.log(b*x)

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

def plot_points(points, solution):
	plt.figure(1)
	plt.subplot(211)
	ax = plt.axes()
	area = 100
	for point in points:
		plt.scatter(point.x, point.y, s=area, alpha=0.5)

	for index in range(0, len(points)-1):
		x = points[solution[index]].x
		y = points[solution[index]].y
		dx = points[solution[index+1]].x - points[solution[index]].x
		dy = points[solution[index+1]].y - points[solution[index]].y
		ax.arrow(x, y, dx, dy, head_width=0.05, head_length=0.01, fc='k', ec='k')
	plt.show()

def improve_greedy_2OPT(points, solution):
	# print('*** 2-OPT ***')
	best_tour_length = tour_length(points, solution)
	MAX_PATIENCE = find_log_patience(len(points))
	done = False
	start = time.time()
	try:
		# 2-OPT
		while not done:
			i = np.random.randint(1, len(points))
			j = np.random.randint(0, len(points)-1)
			new_s = solution[:j] + solution[j:j+i+1][::-1] + solution[j+i+1:]
			current_tour_length = tour_length(points, new_s)
			if current_tour_length < best_tour_length:
				best_tour_length = current_tour_length
				solution = copy.deepcopy(new_s)
				# print('New solution with length: {}'.format(best_tour_length))
				# done = True
				print('stopping at this solution {}'.format(best_tour_length))
			if time.time() - start > MAX_PATIENCE:
				done = True
	except KeyboardInterrupt:
		print('stopping at this solution {}'.format(best_tour_length))

	return solution, points

# not sure if this is 3-OPT or just random swapping
def improve_greedy_3OPT(points, solution):
	# print('*** 3-OPT ***')
	best_tour_length = tour_length(points, solution)
	MAX_PATIENCE = find_log_patience(len(points))
	done = False
	start = time.time()
	try:
		# 3-OPT
		while not done:
			position1, position2 = random.sample(range(0, len(points)), 2)
			# insert a node in an other position
			solution.insert(position1, solution.pop(position2))
			current_tour_length = tour_length(points, solution)
			if current_tour_length < best_tour_length:
				best_tour_length = current_tour_length
				# print('New solution with length: {}'.format(best_tour_length))
				# done = True
			else:
				# insert back
				solution.insert(position2, solution.pop(position1))
			if time.time() - start > MAX_PATIENCE:
				done = True
				print('stopping at this solution {}'.format(best_tour_length))
	except KeyboardInterrupt:
		print('stopping at this solution {}'.format(best_tour_length))

	return solution, points

def greedy_solver(points):
	new_points = []
	old_points = copy.deepcopy(points)
	next_point = np.random.randint(0, len(points))
	current_point = old_points.pop(next_point)
	new_points.append(current_point)
	counter = 0
	total_points = len(old_points)
	while old_points:
		progress(counter, total_points-1)
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

	solution = []
	for point in new_points:
		solution.append(point.index)

	return solution, points

def swap(points, solution):
	print('*** swap ***')
	best_tour_length = tour_length(points, solution)
	MAX_PATIENCE = 10
	done = False
	start = time.time()
	try:
		# swap
		while not done:
			position1, position2 = random.sample(range(0, len(points)), 2)
			# swap 2 nodes
			solution[position1], solution[position2] = solution[position2], solution[position1]
			current_tour_length = tour_length(points, solution)
			if current_tour_length < best_tour_length:
				best_tour_length = current_tour_length
				print('New solution with length: {}'.format(best_tour_length))
				done = True
			else:
				# swap back
				solution[position1], solution[position2] = solution[position2], solution[position1]
			if time.time() - start > MAX_PATIENCE:
				for _ in range(10):
					position1, position2 = random.sample(range(0, len(points)), 2)
					solution[position1], solution[position2] = solution[position2], solution[position1]
				done = True
	except KeyboardInterrupt:
		print('stopping at this solution {}'.format(best_tour_length))

	return solution, points

def solver(points):
	print('number of points: {}'.format(len(points)))
	solution, points = greedy_solver(points)
	# solution = list(np.random.permutation(len(points)))
	# plot_points(points, solution)
	# alternate 2-OPT with 3-OPT
	best_tour_length = tour_length(points, solution)
	no_improvements_count = 0
	print('Tour length before improvement": {}'.format(best_tour_length))

	for i in range(3):
		solution, points = improve_greedy_3OPT(points, solution)
		solution, points = improve_greedy_2OPT(points, solution)
		current_tour_length = tour_length(points, solution)
		if current_tour_length < best_tour_length:
			no_improvements_count = 0
			best_tour_length = current_tour_length
			best_solution = copy.deepcopy(solution)
			print('New best solution with length: {}'.format(best_tour_length))
		else:
			no_improvements_count += 1

		if no_improvements_count % 2 ==0 :
			print('** swap **')
			p1, p2 = random.sample(range(0, len(points)), 2)
			solution[p1], solution[p2] = solution[p2], solution[p1]
			print('After swap, tour length: {}'.format(tour_length(points, solution)))

	best_tour_length = tour_length(points, best_solution)
	print('Best tour length after improvement 2 and 3-OPT": {}'.format(best_tour_length))
	# plot_points(points, solution)
	return best_solution, points

def trivial_solver(points):
	node_count = len(points)
	solution = range(0, node_count)
	return solution, points
