from __future__ import annotations

from pydantic import BaseModel, ValidationError


class GameConfig(BaseModel):
    # gameplay
    highscore_filename: str = "highscores.json"
    seed: int = 42
    level_max_time: int = 90
    pacgum: int = 40
    lives: int = 3
    point_per_pacgum: int = 10
    point_per_super_pacgum: int = 50
    point_per_ghost: int = 200
    player_speed: int | float = 4

    # affichage
    m_height: int = 30
    m_width: int = 30
    box_size: int = 20
    wall_thikness: int = 1
    padding: int = 1
    top_offset: int = 90 + (box_size * padding)
    pacgum_radius: int = 4

    # colors
    color_player: tuple[int, int, int] = (255, 255, 0)
    color_wall: tuple[int, int, int] = (33, 50, 197)
    color_pacgum: tuple[int, int, int] = (255, 184, 255)

    @staticmethod
    def load_config(filepath: str) -> GameConfig:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                clean_line = [
                    line
                    for line in f.readlines()
                    if not line.strip().startswith("#")
                ]
                clean_json_string = "".join(clean_line)

            return GameConfig.model_validate_json(clean_json_string)
        except (FileNotFoundError, ValidationError) as e:
            print(f"[ERROR]: {e}\nUsing default value!")
            return GameConfig()
