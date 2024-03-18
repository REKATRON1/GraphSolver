import pygame as pg

from runtime_stats import InputData
from ui import KeyInfo, KeyFunctionality

def get_main_key_input_setup() -> InputData:
    key_infos: list[KeyInfo] = []
    key_infos.append(KeyInfo(pg.K_RETURN, KeyFunctionality.Run))
    key_infos.append(KeyInfo(pg.K_F11, KeyFunctionality.ChangeWindow))
    key_infos.append(KeyInfo(pg.K_o, KeyFunctionality.ChangeProjection))
    key_infos.extend([KeyInfo(pg.K_UP, KeyFunctionality.EditPoints, mode=1, amount=25), 
                        KeyInfo(pg.K_DOWN, KeyFunctionality.EditPoints, mode=0, amount=25)])
    return InputData(key_infos)

"""
class ButtonInfos():
    def __init__(self, buttons: list[Button]=None) -> None:
        self.buttons = buttons
    def get_button_names_from_active_mode(active_mode: ActiveMode) -> ButtonInfos:
        match active_mode:
            case ActiveMode.GraphSolve:
                buttons = []
                button_names = np.array([['Min Graph','Pathsolving','NaN'],
                                        ['Addbuid', 'Addbuild 2'],
                                        [],
                                        ['Inverse', 'Factor dst.', 'Min dst.', 'Avg dst.', '.5 & 1.5 Avg dst.', 'Min X', 'Min Y'],
                                        ['Animate', 'Looping'],
                                        ['Keep Relations', 'Include Scal.'],
                                        ['Solve']])
                for button_list, button_type in zip(button_names, list(ButtonType)):
                    for button_name in button_list:
                        if button_name in ['Min Graph', 'Addbuild', 'Min dst.']:
                            buttons.append(Button(button_name, button_type, True))
                        else:
                            buttons.append(Button(button_name, button_type, False))
                return ButtonInfos(buttons)
            case ActiveMode.PathSolve:
                button_names = np.array([['Min Graph','Pathsolving','NaN'],
                                        ['Brute Force', 'Closest PtP', 'Multi cPtP', 'Addbuid'],
										['Enable Tour', 'Intersect Optim.', 'No Acute Angles'],
                                        ['Inverse', 'Factor dst.', 'Min dst.', 'Avg dst.', '.5 & 1.5 Avg dst.', 'Min X', 'Min Y'],
                                        ['Animate', 'Looping'],
                                        ['Keep Relations', 'Include Scal.'],
                                        ['Solve']])
                for button_list, button_type in zip(button_names, list(ButtonType)):
                    for button_name in button_list:
                        if button_name in ['Pathsolving', 'Addbuild', 'Min dst.']:
                            buttons.append(Button(button_name, button_type, True))
                        else:
                            buttons.append(Button(button_name, button_type, False))
                return ButtonInfos(buttons)
        return ButtonInfos()
    def get_button_activity(button_name: str) -> bool:
        for button in self.buttons:
            if button.name == button_name:
                return button.is_active()
        return False
    def get_type_activity(button_type: ButtonType) -> list[bool]:
        type_activity = []
        for button in self.buttons:
            if button.type == button_type:
                type_activity.append(button.is_active())
        return type_activity
    def switch_button(button_name: str) -> None:
        for button in self.buttons:
            if button.name == button_name:
                button.switch()
                return
"""