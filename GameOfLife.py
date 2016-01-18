from collections import OrderedDict
import pygame,random
from pygame.locals import *
from Cell import cell
from Board import board 
from Compartment import Compartment

pygame.init()

speed = 4 # how many iterations per second
squares = 2 # size of squares: 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
map_size = 20 # the width and height

if squares == 0:
	imgs = ["res/infected_8.png","res/susceptible_8.png",8]
elif squares == 1:
	imgs = ["res/infected_16.png","res/susceptible_16.png",16]
elif squares == 2:
	imgs = ["res/infected_32.png","res/susceptible_32.png",32]
elif squares == 3:
	imgs = ["res/infected_64.png","res/susceptible_64.png",64]

#If other value different than 0,1,2,3,4 inserted, the default value is 8 
else:
	imgs=["res/infected_8.png","res/susceptible_8.png",8]
#-----CONFIG-----

#screen size
square_size=imgs[2]
width = map_size*square_size
height = map_size*square_size
screen_size = width,height

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

#loads the image to dead and alive cells
img_alive = pygame.image.load(imgs[0]).convert()
img_dead = pygame.image.load(imgs[1]).convert()
done = False

#constants required to calculate contact and infectious rates
#range 0...10
SINGER_POPULARITY=1
MEDIA_DIVULGATION=5

#variables that will be calculated from by constants
quantity_cells_around=0
number_generations_to_be_infected=0
number_generations_to_be_recovered=0 

#formula rates
contact_rate=0
recovery_rate=0

def cell_list():
    lst = []
    for i in xrange(map_size):
    	lst.append([])
        for g in xrange(map_size): 
		lst[i].append((board.map[i][g].location[0]*square_size,board.map[i][g].location[1]*square_size))
    return lst

board = board(map_size, img_alive, img_dead, square_size)
board.fill(False)
board.draw(screen)  
tp = 0

#indicates whether the game runs or not
run = False

while done == False:
	milliseconds = clock.tick(60)
	seconds = milliseconds / 1000.0
	tp += milliseconds

	#retrieve user commands
	for event in pygame.event.get():
		if event.type == QUIT:
			done = True

		#If pressed key SPACE, the game is paused if has been running or executed if has been paused
		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				run = not run

		#If pressed key "Q", the game execute the next step
		elif event.type == KEYUP:
			if event.key == K_q:
				run = False
				board.update_frame()
				board.update(screen)

		elif event.type == MOUSEBUTTONUP:
			for i in xrange(map_size):
				for g in xrange(map_size):
					board.map[i][g].pressed = False

	pressed = pygame.key.get_pressed()
	mouse = pygame.mouse.get_pressed()
	pos = pygame.mouse.get_pos()

	#if press the key "R", resets automaton
	if pressed[K_r]:
		board.map = []
		board.fill(False)
		board.draw(screen)
	#if press the key "A", fill automaton in a aleatory mode
	if pressed[K_a]:
		board.map = []
		board.fill(True)
		board.draw(screen)

	if run == True and tp >= 1000/speed :
		tp = 0
		board.update_frame()
		board.update(screen)

	if mouse[0]:# makes cells alive
		rects = cell_list()
		for i in xrange(map_size):
			for g in xrange(map_size):
				if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+square_size and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+square_size and board.map[i][g].pressed == False:
					board.map[i][g].alive = Compartment.infected
					board.map[i][g].pressed = True
					board.update(screen)

	if mouse[2]: # kills cells
		rects = cell_list()
		for i in xrange(map_size):
			for g in xrange(map_size):
				if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+square_size and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+square_size and board.map[i][g].pressed == False:
					board.map[i][g].alive = Compartment.susceptible
					board.map[i][g].pressed = False
					board.update(screen)

	pygame.display.flip()

pygame.quit()
