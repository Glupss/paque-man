from mazegenerator import MazeGenerator
from abc import ABC, abstractmethod
from player import Player
from math import dist
from config import GameConfig


class Ghost(ABC):
    def __init__(
        self,
        maze: MazeGenerator,
        pac_man: Player,
        start_col: int,
        start_row: int,
        config: GameConfig,
        escape: tuple = (0, 0),
    ):
        self.maze = maze
        self.grid = maze.maze
        self.config = config
        self.grid_pos = (start_col, start_row)
        self.target = (0, 0)
        self.pac_man = pac_man
        self.escape = escape
        self.speed = 2
        self.last_pos = (0, 0)
        self.current_dir = (0, 0)
        self.flee = False

        # pix coordinate
        self.x = (start_col + config.padding) * config.box_size + (
            config.box_size // 2
        )
        self.y = (
            (start_row + config.padding) * config.box_size
            + (config.box_size // 2)
            + config.top_offset
        )

    def grid_to_pix(self, x, y) -> tuple[int, int]:
        config = self.config
        px = (x + config.padding) * config.box_size + (config.box_size // 2)
        py = (
            (y + config.padding) * config.box_size
            + (config.box_size // 2)
            + config.top_offset
        )
        return (px, py)

    def move_to_target(
        self,
    ) -> None:
        if self.is_centered(*self.grid_pos):
            possible_tiles: list[tuple[int, int]] = []
            neighbors = [(1, 0), (0, -1), (0, 1), (-1, 0)]

            for tile in neighbors:
                target = (
                    self.grid_pos[0] + tile[0],
                    self.grid_pos[1] + tile[1],
                )
                if (
                    self.can_move(self.grid_pos, target)
                    and self.is_valid_pos(target)
                    and target != self.last_pos
                ):
                    possible_tiles.append(tile)

            if not possible_tiles:
                dx = self.last_pos[0] - self.grid_pos[0]
                dy = self.last_pos[1] - self.grid_pos[1]
                possible_tiles.append((dx, dy))

            self.current_dir = min(
                possible_tiles,
                key=lambda tile: self.get_dist(
                    self.grid_to_pix(
                        self.grid_pos[0] + tile[0],
                        self.grid_pos[1] + tile[1],
                    ),
                    self.target,
                ),
            )

        self.x += self.current_dir[0] * self.speed
        self.y += self.current_dir[1] * self.speed
        col, row = self.get_grid_pos()
        if self.is_centered(col, row):
            self.last_pos = self.grid_pos
            self.grid_pos = (col, row)

    def is_centered(self, col, row) -> bool:
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
        return col, row

    def is_valid_pos(self, pos: tuple[int, int]) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return False
        elif pos[0] > len(self.grid[0]) - 1 or pos[1] > len(self.grid) - 1:
            return False
        if self.grid[pos[1]][pos[0]] == 15:
            return False
        return True

    def can_move(
        self,
        curr_pos: tuple[int, int],
        new_pos: tuple[int, int],
    ) -> bool:
        """
        Check either we can move or not based on the wall positions
        return True = OK
        Return False = NOT OK
        """
        WALL_N = 1  # 0001
        WALL_E = 2  # 0010
        WALL_S = 4  # 0100
        WALL_W = 8  # 1000

        if new_pos[1] < curr_pos[1]:
            # UP
            if self.grid[curr_pos[1]][curr_pos[0]] & WALL_N:
                return False
        elif new_pos[1] > curr_pos[1]:
            # DOWN
            if self.grid[curr_pos[1]][curr_pos[0]] & WALL_S:
                return False
        elif new_pos[0] < curr_pos[0]:
            # LEFT
            if self.grid[curr_pos[1]][curr_pos[0]] & WALL_W:
                return False
        elif new_pos[0] > curr_pos[0]:
            # RIGHT
            if self.grid[curr_pos[1]][curr_pos[0]] & WALL_E:
                return False
        return True

    def get_dist(
        self, tile: tuple[int, int], target: tuple[int, int]
    ) -> float:
        return dist(tile, target)

    @abstractmethod
    def chose_target(self):
        pass


class Blinky(Ghost):
    def chose_target(
        self,
    ) -> None:
        if not self.flee:
            self.target = (self.pac_man.x, self.pac_man.y)
        else:
            self.target = self.grid_to_pix(self.escape[0], self.escape[1])


class Inky(Ghost):
    def __init__(
        self,
        maze: MazeGenerator,
        pac_man: Player,
        start_col: int,
        start_row: int,
        config: GameConfig,
        blinky,
        escape: tuple = (0, 0),
    ):
        super().__init__(
            maze=maze,
            pac_man=pac_man,
            start_col=start_col,
            start_row=start_row,
            config=config,
            escape=escape,
        )
        self.blinky = blinky

    def chose_target(
        self,
    ) -> None:
        if not self.flee:
            anchor = (
                self.pac_man.x + (self.pac_man.dir[0] * 120),
                self.pac_man.y + (self.pac_man.dir[1] * 120),
            )
            self.target = (
                2 * anchor[0] - self.blinky.x,
                2 * anchor[1] - self.blinky.y,
            )
        else:
            self.target = self.grid_to_pix(self.escape[0], self.escape[1])


class Pinky(Ghost):
    def chose_target(
        self,
    ) -> None:
        if not self.flee:
            self.target = (
                self.pac_man.x + (self.pac_man.dir[0] * 200),
                self.pac_man.y + (self.pac_man.dir[1] * 200),
            )
        else:
            self.target = self.grid_to_pix(self.escape[0], self.escape[1])


class Clyde(Ghost):
    def chose_target(
        self,
    ) -> None:
        if not self.flee:
            self.target = (self.pac_man.x, self.pac_man.y)
            if (
                self.get_dist(
                    self.grid_to_pix(self.grid_pos[0], self.grid_pos[1]),
                    self.target,
                )
                < 240
            ):
                self.target = self.grid_to_pix(self.escape[0], self.escape[1])
        else:
            self.target = self.grid_to_pix(self.escape[0], self.escape[1])
