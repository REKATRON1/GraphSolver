import pygame as pg
import numpy as np

from enum import Enum

from utility import Vector2, Vector3, clamp

class ProjectionStile(Enum):
    Orthogonal = 0
    Perspective = 1

class Screen():
    def __init__(self) -> None:
        self.size = (1280, 720)
        self.main_screen = pg.display.set_mode(self.size, pg.RESIZABLE)
        self.fullscreen = False
        self.zoom = 1
        self.projection_stile = ProjectionStile.Orthogonal

        self.radius = 1000
        self.rotation_x = 0
        self.rotation_y = 0
    def get_position(self) -> Vector3:
        from projection import Projection
        return Projection.position_from_rotation(self.rotation_x, self.rotation_y, self.radius)
    def get_forward(self) -> Vector3:
        from projection import Projection
        return Projection.direction_from_rotation(self.rotation_x, self.rotation_y)
    def get_up(self) -> Vector3:
        from projection import Projection
        return Projection.up_from_rotation(self.rotation_x, self.rotation_y)
    
    def zoom_in(self) -> None:
        self.zoom *= 1.1
    def zoom_out(self) -> None:
        self.zoom /= 1.1

    def switch_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.main_screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
        else:
            self.main_screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)

    def switch_projection_stile(self) -> None:
        if self.projection_stile == ProjectionStile.Orthogonal:
            self.projection_stile = ProjectionStile.Perspective
        else:
            self.projection_stile = ProjectionStile.Orthogonal

    def update(self):
        """updates screen"""
        self.update_attributes()
        self.main_screen.fill("black")

    def update_attributes(self) -> None:
        self.size = self.main_screen.get_width(), self.main_screen.get_height()

    def rotate(self, x:float=0, y:float=0) -> None:
        self.rotation_x = clamp(self.rotation_x + x, -np.pi/4, np.pi/4)
        self.rotation_y += y
        while self.rotation_y < 0:
            self.rotation_y += 2*np.pi
        while self.rotation_y >= 2*np.pi:
            self.rotation_y -= 2*np.pi