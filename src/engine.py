from drawing.draw_stuff import draw_player
from mazegenerator import MazeGenerator
from maze_renderer import MazeRenderer
from player import Player
import pygame


class Engine:
    def __init__(self, m_height: int = 20, m_width: int = 20) -> None:
        self.maze_gen = MazeGenerator((m_height, m_width))
        self.maze_renderer = MazeRenderer(self.maze_gen, 1, 20, 1)
        self.player = Player(self.maze_gen, (0, 0))
        self.running = True

    def key_handler(self, keycode: int) -> int:
        """
        Handle the key pressed on the keyboard
        Dispatch the action to the right fuction
        """
        row, col = self.player.pos
        next_row, next_col = row, col

        match keycode:
            case pygame.K_w | pygame.K_UP:
                next_col -= 1
            case pygame.K_s | pygame.K_DOWN:
                next_col += 1
            case pygame.K_a | pygame.K_LEFT:
                next_row -= 1
            case pygame.K_d | pygame.K_RIGHT:
                next_row += 1
        if (next_row, next_col) == (row, col):
            return 1
        if self.player.can_move((row, col), (next_row, next_col)):
            self.player.pos = (next_row, next_col)
        return 0

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode((1200, 800))
        screen.fill((0, 0, 0))

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
                    and self.key_handler(event.key) == 0
                ):
                    print(self.maze_gen.maze)
                    print(self.player.pos)
                self.maze_renderer.draw(screen)
                draw_player(screen, self.player.pos)
                pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
