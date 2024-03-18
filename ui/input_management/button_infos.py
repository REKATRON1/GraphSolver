
from dataclasses import dataclass

def apply_button_press(data, referencing_functionality_tag: str, clicked_button) -> None:
    idata: InputData = data.input_data
    vdata: VisualData = data.visual_data
    adata: AlgorithmusData = data.algo_data
    
    print(referencing_functionality_tag)
    
    button_info: list[str] = referencing_functionality_tag.split('_')
    do_switch = True
    match button_info:
        case 'solve', _:
            do_switch = False
            from algorithms import request_solution
            if adata != None and len(vdata.points) > 0:
                adata.algorithmus_setup.points = vdata.points[0].points
                adata.set_solution(request_solution(adata.algorithmus_setup))
        case '2d', _:
            from ui.screen import ProjectionStile
            vdata.screen.projection_stile = ProjectionStile.Perspective
            for ui_points in vdata.points:
                ui_points.add_random_z_offset()
        case '3d', _:
            from ui.screen import ProjectionStile
            vdata.screen.projection_stile = ProjectionStile.Orthogonal
            for ui_points in vdata.points:
                ui_points.set_z_to_zero()
            vdata.screen.rotation_x, vdata.screen.rotation_y = 0, 0
        case _:
            return

    def switch_button(clicked_button, button_postfix: str) -> None:
        match button_info[-1]:
            case 'inc':
                clicked_button.switch(1)
            case 'dec':
                clicked_button.switch(-1)
            case _:
                clicked_button.switch()
    if do_switch:
        switch_button(clicked_button, button_info[-1])