from config import GameConfig
import pygame
from mazegenerator import MazeGenerator
from pac_gum import PacGum
from player import Player
from renderer import Renderer


class Engine:
    def __init__(self, config: GameConfig) -> None:
        self.maze_gen = MazeGenerator((config.height, config.width))
        self.renderer = Renderer(config)
        self.player = Player(self.maze_gen, (0, 0))
        self.pac_gum = PacGum(self.maze_gen)
        self.running = True

    def move_handler(self, keycode: int) -> int:
        """
        Gère les entrées clavier pour bouger le joueur.
        """
        col, row = self.player.pos
        next_col, next_row = col, row

        match keycode:
            case pygame.K_w | pygame.K_UP:
                next_row -= 1  # Haut = on monte dans les lignes (Y)
            case pygame.K_s | pygame.K_DOWN:
                next_row += 1  # Bas = on descend dans les lignes (Y)
            case pygame.K_a | pygame.K_LEFT:
                next_col -= 1  # Gauche = on diminue les colonnes (X)
            case pygame.K_d | pygame.K_RIGHT:
                next_col += 1  # Droite = on augmente les colonnes (X)
        if (next_col, next_row) == (col, row):
            return 1
        if self.player.move((col, row), (next_col, next_row)):
            return 0
        return 0

    def run(self):
        self.renderer.create_static_background(self.maze_gen.maze)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self.running = False
                if (
                    event.type == pygame.KEYDOWN
                    and self.move_handler(event.key) == 0
                ):
                    col, row = self.player.pos
                    if self.pac_gum.pac_gum[row][col] == 1:
                        self.pac_gum.pac_gum[row][col] = 0
                        self.player.score += self.pac_gum.value
                        print(self.player.score)

            self.renderer.render_frame(self)
        pygame.quit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
