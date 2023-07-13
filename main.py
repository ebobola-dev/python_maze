from models.field import Maze

from config import CONFIG

maze = Maze(CONFIG.MAZE_SIZE)
maze.generate()
maze.find_way()


