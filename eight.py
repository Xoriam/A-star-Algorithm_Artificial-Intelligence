import sys
import random
import time


class Node:
	def __init__(self, state, depth, cost):
		self.state = state
		self.depth = depth
		self.cost = cost

	def print_node(self):
		print (self.state[0], self.state[1], self.state[2])
		print (self.state[3], self.state[4], self.state[5])
		print (self.state[6], self.state[7], self.state[8])


def calculate_cost(child, goal, choice):
	if choice:
		cost = tiles_out_of_place(child, goal) 
	return cost

def tiles_out_of_place(child, goal):
	hOfN = 0
	for cv, gv in zip(child.state, goal):
		if (cv != gv):
			if(cv != 0):
				hOfN = hOfN + 1
	return hOfN + child.depth


def swap(offspring, i, j):
	offspring[j], offspring[i] = offspring[i], offspring[j]
	return offspring


def generate_children(parent, goal, choice):
	blank_index = parent.state.index(0)
	children = []

	if blank_index > 2:
		upper_index = blank_index - 3
		up = parent.state[:]
		up = swap(up, blank_index, upper_index)
		up_child = Node(up, parent.depth + 1, 0)
		up_child.cost = calculate_cost(up_child, goal, choice)
		# print up_child.cost
		# up_child.print_node()
		children.append(up_child)

	if blank_index % 3 != 0:
		left_index = blank_index - 1
		left = parent.state[:]
		left = swap(left, blank_index, left_index)
		left_child = Node(left, parent.depth + 1, 0)
		left_child.cost = calculate_cost(left_child, goal, choice)
		# print left_child.cost
		# left_child.print_node()
		children.append(left_child)

	if blank_index != 2 and blank_index != 5 and blank_index != 8:
		right_index = blank_index + 1
		right = parent.state[:]
		right = swap(right, blank_index, right_index)
		right_child = Node(right, parent.depth + 1, 0)
		right_child.cost = calculate_cost(right_child, goal, choice)
		# print right_child.cost
		# right_child.print_node()
		children.append(right_child)

	if blank_index < 5:
		bottom_index = blank_index + 3
		down = parent.state[:]
		down = swap(down, blank_index, bottom_index)
		bottom_child = Node(down, parent.depth + 1, 0)
		bottom_child.cost = calculate_cost(bottom_child, goal, choice)
		# print bottom_child.cost
		# bottom_child.print_node()
		children.append(bottom_child)

	return children



def in_place_selection_sort(open_list):
	for k in range(len(open_list) - 1):
		greatest = k
		for i in range(k + 1, len(open_list)):
			if open_list[i].cost > open_list[greatest].cost:
				greatest = i
		# swap elements
		open_list[k], open_list[greatest] = open_list[greatest], open_list[k]
	return open_list


def best_first_search(start, goal, choice):
	open_states = []
	open_states.append(Node(start, 0, 0))

	closed_states = []
	counter = 0
	while open_states != []:
		counter += 1
		next = open_states.pop()
		if next.state == goal:
			closed_states.append(next)
			return closed_states, counter
		else:
			children = generate_children(next, goal, choice)

			for child in children:
				exists_in_open = False
				exists_in_closed = False
				index = None
				for node in open_states:
					if node.state == child.state:
						exists_in_open = True
						index = open_states.index(node)
						break
				for node in closed_states:
					if node.state == child.state:
						exists_in_closed = True
						index = closed_states.index(node)
						break

				if exists_in_open is False and exists_in_closed is False:
					open_states.append(child)
				elif exists_in_open is True:
					if child.cost < open_states[index].cost:
						open_states.pop(index)
						open_states.append(child)
				elif exists_in_closed is True:
					if child.cost < closed_states[index].cost:
						closed_states.pop(index)
						open_states.append(child)
				else:
					sys.exit(1)

		closed_states.append(next)
		sorted_list = in_place_selection_sort(open_states)
		open_states = sorted_list
		#time.sleep(5)

	return None


def main():
	print("Welcome to A* Algorithm Implementation of the CS481 Term Project")

	choice = 1
	start = [4, 1, 2, 0, 8, 7, 6, 3, 5]
	#random.shuffle(start)
	#start = [2, 8, 3, 1, 6, 4, 7, 0, 5]
	goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	result, count = best_first_search(start, goal, choice)
	print (count)
	for each in result:
		print("=============")
		each.print_node()
		print("=============")

if __name__ == '__main__':
	main()