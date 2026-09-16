from config import GameConfig
import player
import pygame


class Renderer:
    def __init__(self, config: GameConfig) -> None:
        pygame.init()
        self.padding = config.padding
        self.top_offset = config.top_offset
        self.box_size = config.box_size
        self.wall_thikness = config.wall_thikness
        self.color_wall = config.color_wall
        self.color_player = config.color_player
        self.color_ghost = config.color_ghost
        self.color_pacgum = config.color_pacgum
        self.pacgum_radius = config.pacgum_radius
        screen_w = (config.m_width + config.padding * 2) * config.box_size
        screen_h = (
            config.m_height + config.padding * 3
        ) * config.box_size + self.top_offset
        self.background_surface = pygame.Surface((screen_w, screen_h))
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        # Logo PacMan
        original_logo = pygame.image.load(
            "./assets/Pacman_logo.png"
        ).convert_alpha()
        target_width = int(screen_w * 0.4)
        ratio = original_logo.get_height() / original_logo.get_width()
        target_height = int(target_width * ratio)
        self.logo = pygame.transform.smoothscale(
            original_logo, (target_width, target_height)
        )
        # pacman sprite
        player_size = self.box_size - (2 * self.wall_thikness) - 4

        def load_and_scale(filepath):
            img = pygame.image.load(filepath).convert_alpha()
            return pygame.transform.smoothscale(
                img, (player_size, player_size)
            )

        self.pacman_sprites = {
            "RIGHT": [
                load_and_scale("assets/img_right_0.png"),
                load_and_scale("assets/img_right_1.png"),
                load_and_scale("assets/img_right_2.png"),
            ],
            "LEFT": [
                load_and_scale("assets/img_left_0.png"),
                load_and_scale("assets/img_left_1.png"),
                load_and_scale("assets/img_left_2.png"),
            ],
            "UP": [
                load_and_scale("assets/img_up_0.png"),
                load_and_scale("assets/img_up_1.png"),
                load_and_scale("assets/img_up_2.png"),
            ],
            "DOWN": [
                load_and_scale("assets/img_down_0.png"),
                load_and_scale("assets/img_down_1.png"),
                load_and_scale("assets/img_down_2.png"),
            ],
        }
        self.ghost_sprites = [
            load_and_scale("assets/ghost1.png"),
            load_and_scale("assets/ghost2.png"),
            load_and_scale("assets/ghost3.png"),
            load_and_scale("assets/ghost4.png"),
        ]

    def _box_px(self, box_col: int) -> int:
        return (box_col + self.padding) * self.box_size

    def _box_py(self, box_row: int) -> int:
        return (box_row + self.padding) * self.box_size + self.top_offset

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
        logo_rect = self.logo.get_rect()
        logo_rect.centerx = self.background_surface.get_width() // 2
        logo_rect.y = self.padding * self.box_size
        self.background_surface.blit(self.logo, logo_rect)

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
        # ---Player render---
        center_x = engine.player.x
        center_y = engine.player.y
        player_size = self.box_size - (2 * self.wall_thikness) - 4
        top_left_x = int(center_x - (player_size // 2))
        top_left_y = int(center_y - (player_size // 2))

        progress = (engine.player.x + engine.player.y) % self.box_size
        cycle_step = int((progress / self.box_size) * 4)

        match cycle_step:
            case 0:
                frame_index = 0  # close
            case 1:
                frame_index = 1  # opening
            case 2:
                frame_index = 2  # big mouth
            case 3:
                frame_index = 1  # opening/closing

        dx, dy = engine.player.dir
        if dx == 0 and dy == 0:
            dx, dy = engine.player.next_dir

        direction_str = "RIGHT"
        if dx == 1:
            direction_str = "RIGHT"
        elif dx == -1:
            direction_str = "LEFT"
        elif dy == 1:
            direction_str = "DOWN"
        elif dy == -1:
            direction_str = "UP"

        sprite = self.pacman_sprites[direction_str][frame_index]

        """self._draw_rectangle(
            self.screen,
            pixels,
            top_left_x,
            top_left_y,
            player_size,
            player_size,
            self.color_player,
        )"""
        tl_x = []
        tl_y = []
        sprites = []
        count = 0
        for ghost in engine.ghosts:
            ghost_col, ghost_row = ghost.x, ghost.y
            tl_x.append(int(ghost_col - (player_size // 2)))
            tl_y.append(int(ghost_row - (player_size // 2)))
            sprites.append(self.ghost_sprites[count])
            """self._draw_circle(
                self.screen,
                pixels,
                color=self.color_player,
                center_x=int(ghost.target[0]),
                center_y=int(ghost.target[1]),
                radius=int(player_size / 2),
            )"""
            count += 1
        pixels.close()
        self.screen.blit(sprite, (top_left_x, top_left_y))
        for x in range(len(sprites)):
            self.screen.blit(sprites[x], (tl_x[x], tl_y[x]))
        pygame.display.flip()
