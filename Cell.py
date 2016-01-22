#The cell class contains attributes that carachterize the cells, such as alive, pressed and location
#alive indicates whether cell is alive or not
#to_be informs which state of cell in next step, whether alive or not
#pressed informs if cell is pressed by user
#location returns position x and y the cell in board
#generations_remaining indicate how many generations left to cell be recovered or infected
#probability_to receives the probability the cell to be infected or recovered
from Compartment import Compartment
class cell:

	def __init__(self,location,alive, to_cure, to_infection, probability_to_infection, probability_to_cure):
		self.to_be = None
		self.alive = alive
		self.pressed = False
		self.location = location
		self.generations_remaining_to_cure=to_cure
		self.generations_remaining_to_infection=to_infection
		self.probability_to_infection=probability_to_infection
		self.probability_to_cure=probability_to_cure


