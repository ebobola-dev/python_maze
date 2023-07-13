from enum import Enum

from models.coords import Coords

from config import CONFIG

class Direction(Enum):
	LEFT = 0
	DOWN = 1
	RIGHT = 2
	UP = 3

class Move:
	def __init__(
		self,
		start_point: Coords,
		direction: Direction,
	):
		self.start_point = start_point	#? Откуда ходим
		self.direction = direction		#? Направление хода
		#? Вычисляем конечную точку хода ↓↓↓
		match direction:
			case Direction.LEFT:
				self.end_point = start_point.with_changed_col(-CONFIG.MOVE_LEN)
			case Direction.DOWN:
				self.end_point = start_point.with_changed_row(CONFIG.MOVE_LEN)
			case Direction.RIGHT:
				self.end_point = start_point.with_changed_col(CONFIG.MOVE_LEN)
			case Direction.UP:
				self.end_point = start_point.with_changed_row(-CONFIG.MOVE_LEN)

	def __repr__(self):
		match self.direction:
			case Direction.LEFT:
				return f'{self.start_point}←{self.end_point}'
			case Direction.DOWN:
				return f'{self.start_point}↓{self.end_point}'
			case Direction.RIGHT:
				return f'{self.start_point}→{self.end_point}'
			case Direction.UP:
				return f'{self.start_point}↑{self.end_point}'

	def get_middle_point(self):
		match self.direction:
				case Direction.LEFT:
					return self.end_point.with_changed_col(1)
				case Direction.DOWN:
					return self.end_point.with_changed_row(-1)
				case Direction.RIGHT:
					return self.end_point.with_changed_col(-1)
				case Direction.UP:
					return self.end_point.with_changed_row(1)