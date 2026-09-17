from config import GameConfig


class Entity:
    def __init__(
        self,
        maze_grid: list[list[int]],
        start_row: int,
        start_col: int,
        config: GameConfig,
        speed: float,
    ) -> None:
        self.grid = maze_grid
        self.config = config
        self.speed = speed

        # pix coordinate
        self.x = (start_col + config.padding) * config.box_size + (
            config.box_size // 2
        )
        self.y = (
            (start_row + config.padding) * config.box_size
            + (config.box_size // 2)
            + config.top_offset
        )
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.grid_pos = (start_row, start_col)

    def get_grid_pos(self) -> tuple[int, int]:
        col = int(
            (self.x - (self.config.padding * self.config.box_size))
            // self.config.box_size
        )
        row = int(
            (
                self.y
                - self.config.top_offset
                - (self.config.padding * self.config.box_size)
            )
            // self.config.box_size
        )
        return row, col

    def is_centered(self, row, col) -> bool:
        target_x = (col + self.config.padding) * self.config.box_size + (
            self.config.box_size // 2
        )
        target_y = (
            (row + self.config.padding) * self.config.box_size
            + (self.config.box_size // 2)
            + self.config.top_offset
        )
        threshold = self.speed * 0.6
        if (
            abs(self.x - target_x) <= threshold
            and abs(self.y - target_y) <= threshold
        ):
            self.x = target_x
            self.y = target_y
            return True
        return False

    def can_move(
        self,
        row,
        col,
        direction,
    ) -> bool:
        """
        Check either we can move or not based on the wall positions
        return True = OK
        Return False = NOT OK
        """
        if direction == (0, 0):
            return False

        dx, dy = direction
        WALL_N = 1  # 0001
        WALL_E = 2  # 0010
        WALL_S = 4  # 0100
        WALL_W = 8  # 1000

        if dy == -1 and (self.grid[row][col] & WALL_N):
            return False
        if dy == 1 and (self.grid[row][col] & WALL_S):
            return False
        if dx == -1 and (self.grid[row][col] & WALL_W):
            return False
        if dx == 1 and (self.grid[row][col] & WALL_E):
            return False
        return True
