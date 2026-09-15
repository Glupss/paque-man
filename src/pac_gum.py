from config import GameConfig
from mazegenerator import MazeGenerator


class PacGum:
    def __init__(
        self,
        maze: MazeGenerator,
        config: GameConfig,
        start_col: int,
        start_row: int,
    ) -> None:
        self.pac_gum: list[list[int]] = [
            [0 if val == 15 else 1 for val in row] for row in maze.maze
        ]
        self._clear_42_zone(maze.maze, 2)
        self.value = config.point_per_pacgum
        self.pac_gum[start_row][start_col] = 0

    def _clear_42_zone(self, maze_grid: list[list[int]], margin: int) -> None:
        """ """
        min_row = len(maze_grid)
        max_row = 0
        min_col = len(maze_grid[0])
        max_col = 0
        is_42 = False

        for r in range(len(maze_grid)):
            for c in range(len(maze_grid[0])):
                if maze_grid[r][c] == 15:
                    is_42 = True
                    min_row = min(min_row, r)
                    max_row = max(max_row, r)
                    min_col = min(min_col, c)
                    max_col = max(max_col, c)

        if is_42:
            for r in range(min_row - margin, max_row + margin + 1):
                for c in range(min_col - margin, max_col + margin + 1):
                    if 0 <= r < len(self.pac_gum) and 0 <= c < len(
                        self.pac_gum[0]
                    ):
                        self.pac_gum[r][c] = 0
