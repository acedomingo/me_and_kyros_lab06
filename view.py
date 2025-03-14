import pyxel
from collections.abc import Sequence
 
from project_types import UpdateHandler, DrawHandler, PlatformInfo, EggInfo
 
 
class View:
    def __init__(self, width: int, height: int, fps: int):
        self._width = width
        self._height = height
        self._fps = fps
 
    def start(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._width, self._height)
        pyxel.run(update_handler.update, draw_handler.draw)
 
    def was_spacebar_just_pressed(self):
        return pyxel.btnp(pyxel.KEY_SPACE)
 
    def clear_screen(self):
        pyxel.cls(0)
 
    def draw_platform(self, platforms: Sequence[PlatformInfo]):
        for p in platforms:
            rect = p.platform
            pyxel.rect(rect.x, rect.y, rect.width, rect.height, 4)
 
 
    def draw_egg(self, egg: EggInfo):
        pyxel.circ(egg.x, egg.y, egg.radius, 10)
        pyxel.circb(egg.x, egg.y, egg.radius, 7)
 
    def draw_score(self, score: int):
        pyxel.text(self._width // 2 - 3, 10, str(score), 7)
 
    def draw_game_over(self):
        pyxel.text(self._width // 2 - 15, self._height // 2, "Game over", 7)