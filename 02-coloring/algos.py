from __future__ import division
import numpy as np
from collections import OrderedDict
import time

def find_adjacent_nodes(node, edges):
	other_nodes = []
	for edge in edges:
		if node in edge:
			other_node = [x for x in list(edge) if x != node][0]
			other_nodes.append(other_node)
	# print('\nNode: {}\nOther Nodes: {}'.format(node, other_nodes))
	return other_nodes

def find_nodes_color(nodes, nodes_color):
	# print('finding colors for these nodes: {}'.format(nodes))
	colors = nodes_color[nodes]
	colored = np.where(colors != -1)
	return colors[colored]

def difference(first, second):
	second = set(second)
	return [item for item in first if item not in second]

def intersect(a, b):
	return list(set(a) & set(b))

def trivial_solver(edges, node_count):
	# build a trivial solution
	# every node has its own color
	solution = range(0, node_count)
	return solution, node_count

def order_by_degree(edges, node_count, reverse):
	a = []
	for edge in edges:
		a.append(edge[0])
		a.append(edge[1])
	set_a = set(a)
	print('ordering {} elements...'.format(node_count))
	sorted_a = {}
	for unique in set_a:
		sorted_a[unique] = a.count(unique)
	unique_sorted_a = []
	# sort by key
	for key, _ in sorted(sorted_a.iteritems(), key=lambda (k,v): (v,k), reverse=reverse):
		unique_sorted_a.append(key)
	return unique_sorted_a

def greedy(edges, node_count):
	# color available
	color_candidates = range(0, node_count)
	# for each possible color, keep track how many times it was used
	color_used = np.zeros((node_count))
	# initialize each node with no color assignement. -1 means no color
	nodes_color = np.ones((node_count)) * -1

	nodes = order_by_degree(edges, node_count, True)
	for idx, node in enumerate(nodes):
		# print('progress: {:.2f}%'.format(idx / len(nodes) * 100))
		# Initialize color candidates
		color_candidates = range(0, node_count)
		# find adjacent nodes
		other_nodes = find_adjacent_nodes(node, edges)
		# find the used colors for the adjacent nodes
		colors = find_nodes_color(other_nodes, nodes_color)
		# print('Adjacent nodes colors: {}'.format(colors))
		# remove the list of used colors from the color candidates for this node
		available_colors = difference(color_candidates, colors)
		# print('Available colors: {}'.format(available_colors))
		# print('Color used: {}'.format(color_used))
		# select the color for this node from the color_used array with the maximum usage
		sorted_used_colors = sorted(range(len(color_used)), key=lambda k: color_used[k])
		# print('sorted_used_colors: {}'.format(sorted_used_colors))
		favourite_color = intersect(sorted_used_colors, available_colors)[0]
		# print('favourite_color : {}'.format(favourite_color))
		nodes_color[node] = favourite_color
		color_used[favourite_color] += 1
	return nodes_color, color_used

def improve_greedy(nodes_color, edges, node_count, color_used, greedy_solution):
	sorted_used_colors = sorted(range(node_count), key=lambda k: color_used[k])
	# for each node with that color
	#   try for each another used_color that is compatible
	done = False
	best_solution = greedy_solution
	best_nodes_color = nodes_color
	best_color_used = color_used
	# give the improvement algorithm MAX_PATIENCE seconds
	MAX_PATIENCE = np.log(node_count-48)*1500
	print('Max patience in seconds {}'.format(MAX_PATIENCE))
	start = time.time()
	nodes = order_by_degree(edges, node_count, True)
	try:
		while not done:
			node = np.random.randint(0, len(nodes))
			# find adjacent nodes
			other_nodes = find_adjacent_nodes(node, edges)
			# find the used colors for the adjacent nodes
			colors = find_nodes_color(other_nodes, nodes_color)
			# print('other nodes colors {}'.format(colors))
			# available colors are the all colors that are used a part from the most uncommon
			available_colors = sorted_used_colors[-len(set(nodes_color))+1:]
			# print('available_colors: {}'.format(available_colors))
			usable_colors = difference(available_colors, colors)
			# print('usable_colors{}'.format(usable_colors))
			# print('usable_colors: {}'.format(usable_colors))
			if usable_colors:
				usable_color = usable_colors[np.random.randint(0, len(usable_colors))]
				# print('chaning node {} from color {} to color {}'.format(node, nodes_color[node], usable_color))
				previous_color = nodes_color[node]
				nodes_color[node] = usable_color
				color_used[int(nodes_color[node])] -= 1
				color_used[usable_color] += 1
				if len(set(nodes_color)) < best_solution:
					print('improving from {} to {}'.format(best_solution, len(set(nodes_color))))
					best_solution = len(set(nodes_color))
					best_nodes_color = nodes_color
					best_color_used = color_used

		if time.time() - start > MAX_PATIENCE:
			done = True
	except KeyboardInterrupt:
		print('stopping at this solution {}'.format(best_solution))

	return best_nodes_color, best_color_used

def solver(edges, node_count):
	nodes_color, color_used = greedy(edges, node_count)
	greedy_solution = len(set(nodes_color))
	print('solution before improving: {}'.format(greedy_solution))
	nodes_color, color_used = improve_greedy(nodes_color, edges, node_count, color_used, greedy_solution)
	print('solution after improving: {}'.format(len(set(nodes_color))))
	solution = map(int, list(nodes_color))
	colors = len(set(nodes_color))

	return solution, colors
