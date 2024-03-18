import pygame as pg

from dataclasses import dataclass

from runtime_stats import VisualData
from ui import UISidebar, LayoutGroupCreateInfo, ButtonRequestCreateInfo, Header, HeaderType, Footer, FooterType
from ui import Screen, UIObject, UIPoints, UIButton, ButtonType, ButtonCreateInfo, AlignmentMode, NumericAlignment, TextRequestCreateInfo

def get_main_visual_setup() -> VisualData:
    all_objects: list[UIObject] = []
    points = [(-250,-250,-250),(-250,-250,250),(-250,250,-250),(-250,250,250),(250,-250,-250),(250,-250,250),(250,250,-250),(250,250,250),
							(-250,-250,0),(-250,250,0),(250,-250,0),(250,250,0),(-250,0,-250),(-250,0,250),(250,0,-250),(250,0,250),(0,-250,-250),(0,-250,250),(0,250,-250),(0,250,250)]
    points = []
    all_objects.append(UIPoints(points))
    all_objects.append(UIButton(ButtonCreateInfo(['Solve'], ['solve'],pg.Rect(0,0,500,500),AlignmentMode.Bottom)))
    all_objects.append(get_meta_sidebar())
    all_objects.append(get_right_sidebar())
    return VisualData(Screen(), all_objects)

def get_meta_sidebar() -> UISidebar:
    return UISidebar.create(pg.Rect((0,0),(500,500)), AlignmentMode.Right, 200,
    [LayoutGroupCreateInfo([ButtonRequestCreateInfo(['2D', '3D'], ['2d', '3d'], ButtonType.Numeric, NumericAlignment.SideCenter)], Header('Mode'), Footer('', FooterType.Hidden))], Header('Meta Setup'), Footer('by Sven'))

def get_right_sidebar() -> UISidebar:
    return UISidebar.create(pg.Rect((0,0),(500,500)), AlignmentMode.Right, 200,
    [LayoutGroupCreateInfo([ButtonRequestCreateInfo(['Default', 'Closest PtP','Multi PtP','Addbuild'], ['algo_def', 'algo_ptp','algo_mptp','algo_add'], ButtonType.Numeric, NumericAlignment.SideCenter),
                            ButtonRequestCreateInfo(['Start'], ['start']),
                            TextRequestCreateInfo('Hello World')], Header('Algorithms'), Footer('', FooterType.Hidden))], Header('3D Pathsolving'), Footer('by Sven'))