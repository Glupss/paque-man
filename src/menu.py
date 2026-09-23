import pygame
from renderer import Renderer
import json


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
            renderer.show_text_interface(pause_txt, 36, -1)
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
                                if not self.show_highscore(renderer):
                                    return False
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
            renderer.show_text_interface(instructions, 36)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        renderer.clean()
                        return True
                    if event.key == pygame.K_q:
                        return False

    def show_highscore(self, renderer) -> bool:
        try:
            with open("highscores.json", "r") as f:
                scores = json.load(f)
        except Exception:
            scores = {}
        sorted_scores = dict(
            sorted(scores.items(), key=lambda item: item[1], reverse=True)[:10]
        )
        scores_final = ["HIGHSCORES", "", ""]
        tmp = [f"{n}:           {s}" for n, s in sorted_scores.items()]
        scores_final.extend(tmp)
        while 1:
            renderer.show_text_interface(scores_final, 36, -1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        renderer.clean()
                        return True
                    if event.key == pygame.K_q:
                        return False

    def add_score(self, renderer, score) -> str:
        pressed = [".", ".", "."]
        count = 0
        while 1:
            end_msg = [
                "GAME OVER",
                "",
                "",
                f"Score : {score}",
                "",
                "",
                "ENTER YOUR NAME:",
                "",
                "",
                f"{''.join(pressed)}",
            ]
            renderer.show_text_interface(end_msg, 48, -1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ""
                if event.type == pygame.KEYDOWN:
                    if count < 3:
                        key = pygame.key.name(event.key)
                        if len(key) == 1 and key.isalpha():
                            pressed[count] = pygame.key.name(
                                event.key
                            ).capitalize()
                            count += 1
                    else:
                        ret = "".join(pressed)
                        if event.key == pygame.K_ESCAPE:
                            return ret
                        if event.key == pygame.K_RETURN:
                            return ret
                        if event.key == pygame.K_q:
                            return ret

    def powers(self, renderer, engine) -> tuple[bool, bool, bool, bool]:
        index = 0
        max_index = 2
        inf_life = engine.inf_life
        inf_time = engine.inf_time
        inf_gum = engine.inf_gums
        while 1:
            powers_ = [
                "Powers:",
                "",
                f"[{'X' if inf_life else '_'}] INFINITE LIVES",
                "",
                f"[{'X' if inf_time else '_'}] INFINITE TIME",
                "",
                f"[{'X' if inf_gum else '_'}] PERMANENT SUPER PAC-GUM",
                "",
                "Press [ESCAPE] to resume",
            ]
            renderer.show_text_interface(powers_, 36, index * 2 + 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (False, inf_life, inf_time, inf_gum)
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
                            renderer.clean()
                            return (True, inf_life, inf_time, inf_gum)
                        case pygame.K_q:
                            return (False, inf_life, inf_time, inf_gum)
                        case pygame.K_RETURN:
                            if index == max_index:
                                inf_gum = not inf_gum
                            elif index == max_index - 1:
                                inf_time = not inf_time
                            elif index == max_index - 2:
                                inf_life = not inf_life

        return (False, False, False, False)
