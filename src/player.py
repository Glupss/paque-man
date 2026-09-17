from config import GameConfig
from entity import Entity


class Player(Entity):
    def __init__(
        self,
        maze_grid: list[list[int]],
        start_row: int,
        start_col: int,
        config: GameConfig,
    ) -> None:
        super().__init__(
            maze_grid,
            start_row,
            start_col,
            config,
            speed=config.player_speed,
        )

        self.score = 0

    def update(self) -> None:
        row, col = self.get_grid_pos()
        if self.is_centered(row, col):
            if self.can_move(row, col, self.next_dir):
                self.dir = self.next_dir
            if not self.can_move(row, col, self.dir):
                self.dir = (0, 0)
        else:
            if (
                self.dir[0] == -self.next_dir[0]
                and self.dir[1] == -self.next_dir[1]
                and self.next_dir != (0, 0)
            ):
                self.dir = self.next_dir
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
