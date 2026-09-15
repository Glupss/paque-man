from mazegenerator import MazeGenerator
from abc import ABC, abstractmethod
from player import Player


class Ghost(ABC):
    def __init__(
        self,
        maze: MazeGenerator,
        pac_man: Player,
        start: tuple = (0, 0),
    ):
        self.start = start
        self.maze = maze
        self.grid = maze.maze
        self.pos = start
        self.target = (0, 0)
        self.pac_man = pac_man

    def move_to_target(
        self,
    ) -> None:
        queue = [(self.pos, [self.pos])]

        visited = {self.pos}
        while queue:
            current, path = queue.pop(0)

            if current == self.target and len(path) > 1:
                self.pos = path[1]

            x, y = current

            neighbors = [
                (x, y - 1),
                (x + 1, y),
                (x, y + 1),
                (x - 1, y),
            ]

            for target in neighbors:
                if self.can_move(current, target) and self.is_valid_pos(
                    target
                ):
                    if target not in visited:
                        visited.add(target)
                        new_path = path + [target]
                        queue.append((target, new_path))

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

    @abstractmethod
    def chose_target(self):
        pass


class Blinky(Ghost):
    def chose_target(
        self,
    ) -> None:
        self.target = self.pac_man.pos


class Inky(Ghost):
    def chose_target(
        self,
    ) -> None:
        print("f")


class Pinky(Ghost):
    def chose_target(
        self,
    ) -> None:
        print("f")


class Clyde(Ghost):
    def chose_target(
        self,
    ) -> None:
        print("f")
