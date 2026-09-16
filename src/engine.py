from config import GameConfig
import pygame
from mazegenerator import MazeGenerator
from pac_gum import PacGum
from player import Player
from renderer import Renderer
from ghosts import Blinky, Inky, Pinky, Clyde


class Engine:
    def __init__(self, config: GameConfig) -> None:
        self.maze_gen = MazeGenerator((config.m_height, config.m_width))
        self.renderer = Renderer(config)
        self.player = Player(self.maze_gen.maze, 0, 0, config)
        self.pac_gum = PacGum(self.maze_gen, config)
        blinky = Blinky(self.maze_gen, self.player, 9, 9, config)
        self.ghosts = [
            blinky,
            Inky(self.maze_gen, self.player, 13, 13, config, blinky),
            Pinky(self.maze_gen, self.player, 15, 15, config),
            Clyde(self.maze_gen, self.player, 5, 5, config, (15, 15)),
        ]
        self.running = True

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

    def run(self):
        self.renderer.create_static_background(self.maze_gen.maze)

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        for ghost in self.ghosts:
                            ghost.flee = not ghost.flee
                    else:
                        self.change_direction(event.key)
            self.player.update()
            col, row = self.player.get_grid_pos()
            for ghost in self.ghosts:
                ghost.chose_target()
                ghost.move_to_target()
            if self.pac_gum.pac_gum[row][col] == 1:
                self.pac_gum.pac_gum[row][col] = 0
                self.player.score += self.pac_gum.value
                print(self.player.score)

            self.renderer.render_frame(self)
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
