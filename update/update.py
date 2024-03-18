import pygame as pg
import numpy as np

from .update_infos import UpdateInfos

fps_clock = pg.time.Clock()
update_info = UpdateInfos()

def update():
    update_info.delta_time = fps_clock.tick(update_info.tick_rate) / 1000
    
    from runtime_stats import data
    
    #Update Visuals
    if data.visual_data != None:
        update_visuals()
    
    #Get Key Inputs
    from ui.screen import ProjectionStile
    key_pressed = False
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                update_info.running = False
            case pg.KEYDOWN:
                key_pressed = True
                if not update_info.key and data.input_data != None:
                    update_key_inputs()
            case pg.MOUSEWHEEL:
                if data.visual_data.screen.projection_stile != ProjectionStile.Orthogonal:
                    update_mousewheel_inputs(event)
    if not key_pressed:
        update_info.key = False
    
    #Get Mouse Inputs
    if data.visual_data.screen.projection_stile != ProjectionStile.Orthogonal:
        if pg.mouse.get_pressed(num_buttons=3)[1]:
            update_rotation_from_mouse_movement()
        else:
            update_info.free_rotation_mode = False
    
    if pg.mouse.get_pressed(num_buttons=3)[0]:
        if not update_info.mouse_pressed:
            update_info.mouse_pressed = True
            update_left_click()
    else:
        update_info.mouse_pressed = False

def update_visuals():
    from runtime_stats import data
    vdata =  data.visual_data
    vdata.update()
    screen = vdata.screen
    from ui.screen import ProjectionStile
    if screen.projection_stile == ProjectionStile.Perspective:
        if not update_info.free_rotation_mode:
            screen.rotate(y=1/180*np.pi)
    screen.update()
    for ui_object in vdata.get_all_UIObjects():
        ui_object.draw(screen)

    adata = data.algo_data
    if adata.solution != None:
        from algorithms import draw_solution
        draw_solution(screen, adata.solution)

def update_key_inputs():
    from runtime_stats import data
    from ui import update_data_from_key_inputs
    update_info.button_pressed = update_data_from_key_inputs()

def update_mousewheel_inputs(event: pg.event):
    from ui import update_data_from_mousewheel_inputs
    update_data_from_mousewheel_inputs(event)

def update_rotation_from_mouse_movement():
    from ui import update_data_from_mousewheeldown
    update_data_from_mousewheeldown()

def update_left_click():
    from ui import update_data_from_mouse_input
    update_data_from_mouse_input()