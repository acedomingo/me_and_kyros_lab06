from model import Model
from view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
 
    def start(self): 
        self._view.start(self, self)
 
    def update(self):
        self._model.update(self._view.was_spacebar_just_pressed())
 
    def draw(self):
        self._view.clear_screen()
 
        self._view.draw_platform(self._model._platforms)
        self._view.draw_egg(self._model._egg)
        self._view.draw_score(self._model.score)
        self._view.draw_lives(self._model._egg_lives)
 
        if self._model.is_game_over:
            if self._model._egg_lives <= 0:
                self._view.draw_game_over()
            if self._model._current_index > 4:
                self._view.draw_win()