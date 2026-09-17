import pygame
from renderer import Renderer


class Menu:
    def pause(self, renderer: Renderer, engine):
        while 1:
            renderer.show_pause_menu(engine)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def main_menu(self, renderer: Renderer):
        index = 0
        max_index = 2
        while 1:
            renderer.show_main_menu(index)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
                        case pygame.K_ESCAPE:
                            return
                        case pygame.K_RETURN:
                            self.chose_button(index)
                            return

    def chose_button(self, index: int):
        match index:
            case 0:
                return
            case 1:
                return
            case 2:
                pygame.quit()
