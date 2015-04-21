import sys
import random
import time

def generate_children(current):
	#get the current location of the 0 (blank space) is at
	current_location = current.state.index(0)
	#initiate the list that will be sent back with the children
	children = []

	#generate the up move, if not at the top levels
	if current_location > 2:
		#Blank is not sitting on index 0, 1 or 2
		upper_index = current_location - 3
		up = current.state[:]
		up = swap(up, current_location, upper_index)
		children.append(init_node(up, current, "up", current.depth + 1, 0))

	#generate the left move, if not on left-most side
	if current_location % 3 != 0:
		#left most indices are all a factor of 3, so this loop will be ignored
		#if we are at the left most tiles
		left_index = current_location - 1
		left = current.state[:]
		left = swap(left, current_location, left_index)
		children.append(init_node(left, current, "left", current.depth + 1, 0))

	#generate the right move, if not on right-most side
	if current_location != 2 and current_location != 5 and current_location != 8:
		#right-most indices are 2, 5, 8, so we create a child if we are not
		#in any of these
		right_index = current_location + 1
		right = current.state[:]
		right = swap(right, current_location, right_index)
		children.append(init_node(right, current, "right", current.depth + 1, 0))

	#generate the down move, if not on the bottom-most tiles
	if current_location < 5:
		#bottom-most indices are greater than 5, so we can just exclude them
		bottom_index = current_location + 3
		down = current.state[:]
		down = swap(down, current_location, bottom_index)
		children.append(init_node(down, current, "down", current.depth + 1, 0))

	return children

	
def swap(L, i, j):
	L[j], L[i] = L[i], L[j]
	return L

	
def in_place_selection_sort(L):
	#CPSC 335 Code
	#Algorithm takes the lowest heuristic value and puts it in the first spot of the array.
	#Each successive will be the next lowest until the algorithm reaches the k-1 spot. 
	for k in range (len(L)-1):
		least = k
		for i in range (k+1, len(L)):
			if L[i].heuristic_value < L[least].heuristic_value:
				least = i
		#swap elements
		L[k], L[least] = L[least], L[k]
	return L


def sum_of_distances_out_of_place(current, goal):
	heuristic_value = 0
	for i in range(1, 9):
		# Reference from:
		# http://www.cyotek.com/blog/converting-2d-arrays-to-1d-and-accessing-as-either-2d-or-1d
		current_index = current.state.index(i)
		cy = current_index / 3
		cx = current_index - (cy * 3)
		
		goal_index = goal.index(i)
		gy = goal_index / 3
		gx = goal_index - (cy * 3)
		#Reference from:
		#http://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
		heuristic_value += abs(cx - gx) + abs(cy - gy)
	return heuristic_value + current.depth
	
def tiles_out_of_place(current, goal):
	#Assign a heuristic value to each by comparing child to goal state
	heuristic_value = 0 
	#heuristic value goes up for each cv and gv that don't match
	#cv = current value and gv = goal value
	for cv, gv in zip(current.state, goal):
		if(cv != gv):
			if(cv != 0):
				#Ignores the blank as it is not a tile.
				heuristic_value += 1
	return heuristic_value + current.depth


def calculate_heuristic_value(current, goal, choice):
	heuristic_value = 0
	if choice == 1:
		heuristic_value = tiles_out_of_place(current, goal)
		return heuristic_value
	elif choice == 2:
		heuristic_value = sum_of_distances_out_of_place(current, goal)
		return heuristic_value
	elif choice == 3:
		pass
	else:
		sys.exit(1)
	
	
def best_first_search(start, goal, choice):
	#Begin Best-First Search Algorithm
	#Set up the open and closed states.
	#Open state is initiated empty.
	open_states = []
	#Append the starting node by initiating in a node object.
	open_states.append(init_node(start, None, None, 0, 0))
	#Closed state is initiated empty
	closed_states = []

	#The loop that controls the entire best-first search algorithm
	while open_states != []:
		#Pop the front most value of the list, as it will be the one with the lowest heuristic value
		current = open_states.pop()

		if current.state == goal:
			#We are finished. Returning the list that has all the states that led to goal.
			closed_states.append(current)
			return closed_states
		else:
			#generate possible children that can be made
			children = generate_children(current)

			#check if children already exists
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

				child.heuristic_value = calculate_heuristic_value(child, goal, choice)

				if exists_in_open == False and exists_in_closed == False:
					#child does not exists in both states
					open_states.append(child)
				elif exists_in_open == True and exists_in_closed == False:
					#child exists in open states
					if child.heuristic_value < open_states[index].heuristic_value:
						open_states.pop(index)
						open_states.append(child)
				elif exists_in_open == False and exists_in_closed == True:
					#child exists in closed states
					if child.heuristic_value < closed_states[index].heuristic_value:
						closed_states.pop(index)
						open_states.append(child)
				else:
					#ruh-roh child exists in both
					sys.exit("Child is in both states. Fix it!")
		#Put X in closed
		closed_states.append(current)
		#Sort the open states by heuristic merit
		open_states = in_place_selection_sort(open_states)
		open_states.reverse()
		print("open states -----------")
		for state in open_states:
			print_state(state.state)
			print ("h-val = %i" % state.heuristic_value)
		print ("End of iteration---------")

	return None

def print_state(node):
	print (node[0], node[1], node[2])
	print (node[3], node[4], node[5])
	print (node[6], node[7], node[8])

def init_node(state, parent, direction, depth, heuristic_value):
	#Node and all its values are sent in to this method and then a Node object is returned
	#with all the values put together
	return Node(state, parent, direction, depth, heuristic_value)

class Node:
	def __init__(self, state, parent, direction, depth, heuristic_value):
		#This class object is used to hold all the values necessary for each node.
		self.state = state
		self.parent = parent
		self.direction = direction
		self.depth = depth
		self.heuristic_value = heuristic_value

		
def main():
	# Setting up a value to pass in through the terminal, to decide which heuristic to used.
	if int(sys.argv[1]) > 0 and int(sys.argv[1]) < 4 and len(sys.argv) == 2:
		choice = int(sys.argv[1])
	else:
		# Choice will just default to one, in case the values are not what the program demands.
		choice = 1
	
	print ("Welcome to the CS481 Artificial Intelligence Term Project")
	if choice == 1:
		print("You selected the tiles out of place heuristic")
	elif choice == 2:
		print("You selected the sum of distances out of place heuristic")
	elif choice == 3:
		pass
	#Initiating start state for 8-puzzle by shuffling the values of the start state.
	#Book example in page 141
	start = [2, 8, 3, 1, 6, 4, 7, 0, 5]
	#start = [1,2,3,8,0,4,7,6,5]
	random.shuffle(start)

	#Initiating the goal state of the 8-puzzle
	goal = [1,2,3,8,0,4,7,6,5]

	#Call Best-First Search Algorithm Function
	print("Please wait.....")
	result = best_first_search(start, goal, choice)

	for res in result:
		print("-------Results---------")
		print("Depth = %i" % res.depth)
		print("HV = %i" % res.heuristic_value)
		print_state(res.state)
		print("")

		
if __name__ == '__main__':
	main()