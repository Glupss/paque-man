from config import GameConfig
from mazegenerator import MazeGenerator
from pac_gum import PacGum
from player import Player
from renderer import Renderer
from ghosts import Blinky, Inky, Pinky, Clyde
from menu import Menu

import pygame
import math


class Engine:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.maze_gen = MazeGenerator((config.m_width, config.m_height))
        self.maze_grid = self.maze_gen.maze
        self.renderer = Renderer(config)
        self.menu = Menu()
        # Start pos Pacman
        start_col, start_row = self._get_spawn_point()
        self.player = Player(self.maze_grid, start_row, start_col, config)

        # init ghost
        blinky = Blinky(self.maze_grid, 0, 0, self.player, config)
        self.ghosts = [
            blinky,
            Inky(
                self.maze_grid,
                self.player,
                0,
                (len(self.maze_grid[0]) - 1),
                config,
                blinky,
            ),
            Pinky(
                self.maze_grid,
                len(self.maze_grid[0]),
                0,
                self.player,
                config,
            ),
            Clyde(
                self.maze_grid,
                len(self.maze_grid[0]),
                (len(self.maze_grid[0]) - 1),
                self.player,
                config,
            ),
        ]

        self.pac_gum = PacGum(self.maze_grid, config, start_row, start_col)
        self.running = True

        # init timer and chrono
        self.start_ticks = pygame.time.get_ticks()
        self.time_limit = config.time_limit
        self.time_left = self.time_limit
        self.flee_timer = 0

    def _get_spawn_point(self) -> tuple[int, int]:
        center_col = self.config.m_width // 2
        center_row = self.config.m_height // 2

        for radius in range(self.config.m_width):
            for r in range(center_row - radius, center_row + radius + 1):
                for c in range(center_col - radius, center_col + radius + 1):
                    if (
                        0 <= r < self.config.m_height
                        and 0 <= c < self.config.m_width
                    ):
                        if self.maze_grid[r][c] != 15:
                            return c, r
        return center_col, center_row

    def _reset_all_pos(self) -> None:
        self.player.reset_pos()
        for ghost in self.ghosts:
            ghost.reset_pos()

    def change_direction(self, keycode: int) -> None:
        """
        Gère les entrées clavier pour bouger le joueur
        """

        match keycode:
            case pygame.K_w | pygame.K_UP:
                # Haut = on monte dans les lignes (Y)
                self.player.next_dir = (0, -1)
            case pygame.K_s | pygame.K_DOWN:
                # Bas = on descend dans les lignes (Y)
                self.player.next_dir = (0, 1)
            case pygame.K_a | pygame.K_LEFT:
                # Gauche = on diminue les colonnes (X)
                self.player.next_dir = (-1, 0)
            case pygame.K_d | pygame.K_RIGHT:
                # Droite = on augmente les colonnes (X)
                self.player.next_dir = (1, 0)

    def _eat_pacgums(self) -> None:
        row, col = self.player.get_grid_pos()
        val = self.pac_gum.pac_gum[row][col]

        if val == 1:
            self.pac_gum.pac_gum[row][col] = 0
            self.player.score += self.pac_gum.value
            print(f"Score: {self.player.score}")
        elif val == 2:
            self.pac_gum.pac_gum[row][col] = 0
            self.player.score += self.pac_gum.super_value

            # Flee behaviour
            self.flee_timer = pygame.time.get_ticks()
            for ghost in self.ghosts:
                ghost.flee = True
            print(f"Score: {self.player.score}")

    def _check_collisions(self) -> None:
        threshold = self.config.box_size // 2

        for ghost in self.ghosts:
            distance = math.dist(
                (self.player.x, self.player.y), (ghost.x, ghost.y)
            )
            if distance < threshold:
                if ghost.flee:
                    self.player.score += self.config.point_per_ghost
                    ghost.reset_pos()
                else:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.running = False
                        print("Game Over")
                    else:
                        self._reset_all_pos()
                    break

    def run(self):
        self.renderer.create_static_background(self.maze_grid)

        clock = pygame.time.Clock()

        if not self.menu.main_menu(self.renderer, self):
            self.running = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.menu.pause(self.renderer, self):
                            self.running = False
                    elif event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        for ghost in self.ghosts:
                            ghost.flee = not ghost.flee
                    elif event.key == pygame.K_r:
                        for ghost in self.ghosts:
                            ghost.reset_pos()
                    else:
                        self.change_direction(event.key)

            if self.flee_timer > 0:
                if pygame.time.get_ticks() - self.flee_timer > 10000:
                    self.flee_timer = 0
                    for ghost in self.ghosts:
                        ghost.flee = False

            # update player & ghost
            self.player.update()

            for ghost in self.ghosts:
                ghost.chose_target()
                ghost.move_to_target()

            sec_passed = (pygame.time.get_ticks() - self.start_ticks) // 1000
            self.time_left = max(0, self.time_limit - sec_passed)
            if self.time_left == 0:
                self.running = False

            self._eat_pacgums()
            self._check_collisions()

            self.renderer.render_frame(self)
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    pass
