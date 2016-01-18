from Cell import cell
from collections import OrderedDict
import random
from Compartment import Compartment
#This class builds the board, inserting cells according to configurations defined by parameters
class board:

	def __init__(self, map_size, img_alive, img_dead, square_size, number_generations_to_be_recovered, number_generations_to_be_infected, quantity_cells_around):
		self.map = []
		self.map_size=map_size
		self.alive=img_alive
		self.dead=img_dead
		self.square_size=square_size
		self.number_generations_to_be_recovered=number_generations_to_be_recovered
		self.number_generations_to_be_infected=number_generations_to_be_infected
		self.quantity_cells_around=quantity_cells_around

	def fill(self,ran):
		for i in xrange(self.map_size):
			self.map.append([])
			for g in xrange(self.map_size):
				if ran == True:
					a = random.randint(0,4)
					if a == 0: 
						self.map[i].insert(g,cell((i,g),Compartment.infected, self.number_generations_to_be_recovered, self.number_generations_to_be_infected))
					else: 
						self.map[i].insert(g,cell((i,g), Compartment.susceptible,self.number_generations_to_be_recovered, self.number_generations_to_be_infected))	
				else: 
					self.map[i].insert(g,cell((i,g),Compartment.susceptible,self.number_generations_to_be_recovered, self.number_generations_to_be_infected))					

	def draw(self, screen):
		for i in xrange(self.map_size):
			for g in xrange(self.map_size):
				cell = self.map[i][g]
				loc = cell.location
				if cell.alive == Compartment.infected: 
					screen.blit(self.alive,(loc[0]*self.square_size,loc[1]*self.square_size))
				else: 
					screen.blit(self.dead,(loc[0]*self.square_size,loc[1]*self.square_size))

	def get_cells(self, cell):# gets the cells around a cell
		cells_around = []
		cells_state = []
		cells_alive = 0
		cell_loc = cell.location

		try: cells_around.append(self.map[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
		except Exception: pass
		try: cells_around.append(self.map[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
		except Exception: pass
		try: cells_around.append(self.map[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
		except Exception: pass
		try: 
			cells_around.append(self.map[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
		except Exception: pass
		try: 
			cells_around.append(self.map[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
		
		except Exception: pass
		try: cells_around.append(self.map[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
		except Exception: pass
		try: cells_around.append(self.map[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
		except Exception: pass
		try: cells_around.append(self.map[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
		except Exception: pass
		# removes duplicates
		cells_around=list(OrderedDict.fromkeys(cells_around))
		for i in xrange(len(cells_around)): 
			cells_state.append(self.map[cells_around[i][0]][cells_around[i][1]].alive)
		for i in cells_state:# cells_alive houses how many cells are alive around it
			if i == Compartment.infected:
				 cells_alive+=1
		#The rules are the following:
		#If cell is alive, it continues alive if double minus 4 is greater than 5
		#If cell is dead, it turns alive if 3 or 6 cells around it are alive or has 8 cells around it
		if cell.alive == Compartment.infected:
			if (cells_alive *2 -4)>5:
				cell.to_be = Compartment.infected
			else:
				cell.to_be=Compartment.susceptible

		else:
			if cells_alive %3 == 0 or len(cells_around)-2>6: cell.to_be = Compartment.infected
							  #rules
	def update_frame(self):
		for i in xrange(self.map_size):
			for g in xrange(self.map_size):
				cell = self.map[i][g]
				self.get_cells(cell)

	def update(self, screen):
		for i in xrange(self.map_size):
			for g in xrange(self.map_size):
				cell = self.map[i][g]
				loc = cell.location
				if cell.to_be != None: 
					cell.alive = cell.to_be
				if self.map[i][g].alive == Compartment.infected:
					 screen.blit(self.alive,(loc[0]*self.square_size,loc[1]*self.square_size))
				else: 
					screen.blit(self.dead,(loc[0]*self.square_size,loc[1]*self.square_size))
				cell.to_be = None


