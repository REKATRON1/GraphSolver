import pygame as pg

from utility import Point
from ui import UIObject, Screen, UIButton, UIPoints, UISidebar

class VisualData():
    def __init__(self, main_screen: Screen, ui_objects: list[UIObject]):
        self.all: list[UIObject] = []
        self.screen: Screen = main_screen
        self.buttons: list[UIButton] = []
        self.sidebars: list[UISidebar] = []
        self.points: list[UIPoints] = []
        for ui_object in ui_objects:
            self.all.append(ui_object)
            match ui_object:
                case UISidebar():
                    self.sidebars.append(ui_object)
                case UIButton():
                    self.buttons.append(ui_object)
                case UIPoints():
                    self.points.append(ui_object)

        self.active_ui_mode = 0
        for sidebar in self.sidebars:
            sidebar.enabled = False
        self.sidebars[self.active_ui_mode].enabled = True
    def get_all_enabled_buttons(self) -> list[tuple[pg.Rect, str, UIButton]]:
        all_enabled_buttons: list[tuple[pg.Rect, str, UIButton]] = []
        for button in self.buttons:
            if button.enabled:
                all_enabled_buttons.extend(button.get_buttons())
        for sidebar in self.sidebars:
            if sidebar.enabled:
                all_enabled_buttons.extend(sidebar.get_enabled_buttons())
        return all_enabled_buttons
    def get_all_UIObjects(self) -> list[UIObject]:
        return [ui_object for ui_object in self.all if ui_object.enabled]
    def add_points(self, points: list[UIPoints]) -> None:
        if len(self.points) > 0:
            self.points[0].add_points(points)
    def remove_points(self, amount: int) -> None:
        if len(self.points) > 0:
            self.points[0].remove_points(amount)
    def update(self) -> None:
        for sidebar in self.sidebars:
            sidebar.update(pg.Rect((0,0),self.screen.size))
        for button in self.buttons:
            button.update(pg.Rect((0,0),self.screen.size))