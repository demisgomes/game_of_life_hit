from Cell import cell
from collections import OrderedDict
import random
from Compartment import Compartment
#This class builds the board, inserting cells according to configurations defined by parameters
class board:

	def __init__(self, map_size, img_alive, img_dead, square_size, number_generations_to_be_recovered, number_generations_to_be_infected, quantity_cells_around, img_recovered, probability_to_infection, probability_to_cure):
		self.map = []
		self.map_size=map_size
		self.alive=img_alive
		self.dead=img_dead
		self.square_size=square_size
		self.number_generations_to_be_recovered=number_generations_to_be_recovered
		self.number_generations_to_be_infected=number_generations_to_be_infected
		self.quantity_cells_around=quantity_cells_around
		self.recovered=img_recovered
		self.probability_to_infection=probability_to_infection
		self.probability_to_cure=probability_to_cure

	#the fill method insert the cells
	#Some can be infected, if the parameter ran is true
	def fill(self,ran):
		for i in xrange(self.map_size):
			self.map.append([])
			for g in xrange(self.map_size):
				if ran == True:
					a = random.randint(0,4)
					if a == 0: 
						self.map[i].insert(g,cell((i,g),Compartment.infected, self.number_generations_to_be_recovered, self.number_generations_to_be_infected, self.probability_to_infection, self.probability_to_cure))
					else: 
						self.map[i].insert(g,cell((i,g), Compartment.susceptible,self.number_generations_to_be_recovered, self.number_generations_to_be_infected, self.probability_to_infection, self.probability_to_cure))	
				else: 
					self.map[i].insert(g,cell((i,g),Compartment.susceptible,self.number_generations_to_be_recovered, self.number_generations_to_be_infected, self.probability_to_infection, self.probability_to_cure))
						
	#update the board with new cells values
	def draw(self, screen):
		for i in xrange(self.map_size):
			for g in xrange(self.map_size):
				cell = self.map[i][g]
				loc = cell.location
				if cell.alive == Compartment.infected: 
					screen.blit(self.alive,(loc[0]*self.square_size,loc[1]*self.square_size))
				elif cell.alive == Compartment.susceptible: 
					screen.blit(self.dead,(loc[0]*self.square_size,loc[1]*self.square_size))
				else:
					screen.blit(self.recovered,(loc[0]*self.square_size,loc[1]*self.square_size))

	#verify whether a cell will change your compartment or maintain it
	#Serve as for suscetible-> infected as infected->recovered	
	def random_probability(self,probability):
		random_result=random.randint(0,1000)
		if (random_result>(probability*1000)):
			return False
		return True

		
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
		#for each cell in board, it is made the following logic:
		#if cell is infected, it is infected by max n generations, where n was calculed in GameOfLife file
		#For each generation, the generations remaining to cure falls until 0, where the cell to be recovered
		#When generations remaining to cure falls, increases the probability to be recovered before all generations be completed
		
		#if susceptible, is verified if has n cells around it that are infected, where n also was calculed in GameOfLife
		#As infected cell, the probability to be infected increases
		#if a cell was alone, it also can be infected with less probability

		for i in cells_state:# cells_alive houses how many cells are alive around it
			if i == Compartment.infected:
				 cells_alive+=1
		if cell.alive == Compartment.infected:
			cell.generations_remaining_to_cure-=1
			cell.probability_to_cure+=cell.probability_to_cure/15.0
			if(cell.probability_to_cure > 1.0):
				cell.probability_to_cure=0.999
			if self.random_probability(cell.probability_to_cure):
				cell.to_be = Compartment.recovered
			elif cell.generations_remaining_to_cure==0:
				cell.to_be = Compartment.recovered
			else:
				cell.to_be=Compartment.infected
		elif cell.alive == Compartment.susceptible:
			if(cells_alive >= self.quantity_cells_around):
				cell.generations_remaining_to_infection-=1
				cell.probability_to_infection+=cell.probability_to_infection/10.0
				if(cell.probability_to_infection > 1.0):
					cell.probability_to_infection=0.999
				if self.random_probability(cell.probability_to_infection):
					cell.to_be = Compartment.infected
				elif cell.generations_remaining_to_infection==0:
					cell.to_be = Compartment.infected
			else:
				if self.random_probability(cell.probability_to_infection/10):
					cell.to_be=Compartment.infected
				else:
					cell.to_be=Compartment.susceptible
						
			
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
				elif self.map[i][g].alive== Compartment.susceptible: 
					screen.blit(self.dead,(loc[0]*self.square_size,loc[1]*self.square_size))
				else:
					screen.blit(self.recovered,(loc[0]*self.square_size,loc[1]*self.square_size))
				cell.to_be = None
