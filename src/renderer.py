from config import GameConfig
import pygame


class Renderer:
    def __init__(self, config: GameConfig) -> None:
        pygame.init()
        self.padding = config.padding
        self.box_size = config.box_size
        self.wall_thikness = config.wall_thikness
        self.color_wall = config.color_wall
        self.color_player = config.color_player
        self.color_pacgum = config.color_pacgum
        self.pacgum_radius = 3
        screen_w = (config.width + config.padding * 2) * config.box_size
        screen_h = (config.height + config.padding * 2) * config.box_size
        self.background_surface = pygame.Surface((screen_w, screen_h))
        self.screen = pygame.display.set_mode((screen_w, screen_h))

    def _box_px(self, box_col: int) -> int:
        return (box_col + self.padding) * self.box_size

    def _box_py(self, box_row: int) -> int:
        return (box_row + self.padding) * self.box_size

    def _draw_box(self, surface, pixels, box_col, box_row, color) -> None:
        origin_x = self._box_px(box_col) + self.wall_thikness
        origin_y = self._box_py(box_row) + self.wall_thikness
        fill = self.box_size - (2 * self.wall_thikness)
        self._draw_rectangle(
            surface, pixels, origin_x, origin_y, fill, fill, color
        )

    def _draw_wall_n(self, surface, pixels, box_col, box_row) -> None:
        origin_x = self._box_px(box_col) + self.wall_thikness
        origin_y = self._box_py(box_row)
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            (self.box_size - (2 * self.wall_thikness)),
            self.wall_thikness,
            self.color_wall,
        )

    def _draw_wall_s(self, surface, pixels, box_col, box_row) -> None:
        origin_x = self._box_px(box_col) + self.wall_thikness
        origin_y = self._box_py(box_row) + (self.box_size - self.wall_thikness)
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            (self.box_size - (2 * self.wall_thikness)),
            self.wall_thikness,
            self.color_wall,
        )

    def _draw_wall_e(self, surface, pixels, box_col, box_row) -> None:
        origin_x = self._box_px(box_col) + (self.box_size - self.wall_thikness)
        origin_y = self._box_py(box_row) + self.wall_thikness
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            self.wall_thikness,
            (self.box_size - (2 * self.wall_thikness)),
            self.color_wall,
        )

    def _draw_wall_w(self, surface, pixels, box_col, box_row) -> None:
        origin_x = self._box_px(box_col)
        origin_y = self._box_py(box_row) + self.wall_thikness
        self._draw_rectangle(
            surface,
            pixels,
            origin_x,
            origin_y,
            self.wall_thikness,
            (self.box_size - (2 * self.wall_thikness)),
            self.color_wall,
        )

    def _draw_box_walls(
        self, surface, pixels, box_col, box_row, bitmask
    ) -> None:
        WALL_N = 1
        WALL_E = 2
        WALL_S = 4
        WALL_W = 8
        if bitmask & WALL_W:
            self._draw_wall_w(surface, pixels, box_col, box_row)
        if bitmask & WALL_S:
            self._draw_wall_s(surface, pixels, box_col, box_row)
        if bitmask & WALL_E:
            self._draw_wall_e(surface, pixels, box_col, box_row)
        if bitmask & WALL_N:
            self._draw_wall_n(surface, pixels, box_col, box_row)

    def _draw_rectangle(self, surface, pixels, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                if (
                    0 <= i < surface.get_width()
                    and 0 <= j < surface.get_height()
                ):
                    pixels[i, j] = color

    def _draw_circle(
        self,
        surface,
        pixels,
        center_x: int,
        center_y: int,
        radius: int,
        color: tuple[int, int, int],
    ) -> None:
        for x in range(center_x - radius, center_x + radius + 1):
            for y in range(center_y - radius, center_y + radius + 1):
                if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius**2:
                    if (
                        0 <= x < surface.get_width()
                        and 0 <= y < surface.get_height()
                    ):
                        pixels[x, y] = color

    def create_static_background(self, maze_grid: list[list[int]]) -> None:
        pixels = pygame.PixelArray(self.background_surface)
        for row in range(len(maze_grid)):
            for col in range(len(maze_grid[row])):
                color_box = (0, 0, 0)
                if maze_grid[row][col] == 15:
                    color_box = (255, 0, 0)
                self._draw_box(
                    self.background_surface, pixels, col, row, color_box
                )
                self._draw_box_walls(
                    self.background_surface,
                    pixels,
                    col,
                    row,
                    maze_grid[row][col],
                )
        pixels.close()

    def render_frame(self, engine) -> None:
        self.screen.blit(self.background_surface, (0, 0))
        pixels = pygame.PixelArray(self.screen)
        for row in range(len(engine.pac_gum.pac_gum)):
            for col in range(len(engine.pac_gum.pac_gum[row])):
                if engine.pac_gum.pac_gum[row][col] == 1:
                    x = self._box_px(col) + (self.box_size // 2)
                    y = self._box_py(row) + (self.box_size // 2)
                    self._draw_circle(
                        self.screen,
                        pixels,
                        x,
                        y,
                        self.pacgum_radius,
                        self.color_pacgum,
                    )
        player_col, player_row = engine.player.pos
        px_x = self._box_px(player_col) + self.wall_thikness + 2
        px_y = self._box_py(player_row) + self.wall_thikness + 2
        player_size = self.box_size - (2 * self.wall_thikness) - 4
        self._draw_rectangle(
            self.screen,
            pixels,
            px_x,
            px_y,
            player_size,
            player_size,
            self.color_player,
        )
        pixels.close()
        pygame.display.flip()
