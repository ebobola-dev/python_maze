from random import randint

from models.cell import Cell
from models.coords import Coords
from models.move import Move, Direction

class Maze:
	def __init__(
		self,
		size: int,
	):
		self.size = size
		#? Создаем матрицу стен
		self.field = [[Cell(Coords(row, col), is_wall=True) for col in range(size)] for row in range(size)]
		#? Текущая позиция (откуда ходим дальше)
		self.current_position: Coords = Coords(1, 1)
		self.moves: list[Move] = []
		self.free_cells = 0
		self.right_way: list[Move] = []
		#? Бурим ячейки где надо
		self.create_cells()
		#? Долбим вход и выход
		self.create_holes()

	def show(self):
		for row in range(self.size):
			for col in range(self.size):
				print(f'{self.field[row][col]}', end=' ')
			print()

	def create_cells(self):
		for row in range(1, self.size, 2):
			for col in range(1, self.size, 2):
				self.field[row][col].is_wall = False
				self.free_cells += 1

	def create_holes(self):
		#? Сносим вход
		self._set_visited(Coords(0, 1))
		#? Сносим выход
		self._set_visited(Coords(self.size - 1, self.size - 2))

	#? Говорим точке, что её уже прошли
	def _set_visited(self, coords: Coords):
		self.field[coords.row][coords.col].visited = True
		#? Если точка была стеной, сносим её
		self.field[coords.row][coords.col].is_wall = False


	#? Удаляем последний ход, и возвращаем "текущую позицию" на предыдущую
	def remove_last_move(self):
		self.current_position = self.moves.pop(len(self.moves) - 1).start_point

	def _move(self):
		#? Куда можем сходить (влево на CONFIG.MOVE_LEN, вниз, вправо вверх)
		potential_moves: list[Move] = [Move(self.current_position, Direction(i)) for i in range(4)]

		#? Проверяем куда реально можем сходить
		wrong_move_indexes = []
		for index, potential_move in enumerate(potential_moves):
			#? Проверка на границы
			if potential_move.end_point.row < 0 or potential_move.end_point.col < 0 or potential_move.end_point.row > self.size - 1 or potential_move.end_point.col > self.size - 1:
				wrong_move_indexes.append(index)
				continue
			#? Проверка на visited (уже были в этой точке)
			if self.field[potential_move.end_point.row][potential_move.end_point.col].visited:
				wrong_move_indexes.append(index)
				continue

		#? Удаляем неподходящие ходы
		for i in range(len(wrong_move_indexes) - 1, -1, -1):
			potential_moves.pop(wrong_move_indexes[i])

		#? Если ходов не осталось возвращаем False
		if not len(potential_moves):
			return False

		#? Выбираем рандомный ход из оставшихся
		move = potential_moves[randint(0, len(potential_moves) - 1)]

		#? Закрашиваем стену
		self._set_visited(move.get_middle_point())

		#? Закрашиваем конечную точку
		self.field[move.end_point.row][move.end_point.col].visited = True

		#? Ставим текущую позицию
		self.current_position = move.end_point
		#? Сохраняем ход
		self.moves.append(move)
		#? Убавляем свободные ячейки
		self.free_cells -= 1

		#? Если пришли на выход, запоминаем путь
		if move.end_point == Coords(self.size - 2, self.size - 2):
			self.right_way = self.moves[:]

		return True

	def generate(self):

		#? Ставим начальную ячейку (1, 1)
		self._set_visited(self.current_position)
		self.free_cells -= 1

		#? Ходим(долбим стены) пока не заполним все ячейки
		while self.free_cells:
			if not self._move():
				#? Если _move вернул False значит из текущей позиции ходить некуда, удаляем предыдущий ход и ходим дальше
				self.remove_last_move()

		print("ЛАБИРИНТ: ")
		self.show()
		print('\n')

	def find_way(self):
		#? Вход
		self.field[0][1].is_win_way = True
		#? Путь (отрисовываем первую и среднюю точку хода, последнюю не рисуем потому что она является первой у следущего хода)
		for move in self.right_way:
			self.field[move.start_point.row][move.start_point.col].is_win_way = True
			self.field[move.get_middle_point().row][move.get_middle_point().col].is_win_way = True

		#? Конечная точка пути
		self.field[self.size - 2][self.size - 2].is_win_way = True
		#? Выход
		self.field[self.size - 1][self.size - 2].is_win_way = True
		print("РЕШЕНИЕ: ")
		self.show()