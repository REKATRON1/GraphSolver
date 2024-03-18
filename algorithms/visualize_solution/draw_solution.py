import pygame as pg

from algorithms.info import SolutionInfo
from ui import Screen, UIPoints
from utility import Point, GraphAnalysis, interpolate_tuple

def draw_solution(screen: Screen, solution_info: SolutionInfo) -> None:
    projected_points = UIPoints(solution_info.points).get_points_on_plane(screen)
    for start, end in solution_info.solution:
        p1, p2 = solution_info.points[start], solution_info.points[end]
        avg_distance = (GraphAnalysis.distance(p1, screen.get_position()) + GraphAnalysis.distance(p2, screen.get_position()))/2
        color = interpolate_tuple((0,255,0),(0,0,0),(avg_distance-500)/1000)
        projected1, projected2 = projected_points[start], projected_points[end]
        pg.draw.line(screen.main_screen, color, projected1, projected2, 1)