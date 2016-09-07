import numpy as np

from constants import *


class Puzzle(object):

	sides = 0
	puzzle_list = []
	puzzle_grid = []

	def __init__(self, puzzle_list):
		self.puzzle_list = puzzle_list
		boxes = [Box(val) for val in puzzle_list]
		self.puzzle_grid = np.reshape(boxes, (NUM_ROWS, NUM_COLS))


	def solve(self):
		pass

	def print_puzzle(self):
		print np.reshape(self.puzzle_list, (NUM_ROWS, NUM_COLS))



class Box(object):

	val 	 = 0
	possible = []
	row 	 = None
	col      = None
	coord    = None

	def __init__(self, val, (row, col), puzzle_list):
		self.val = val
		self.row = row
		self.col = col
		self.coord = (row,col)
		self.possible = update_possible_vals(puzzle_list) if val==0 else []


	def update_possible_vals(self, puzzle_list):
		
		possible = list(set(itertools.chain(
			get_neighbors(puzzle_list),
			get_row(puzzle_list),
			get_col(puzzle_list))))

		self.possible = possible
		return possible

	def get_neighbors(self, puzzle_list):

		grid_row = self.row / 3
		grid_col = self.col / 3

		np.reshape(puzzle_list, (9,9))

		return np.flatten(puzzle_list[grid_row*3:(grid_row+1)*3, grid_col*3:(grid_col*3)+1])

	def get_row(self, puzzle_list):
		return puzzle_list[self.row, :]

	def get_col(self, puzzle_list):
		return puzzle_list[:, self.col]





if __name__ == '__main__':

	test_puzzle = np.array([0,1,0,0,8,0,0,2,0,
							5,0,0,0,0,0,0,0,1,
							0,2,4,1,0,3,5,7,0,
							1,0,0,0,0,0,0,0,5,
							0,0,5,8,0,9,4,0,0,
							9,0,0,0,0,0,0,0,7,
							0,5,9,4,0,2,1,8,0,
							4,0,0,0,0,0,0,0,2,
							0,6,0,0,1,0,0,4,0])


	puzzle = Puzzle(test_puzzle)

	puzzle.print_puzzle()

	box00 = puzzle.puzzle_grid[0,0]

	print box00.val
	print box00.update_possible_vals(puzzle.puzzle_list)
	print box00.possible