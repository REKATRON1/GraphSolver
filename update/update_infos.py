
from dataclasses import dataclass

from utility import Vector2

@dataclass
class UpdateInfos:
    running = True

    tick_rate: float = 60
    delta_time: float = 0

    key_pressed: bool = False
    mouse_pressed: bool = False
    free_rotation_mode: bool = False
    prev_mouse_pos: Vector2 = (0,0)