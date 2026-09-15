from config import GameConfig
from mazegenerator import MazeGenerator


class PacGum:
    def __init__(self, maze: MazeGenerator, config: GameConfig) -> None:
        self.pac_gum: list[list[int]] = [
            [0 if val == 15 else 1 for val in row] for row in maze.maze
        ]
        self.value = config.point_per_pacgum
