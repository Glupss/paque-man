import pygame
from renderer import Renderer


class Menu:
    def pause(self, renderer: Renderer, engine) -> bool:
        pause_txt = [
            "Game Paused",
            "",
            "",
            f"Score: {engine.player.score}",
            "",
            "",
            "press [ESCAPE] to resume",
            "",
            "",
            "press [Q] to QUIT",
        ]
        while 1:
            renderer.show_text_interface(pause_txt, 36)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    if event.key == pygame.K_q:
                        return False

    def main_menu(self, renderer: Renderer, engine) -> bool:
        index = 0
        max_index = 3
        while 1:
            renderer.show_main_menu(index)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_w | pygame.K_UP:
                            if index == 0:
                                index = max_index
                            else:
                                index -= 1
                        case pygame.K_s | pygame.K_DOWN:
                            if index == max_index:
                                index = 0
                            else:
                                index += 1
                        case pygame.K_ESCAPE | pygame.K_q:
                            return False
                        case pygame.K_RETURN:
                            if index == max_index:
                                return False
                            elif index == max_index - 1:
                                if not self.show_instructions(renderer):
                                    return False
                            elif index == max_index - 2:
                                print("highscores")
                            else:
                                return True

    def show_instructions(self, renderer) -> bool:
        while 1:
            instructions = [
                "Instructions:",
                "",
                "Collect all Pac-Gums to win",
                "",
                "If a ghost eats you the game ends",
                "",
                "Eat a Mega-Gum to eat the ghosts",
                "",
                "Use WASD or ARROWS to move",
            ]
            renderer.show_text_interface(instructions, 24)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        renderer.clean()
                        return True
                    if event.key == pygame.K_q:
                        return False
