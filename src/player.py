class Player:
    def __init__(self, maze: MazeGenerator, start: tuple(int, int) = (0, 0)):
        self.start = start
        self.maze = maze
        self.grid = maze.maze
        self.pos = start

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
