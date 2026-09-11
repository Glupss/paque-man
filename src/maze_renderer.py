from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from mazegenerator import MazeGenerator


class MazeRenderer:
    def __init__(
        self,
        maze: MazeGenerator,
        padding: int,
        box_size: int,
        wall_thinkness: int,
    ) -> None:
        self.maze = maze
        self.padding = padding
        self.box_size = box_size
        self.wall_thikness = wall_thinkness

    def _box_px(self, box_col: int) -> int:
        """Box x position"""
        return (box_col + self.padding) * self.box_size

    def _box_py(self, box_row: int) -> int:
        """Box y position"""
        return (box_row + self.padding) * self.box_size

    def _draw_rectangle(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple,
    ):
        for i in range(x, x + width):
            for j in range(y, y + height):
                if (
                    0 <= i < surface.get_width()
                    and 0 <= j < surface.get_height()
                ):
                    pixels[i, j] = color

    def _draw_box(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        box_col: int,
        box_row: int,
        color: tuple,
    ) -> None:
        """Push a specific box (cell of the maze) into the raw memory"""
        origin_x = self._box_px(box_col) + self.wall_thikness
        origin_y = self._box_py(box_row) + self.wall_thikness
        fill = self.box_size - (2 * self.wall_thikness)
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            fill,
            fill,
            color,
        )

    def _draw_wall_n(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        box_col: int,
        box_row: int,
        color: tuple,
    ) -> None:
        """Push the north wall into raw memory"""
        origin_x = self._box_px(box_col) + self.wall_thikness
        origin_y = self._box_py(box_row)
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            (self.box_size - (2 * self.wall_thikness)),
            self.wall_thikness,
            color,
        )

    def _draw_wall_s(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        box_col: int,
        box_row: int,
        color: tuple,
    ) -> None:
        """Push the south wall into raw memory"""
        origin_x = self._box_px(box_col) + self.wall_thikness
        origin_y = self._box_py(box_row) + (self.box_size - self.wall_thikness)
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            (self.box_size - (2 * self.wall_thikness)),
            self.wall_thikness,
            color,
        )

    def _draw_wall_e(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        box_col: int,
        box_row: int,
        color: tuple,
    ) -> None:
        """Push the east wall into raw memory"""
        origin_x = self._box_px(box_col) + (self.box_size - self.wall_thikness)
        origin_y = self._box_py(box_row) + self.wall_thikness
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            self.wall_thikness,
            (self.box_size - (2 * self.wall_thikness)),
            color,
        )

    def _draw_wall_w(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        box_col: int,
        box_row: int,
        color: tuple,
    ) -> None:
        """Push the west wall into raw memory"""
        origin_x = self._box_px(box_col)
        origin_y = self._box_py(box_row) + self.wall_thikness
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            self.wall_thikness,
            (self.box_size - (2 * self.wall_thikness)),
            color,
        )

    def _draw_box_walls(
        self,
        surface: pygame.Surface,
        pixels: pygame.PixelArray,
        box_col: int,
        box_row: int,
        bitmask: int,
        color: tuple,
    ) -> None:
        """
        Push all the walls into raw memory,
        it uses bitmask to know where the walls are:
        """
        WALL_N = 1  # 0001
        WALL_E = 2  # 0010
        WALL_S = 4  # 0100
        WALL_W = 8  # 1000

        if bitmask & WALL_W:
            self._draw_wall_w(surface, pixels, box_col, box_row, color)
        if bitmask & WALL_S:
            self._draw_wall_s(surface, pixels, box_col, box_row, color)
        if bitmask & WALL_E:
            self._draw_wall_e(surface, pixels, box_col, box_row, color)
        if bitmask & WALL_N:
            self._draw_wall_n(surface, pixels, box_col, box_row, color)

    def draw(self, surface, fill: bool = False) -> None:
        """Draw the maze on the screen"""

        pixels = pygame.PixelArray(surface)
        for row in range(len(self.maze.maze)):
            for col in range(len(self.maze.maze[row])):
                color_box = (0, 0, 0)
                if self.maze.maze[row][col] == 15:
                    color_box = (255, 0, 0)
                self._draw_box(
                    surface,
                    pixels,
                    col,
                    row,
                    color_box,
                )
                self._draw_box_walls(
                    surface,
                    pixels,
                    col,
                    row,
                    self.maze.maze[row][col],
                    (33, 50, 197),
                )
        pixels.close()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1200, 800))
    screen.fill((0, 0, 0))

    maze_gen = MazeGenerator((20, 20))
    renderer = MazeRenderer(maze_gen, 1, 20, 1)

    renderer.draw(screen)

    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()
