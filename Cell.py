#The cell class contains attributes that carachterize the cells, such as alive, pressed and location
#alive indicates whether cell is alive or not
#to_be informs which state of cell in next step, whether alive or not
#pressed informs if cell is pressed by user
#location returns position x and y the cell in board
class cell:

	def __init__(self,location,alive = False):
		self.to_be = None
		self.alive = alive
		self.pressed = False
		self.location = location


