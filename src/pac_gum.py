from mazegenerator import MazeGenerator


class PacGum:
    def __init__(self, maze: MazeGenerator) -> None:
        self.pac_gum: list[list[int]] = [
            [0 if val == 15 else 1 for val in row] for row in maze.maze
        ]
        self.size: int = 3
        self.value: int = 10
