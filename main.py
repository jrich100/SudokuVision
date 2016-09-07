import sudoku
import camera
import vision
import os
import numpy as np

#img_fn = os.getcwd() + "\\test_puzzle.jpg"
img_fn = "test_puzzle.png"

if __name__ == '__main__':

	print "--- Starting Sudoku Solver ---\n\n\n"

	puzzle_list = vision.find_puzzle(img_fn)
	print "Puzzle found\n"
	print np.reshape(puzzle_list, (9,9))

	puzzle = sudoku.Puzzle(puzzle_list)
	puzzle.solve()

	puzzle.print_unsolved()
	puzzle.print_solved()

	print "Puzzle solved\n"

	#vision.overlay(img_fn, rect, answer)


	print "--- Finished ---"