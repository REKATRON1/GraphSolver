import numpy as np
import pygame as pg

from .ui_object import UIObject
from ui import Screen
from utility import Vector3, Vector2, Point, GraphAnalysis, interpolate_tuple
from projection import Projection

point_size = 3

def set_point_size(npoint_size: int) -> None:
    point_size = npoint_size


class UIPoints(UIObject):
    def __init__(self, points: list[Point]) -> None:
        self.enabled = True
        self.points = np.array(points)
    def get_points_on_plane(self, screen: Screen) -> list[Vector2]:
        if len(self.points) < 1 or len(self.points[0]) < 3:
            return self.points
        return Projection.project_points(self.points, screen)
    def draw(self, screen: Screen) -> None:
        for prev_point, proj_point in zip(self.points, self.get_points_on_plane(screen)):
            dst = GraphAnalysis.distance(prev_point, screen.get_position())
            interpolated_color = interpolate_tuple((255,0,0), (0,0,0), (dst-500)/1000)
            pg.draw.circle(screen.main_screen, interpolated_color, proj_point, point_size)
    def remove_points(self, amount: int) -> None:
        p_points = list(self.points)
        for _ in range(amount):
            if len(p_points) > 0:
                p_points.pop(-1)
        self.points = np.array(p_points)
    def add_points(self, points: list[Point]) -> None:
        p_points = list(self.points)
        p_points.extend(points)
        self.points = np.array(p_points)
    def clear(self) -> None:
        self.points = np.array([])
    def set_z_to_zero(self) -> None:
        for point in self.points:
            point[2] = 0
    def add_random_z_offset(self, range_min_max=(-250,250)) -> None:
        from random import random
        for point in self.points:
            point[2] = random()*(range_min_max[1]-range_min_max[0])+range_min_max[0]