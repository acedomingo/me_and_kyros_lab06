from dataclasses import dataclass
from collections.abc import Sequence
from project_types import Rectangle
import random


PLATFORM_GAP = 30
EGG_VY = -10
PLATFORM_VX = 2.5
PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 3


@dataclass
class Egg:
    x: float
    y: float
    vy: float
    vx: float
    jumping: bool = False
    radius: float = 8.0

    @property
    def top(self):
        return self.y - self.radius
 
    @property
    def bottom(self):
        return self.y + self.radius
 
    @property
    def left(self):
        return self.x - self.radius
 
    @property
    def right(self):
        return self.x + self.radius

@dataclass
class Platform:
    x: float
    y: float
    vx: float = 0
    to_right: bool = True


    @property
    def platform(self) -> Rectangle:
        return Rectangle(self.x, self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    
    @property
    def top(self) -> float:
        return self.y
    
    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + PLATFORM_WIDTH

class Model:
    def __init__(self, width: int, height: int, fps: int):
        self._width = width
        self._height = height
        self._fps = fps

        self._is_game_over: bool = False
        self._score: int = 0
        self._egg_lives: int = 10
        self._frame_count: int = 0
        self._platforms: list[Platform] = [Platform(random.randint(1, self._width - PLATFORM_WIDTH - 1), height -  (i * PLATFORM_GAP), 0)
                           for i in range(1, 6)]
        
        self._current_platform: Platform = self._platforms[0]
        self._current_index: int = 1
        self._egg = Egg((self._current_platform.right + self._current_platform.left) // 2, self._current_platform.top - 8.0, 0, 0)
        

    def update(self, was_spacebar_just_pressed: bool):
        """Should be called once per frame/tick."""
        egg = self._egg

        if self._current_index > 4:
            self._is_game_over = True
 
        if self._height <= egg.top or egg.bottom < 0:
            if self._egg_lives <= 0:
                self._is_game_over = True
            else:
                self._egg_lives -= 1
                egg.x = (self._current_platform.right + self._current_platform.left) // 2
                egg.y =  self._current_platform.top - 8.0
                egg.vx = self._current_platform.vx
                egg.vy = 0
                egg.jumping = False
 
        if self._is_game_over:
            return
 
        if was_spacebar_just_pressed:
            egg.jumping = True
            self._jump_frame = self._frame_count
            egg.vy = EGG_VY

        for platform in self._platforms:
            if platform.right + PLATFORM_VX >= self._width:
                platform.to_right = False
            if platform.left - PLATFORM_VX <= 0:
                platform.to_right = True

            if platform.to_right:
                platform.vx = PLATFORM_VX
                platform.x += platform.vx
            else:
                platform.vx = -PLATFORM_VX
                platform.x += platform.vx
    
        if egg.jumping:
            egg.vx = 0
            egg.vy += 1
            
            if self._is_in_collision(egg, self._platforms[self._current_index].platform) and egg.vy > 0:
                egg.jumping = False
                egg.vy = 0
                self._current_platform = self._platforms[self._current_index]
                self._current_index += 1
                self._score += 1
        else:
            egg.vy = 0
            egg.vx = self._current_platform.vx

        egg.x += egg.vx
        egg.y += egg.vy

        self._frame_count += 1
 
    def _is_in_collision(self, circle: Egg, rect: Rectangle) -> bool:
        # Left, right, or within?
        if circle.right < rect.left:
            test_x = rect.left
        elif circle.left > rect.right:
            test_x = rect.right
        else:
            test_x = circle.x
 
        # Up, down, or within?
        if circle.bottom < rect.top:
            test_y = rect.top
        elif circle.top > rect.bottom:
            test_y = rect.bottom
        else:
            test_y = circle.y
 
        dist = ((test_x - circle.x)**2 + (test_y - circle.y)**2)**0.5
 
        return dist < circle.radius
 
    @property
    def width(self):
        return self._width
 
    @property
    def height(self):
        return self._height
 
    @property
    def fps(self):
        return self._fps
 
    @property
    def platforms(self) -> Sequence[Platform]:
        return self._platforms
 
    @property
    def egg(self) -> Egg:
        return self._egg
 
    @property
    def score(self) -> int:
        return self._score
 
    @property
    def is_game_over(self) -> int:
        return self._is_game_over
        