from abc import ABC, abstractmethod
from entity import Entity
from player import Player
from math import dist
from config import GameConfig


class Ghost(Entity, ABC):
    def __init__(
        self,
        maze_grid: list[list[int]],
        start_row: int,
        start_col: int,
        pac_man: Player,
        config: GameConfig,
        escape: tuple = (0, 0),
        speed: int = 2,
    ):
        super().__init__(maze_grid, start_row, start_col, config, speed)

        self.last_pos = (start_row, start_col)
        self.target = (0, 0)
        self.pac_man = pac_man
        self.escape = escape
        self.flee = False

    def grid_to_pix(self, x, y) -> tuple[int, int]:
        config = self.config
        px = (y + config.padding) * config.box_size + (config.box_size // 2)
        py = (
            (x + config.padding) * config.box_size
            + (config.box_size // 2)
            + config.top_offset
        )
        return (px, py)

    def move_to_target(self) -> None:
        if self.is_centered(*self.grid_pos):
            possible_tiles: list[tuple[int, int]] = []

            neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]

            for tile in neighbors:
                dx, dy = tile
                target_cell = (
                    self.grid_pos[0] + dy,
                    self.grid_pos[1] + dx,
                )
                if (
                    self.can_move(self.grid_pos[0], self.grid_pos[1], tile)
                    and self.is_valid_pos(target_cell)
                    and target_cell != self.last_pos
                ):
                    possible_tiles.append(tile)

            if not possible_tiles:
                dy = self.last_pos[0] - self.grid_pos[0]
                dx = self.last_pos[1] - self.grid_pos[1]
                possible_tiles.append((dx, dy))

            self.current_dir = min(
                possible_tiles,
                key=lambda tile: self.get_dist(
                    self.grid_to_pix(
                        self.grid_pos[0] + tile[1],
                        self.grid_pos[1] + tile[0],
                    ),
                    self.target,
                ),
            )

        self.x += self.current_dir[0] * self.speed
        self.y += self.current_dir[1] * self.speed
        row, col = self.get_grid_pos()
        if self.is_centered(row, col):
            self.last_pos = self.grid_pos
            self.grid_pos = (row, col)

    def is_valid_pos(self, pos: tuple[int, int]) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= len(self.grid) or pos[1] >= len(self.grid[0]):
            return False
        if self.grid[pos[0]][pos[1]] == 15:
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
        maze_grid: list[list[int]],
        pac_man: Player,
        start_row: int,
        start_col: int,
        config: GameConfig,
        blinky,
        escape: tuple = (0, 0),
    ):
        super().__init__(
            maze_grid=maze_grid,
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
