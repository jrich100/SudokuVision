import cv2
import numpy as np
import constants

from PIL import Image
from pytesser import *



def find_puzzle(img_fn):
	
	#Read in the image
	img = cv2.imread(img_fn,1)

	#find puzzle corners in pixel coords
	rect_corners = find_square(img)

	#straighten and center the image
	puzzle_img = warp_and_center(rect_corners, img)

	#separate into boxes
	boxes = get_boxes(puzzle_img)

	#read boxes
	puzzle_list = read_boxes(boxes)

	return puzzle_list



def find_square(img):

	gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	edges = cv2.Canny(blur, 30, 200)

	_,cnts,_ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	corners = None
	for c in cnts:
		if cv2.contourArea(c) > 10:
			# approximate the contour
			approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
			
			#check if rectangle
			if len(approx) == 4:
				corners = approx

	if corners is not None:
		cv2.drawContours(img, [corners], -1, (0, 255, 0), 3)
		cv2.imshow('res',img)
		cv2.waitKey(0)

	else:
		print "Puzzle not Found"

	return np.reshape(corners, (4,2))


def warp_and_center(rect, img):
	rect = np.asarray(rect, dtype= "float32")
	dstRect = np.array([[0,0],
						[0, constants.PUZZLE_SIDE_PIXELS],
						[constants.PUZZLE_SIDE_PIXELS, constants.PUZZLE_SIDE_PIXELS],
						[constants.PUZZLE_SIDE_PIXELS, 0]], dtype = "float32")

	H = cv2.getPerspectiveTransform(rect, dstRect)
	warped = cv2.warpPerspective(img, H, constants.IMG_SIZE)

	cv2.imshow('res',warped)
	cv2.waitKey(0)

	return warped


def get_boxes(puzzle_img):
	h,w,_ = puzzle_img.shape

	boxes = []
	sideLen = w/constants.NUM_COLS
	for col in xrange(constants.NUM_COLS):
		for row in xrange(constants.NUM_ROWS):
			box = puzzle_img.copy()[col*sideLen:(col+1)*sideLen, row*sideLen:(row+1)*sideLen]
			boxes.append(box)

#	for i, box in enumerate(boxes):
#		cv2.imshow('box '+str(i), cv2.resize(box, (h,w)))
#		cv2.waitKey(0)
	
	return boxes


def read_boxes(boxes):

	if not boxes:
		print "No boxes to read"
	
	return [get_digit(box) for box in boxes]

def get_digit(img):

	pass





def overlay(img_fn, rect, answer):
	pass

if __name__ == '__main__':
	img1 = "solved.png"
	img2 = "unsolved.png"

	print find_puzzle(img1)
	print find_puzzle(img2)