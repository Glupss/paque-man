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
                    return
