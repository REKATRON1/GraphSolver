import pygame as pg
import numpy as np

from .key_infos import KeyFunctionality, KeyInfo
from .button_infos import apply_button_press
from utility import Vector2

def update_data_from_key_inputs() -> bool:
    from runtime_stats import data, InputData, VisualData, AlgorithmusData
    idata: InputData = data.input_data
    vdata: VisualData = data.visual_data
    adata: AlgorithmusData = data.algo_data
    if not idata or not vdata:
        return
    for key_info in idata.get_all_key_infos():
        if pg.key.get_pressed()[key_info.key_code]:
            match key_info.key_functionality:
                case KeyFunctionality.EditPoints:
                    if key_info.mode == 0:
                        vdata.remove_points(key_info.amount)
                    else:
                        from ui.screen import ProjectionStile
                        from utility import generate_random_points
                        if vdata.screen.projection_stile == ProjectionStile.Orthogonal:
                            min_coords = (-250,-250,0)
                            max_coords = (250,250,0)
                            vdata.add_points(generate_random_points(key_info.amount, max_coords, min_coords))
                        elif vdata.screen.projection_stile == ProjectionStile.Perspective:
                            min_coords = (-250,-250,-250)
                            max_coords = (250,250,250)
                            vdata.add_points(generate_random_points(key_info.amount, max_coords, min_coords))
                case KeyFunctionality.Run:
                    from algorithms import request_solution
                    if adata != None and len(vdata.points) > 0:
                        adata.algorithmus_setup.points = vdata.points[0].points
                        adata.set_solution(request_solution(adata.algorithmus_setup))
                case KeyFunctionality.ChangeWindow:
                    vdata.screen.switch_fullscreen()
                case KeyFunctionality.ChangeProjection:
                    vdata.screen.switch_projection_stile()
            return True
    return False

def update_data_from_mousewheel_inputs(event: pg.event) -> bool:
    from runtime_stats import data, VisualData
    vdata: VisualData = data.visual_data
    if event.y > 0:
        vdata.screen.zoom_in()
    elif event.y < 0:
        vdata.screen.zoom_out()

def update_data_from_mousewheeldown():
    from runtime_stats import data, VisualData
    from update import update_info
    vdata: VisualData = data.visual_data
    if update_info.free_rotation_mode:
        new_mouse_pos = pg.mouse.get_pos()
        movX, movY = new_mouse_pos[0] - update_info.prev_mouse_pos[0], new_mouse_pos[1] - update_info.prev_mouse_pos[1]
        vdata.screen.rotate(movY/1800*np.pi, movX/1800*np.pi)
        update_info.prev_mouse_pos = new_mouse_pos
    else:
        update_info.free_rotation_mode = True
        update_info.prev_mouse_pos = pg.mouse.get_pos()

def update_data_from_mouse_input():
    from runtime_stats import data, VisualData
    from ui import UIButton, UISidebar
    vdata: VisualData = data.visual_data
    for button_rect, referencing_functionality_tag, button in vdata.get_all_enabled_buttons():
        if button_rect.collidepoint(pg.mouse.get_pos()):
            apply_button_press(data, referencing_functionality_tag, button)