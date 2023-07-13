class Coords:
	def __init__(
		self,
		row: int = 0,
		col: int = 0,
	):
		self.row = row
		self.col = col

	def __eq__(self, obj):
		return self.row == obj.row and self.col == obj.col

	def __repr__(self):
		return f'({self.row}, {self.col})'

	def change_row(self, value: int):
		self.row += value

	def change_col(self, value: int):
		self.col += value

	def with_changed_row(self, value: int):
		return Coords(self.row + value, self.col)

	def with_changed_col(self, value: int):
		return Coords(self.row, self.col + value)