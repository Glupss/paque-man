import pygame
from mazegenerator import MazeGenerator

WIDTH = 20
HEIGHT = 20
WALL_THIKNESS = 1
BOX_SIZE = 20
BORDER = 1
WALL_N = 1  # 0001
WALL_E = 2  # 0010
WALL_S = 4  # 0100
WALL_W = 8  # 1000


def box_px(box_col: int) -> int:
    """Box x position"""
    return (box_col + BORDER) * BOX_SIZE


def box_py(box_row: int) -> int:
    """Box y position"""
    return (box_row + BORDER) * BOX_SIZE


def draw_rectangle(
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
            if 0 <= i < surface.get_width() and 0 <= j < surface.get_height():
                pixels[i, j] = color


def draw_box(
    surface: pygame.Surface,
    pixels: pygame.PixelArray,
    box_col: int,
    box_row: int,
    color: tuple,
) -> None:
    """Push a specific box (cell of the maze) into the raw memory"""
    origin_x = box_px(box_col) + WALL_THIKNESS
    origin_y = box_py(box_row) + WALL_THIKNESS
    fill = BOX_SIZE - (2 * WALL_THIKNESS)
    draw_rectangle(
        surface,
        pixels,
        origin_x,
        origin_y,
        fill,
        fill,
        color,
    )


def draw_wall_n(
    surface: pygame.Surface,
    pixels: pygame.PixelArray,
    box_col: int,
    box_row: int,
    color: tuple,
) -> None:
    """Push the north wall into raw memory"""
    origin_x = box_px(box_col) + WALL_THIKNESS
    origin_y = box_py(box_row)
    draw_rectangle(
        surface,
        pixels,
        origin_x,
        origin_y,
        (BOX_SIZE - (2 * WALL_THIKNESS)),
        WALL_THIKNESS,
        color,
    )


def draw_wall_s(
    surface: pygame.Surface,
    pixels: pygame.PixelArray,
    box_col: int,
    box_row: int,
    color: tuple,
) -> None:
    """Push the south wall into raw memory"""
    origin_x = box_px(box_col) + WALL_THIKNESS
    origin_y = box_py(box_row) + (BOX_SIZE - WALL_THIKNESS)
    draw_rectangle(
        surface,
        pixels,
        origin_x,
        origin_y,
        (BOX_SIZE - (2 * WALL_THIKNESS)),
        WALL_THIKNESS,
        color,
    )


def draw_wall_e(
    surface: pygame.Surface,
    pixels: pygame.PixelArray,
    box_col: int,
    box_row: int,
    color: tuple,
) -> None:
    """Push the east wall into raw memory"""
    origin_x = box_px(box_col) + (BOX_SIZE - WALL_THIKNESS)
    origin_y = box_py(box_row) + WALL_THIKNESS
    draw_rectangle(
        surface,
        pixels,
        origin_x,
        origin_y,
        WALL_THIKNESS,
        (BOX_SIZE - (2 * WALL_THIKNESS)),
        color,
    )


def draw_wall_w(
    surface: pygame.Surface,
    pixels: pygame.PixelArray,
    box_col: int,
    box_row: int,
    color: tuple,
) -> None:
    """Push the west wall into raw memory"""
    origin_x = box_px(box_col)
    origin_y = box_py(box_row) + WALL_THIKNESS
    draw_rectangle(
        surface,
        pixels,
        origin_x,
        origin_y,
        WALL_THIKNESS,
        (BOX_SIZE - (2 * WALL_THIKNESS)),
        color,
    )


def draw_box_walls(
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
    WALL_N = 1  # 0001
    WALL_E = 2  # 0010
    WALL_S = 4  # 0100
    WALL_W = 8  # 1000
    """
    if bitmask & WALL_W:
        draw_wall_w(surface, pixels, box_col, box_row, color)
    if bitmask & WALL_S:
        draw_wall_s(surface, pixels, box_col, box_row, color)
    if bitmask & WALL_E:
        draw_wall_e(surface, pixels, box_col, box_row, color)
    if bitmask & WALL_N:
        draw_wall_n(surface, pixels, box_col, box_row, color)


def draw(surface, maze: list[list[int]], fill: bool = False) -> None:
    """Draw the maze on the screen"""

    pixels = pygame.PixelArray(surface)
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color_box = (0, 0, 0)
            # if maze[row][col] == 15 and fill is True:
            #    color_box = theme["42"]
            draw_box(
                surface,
                pixels,
                col,
                row,
                color_box,
            )
            draw_box_walls(
                surface,
                pixels,
                col,
                row,
                maze[row][col],
                (0, 255, 0),
            )
    pixels.close()


def draw_player(surface, pos: tuple[int, int]) -> None:
    """Draw the maze on the screen"""

    pixels = pygame.PixelArray(surface)
    draw_box(surface, pixels, pos[0], pos[1], color=(238, 233, 0))
    pixels.close()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1200, 800))
    screen.fill((0, 0, 0))

    maze_gen = MazeGenerator((20, 20))

    maze_grid = maze_gen.maze
    draw(screen, maze_gen.maze)

    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()
