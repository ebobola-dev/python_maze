from models.coords import Coords

class Cell:
	def __init__(
			self,
			coords: Coords = Coords(),
			visited: bool = False,
			is_wall: bool = False,
			is_win_way: bool = False,
		):
		self.coords = coords
		self.is_wall = is_wall			#? Ячейка является стеной
		self.visited = visited			#? По ячейке уже сходили
		self.is_win_way = is_win_way	#? Для вывода верного пути

	def __repr__(self):
		if self.is_wall:
			#return '\033[91m▮\033[00m' #!
			return '▮'
		if self.is_win_way:
			return '\033[91m●\033[00m'
		elif self.visited:
			#return '\033[92m▮\033[00m' #*
			return ' '
		else:
			return '▮'