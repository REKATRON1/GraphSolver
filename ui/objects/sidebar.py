import pygame as pg

import math
from enum import Enum
from dataclasses import dataclass

from .ui_object import UIObject, UICreateInfo, UIRequestCreateInfo, AlignmentMode
from .text import UIText, TextCreateInfo, TextRequestCreateInfo
from .button import UIButton, ButtonCreateInfo, ButtonRequestCreateInfo, ButtonType, UIButton, ButtonFunctionality
from utility import iVector2

class HeaderType(Enum):
    Default = 0
    Hidden = 1

@dataclass
class Header:
    text: str
    header_type: HeaderType=HeaderType.Default

class FooterType(Enum):
    Default = 0
    Hidden = 1

@dataclass
class Footer:
    text: str
    footer_type: FooterType = FooterType.Default

@dataclass
class LayoutGroupCreateInfo:
    objects: list[UIRequestCreateInfo]
    header: Header = None
    footer: Footer = None

@dataclass
class LayoutGroup:
    objects: list[UIObject]
    buttons: list[UIButton]
    header: Header = None
    footer: Footer = None

@dataclass
class SideLayout:
    groups: list[LayoutGroup]

@dataclass
class SidebarCreateInfo(UICreateInfo):
    alignment_mode: AlignmentMode
    size: int
    layouts: list[SideLayout]
    header: Header = None
    footer: Footer = None

class UISidebar(UIObject):
    def __init__(self, wrapping_box: pg.Rect, sidebar_create_info: SidebarCreateInfo) -> None:
        self.enabled = True
        
        self.size: int = sidebar_create_info.size
        self.alignment_mode: AlignmentMode = sidebar_create_info.alignment_mode

        self.side_layouts: list[SideLayout] = sidebar_create_info.layouts
        self.header: Header = sidebar_create_info.header
        self.footer: Footer = sidebar_create_info.footer

        self.active_side = 0

        self.rect = None
        self.update(wrapping_box)

    @staticmethod
    def create(wrapping_box: pg.Rect, alignment_mode: AlignmentMode, size: int, contained_object_groups: list[LayoutGroupCreateInfo], header: Header=None, footer: Footer=None):
        from ui import Screen, main_font
        sidebar_rect = pg.Rect((0,0),(0,0))
        match alignment_mode:
            case AlignmentMode.Left:
                sidebar_rect = pg.Rect(wrapping_box.topleft, (size, wrapping_box.height))
            case AlignmentMode.Right:
                sidebar_rect = pg.Rect(wrapping_box.topleft, (size, wrapping_box.height))
                sidebar_rect.right = wrapping_box.right

        start_height = sidebar_rect.top
        if header != None:
            start_height += 1.5*main_font.render(header.text, False, "white").get_rect().height
        max_height = sidebar_rect.bottom
        if footer != None:
            max_height -= 1.5*main_font.render(footer.text, False, "white").get_rect().height

        all_side_layouts: list[SideLayout] = []

        def create_layout_group(object_group: LayoutGroupCreateInfo, start_height: int, max_height: int) -> tuple[bool, LayoutGroup, int]:
            from ui import main_font
            all_objects: list[UIObject] = []
            all_buttons: list[UIButton] = []

            object_group_start_height = start_height
            if object_group.header != None:
                object_group_start_height += 1.5*main_font.render(object_group.header.text, False, "white").get_rect().height
            object_group_max_height = max_height
            if object_group.footer != None:
                object_group_max_height -= 1.5*main_font.render(object_group.footer.text, False, "white").get_rect().height

            object_group_current_height = object_group_start_height
            group_to_high = False
            for requested_ui_object in object_group.objects:
                match requested_ui_object:
                    case TextRequestCreateInfo() as text_create_request:
                        new_text = UIText(text_create_request.text, pg.Rect(sidebar_rect.left, object_group_current_height, size, math.inf), AlignmentMode.Top)
                        all_objects.append(new_text)
                        object_group_current_height += new_text.rect.height
                    case ButtonRequestCreateInfo() as button_create_request:
                        new_button = UIButton(ButtonCreateInfo(button_create_request.texts, button_create_request.referencing_functionality_tag,
                                        pg.Rect(sidebar_rect.left, object_group_current_height, size, math.inf), 
                                        AlignmentMode.Top, (size, None), button_create_request.button_type, button_create_request.numeric_alignment))
                        all_objects.append(new_button)
                        all_buttons.append(new_button)
                        object_group_current_height += new_button.rect.height
                
                if object_group_current_height > object_group_max_height:
                    return True, None, start_height
            if object_group.footer != None: 
                return False, LayoutGroup(all_objects, all_buttons, object_group.header, object_group.footer), object_group_current_height+1.5*main_font.render(object_group.footer.text, False, "white").get_rect().height
            else:
                return False, LayoutGroup(all_objects, all_buttons, object_group.header, object_group.footer), object_group_current_height

        current_side_layout: list[LayoutGroup] = []
        current_height = start_height
        min_height = True
        for object_group in contained_object_groups:
            group_to_high, new_layout_group, current_height = create_layout_group(object_group, current_height, max_height)
            if group_to_high and min_height:
                print('Sidebar too small')
                continue
            elif group_to_high:
                prev_current_height = current_height
                current_height = start_height
                group_to_high, new_layout_group, current_height = create_layout_group(object_group, current_height, max_height)
                if group_to_high:
                    print('Sidebar too small')
                    current_height = prev_current_height
                    continue
                else:
                    all_side_layouts.append(SideLayout(current_side_layout))
                    current_side_layout = [new_layout_group]
            else:
                current_side_layout.append(new_layout_group)
            min_height = False
        
        all_side_layouts.append(SideLayout(current_side_layout))
    
        return UISidebar(wrapping_box, SidebarCreateInfo(alignment_mode, size, all_side_layouts, header, footer))

    def get_enabled_buttons(self) -> list[tuple[pg.Rect, str, UIButton]]:
        if len(self.side_layouts) == 0 or len(self.side_layouts) < self.active_side:
            return
        side: SideLayout = self.side_layouts[self.active_side]
        all_buttons: list[tuple[pg.Rect, str, UIButton]] = []
        for layout_group in side.groups:
            if len(layout_group.objects) == 0:
                continue
            for ui_object in layout_group.objects:
                match ui_object:
                    case UIButton() as button:
                        if button.enabled:
                            all_buttons.extend(button.get_buttons())
        return all_buttons

    def draw(self, screen) -> None:
        from ui import main_font, Screen
        
        #temporary!
        #self.update(pg.Rect((0,0),(screen.size)))

        match self.alignment_mode:
            case AlignmentMode.Left:
                pg.draw.line(screen.main_screen, "white", self.rect.topright, self.rect.bottomright)
            case AlignmentMode.Right:
                pg.draw.line(screen.main_screen, "white", self.rect.topleft, self.rect.bottomleft)
        if self.rect.top > 0:
            pg.draw.line(screen.main_screen, "white", self.rect.topleft, self.rect.topright)
        if self.rect.bottom < screen.size[1]:
            pg.draw.line(screen.main_screen, "white", self.rect.bottomleft, self.rect.bottomright)

        if self.header != None:
            header_surface = main_font.render(self.header.text, False, "white")
            header_rect = header_surface.get_rect()
            header_rect.centerx = self.rect.centerx
            header_rect.top = self.rect.top
            match self.header.header_type:
                case HeaderType.Default:
                    screen.main_screen.blit(header_surface, header_rect)
                    header_rect.width = min(self.size, 1.5*header_rect.width)
                    header_rect.centerx = self.rect.centerx
                    pg.draw.line(screen.main_screen, "white", header_rect.bottomleft, header_rect.bottomright)
                case HeaderType.Hidden:
                    header_rect.width = 2/3*self.size
                    header_rect.centerx = self.rect.centerx
                    pg.draw.line(screen.main_screen, "white", header_rect.bottomleft, header_rect.bottomright)
        if self.footer != None:
            footer_surface = main_font.render(self.footer.text, False, "white")
            footer_rect = footer_surface.get_rect()
            footer_rect.centerx = self.rect.centerx
            footer_rect.bottom = self.rect.bottom
            match self.footer.footer_type:
                case FooterType.Default:
                    screen.main_screen.blit(footer_surface, footer_rect)
                    footer_rect.width = min(self.size, footer_rect.width*1.5)
                    footer_rect.centerx = self.rect.centerx
                    pg.draw.line(screen.main_screen, "white", footer_rect.topleft, footer_rect.topright)
                case FooterType.Hidden:
                    footer_rect.width = 2/3*self.size
                    footer_rect.centerx = self.rect.centerx
                    pg.draw.line(screen.main_screen, "white", footer_rect.topleft, footer_rect.topright)

        if len(self.side_layouts) == 0 or len(self.side_layouts) < self.active_side:
            return
        
        side: SideLayout = self.side_layouts[self.active_side]
        for layout_group in side.groups:
            if len(layout_group.objects) == 0:
                continue
            
            if layout_group.header != None:
                first_object: UIObject = layout_group.objects[0]
                header_surface = main_font.render(layout_group.header.text, False, "white")
                header_rect = header_surface.get_rect()
                header_rect.centerx = self.rect.centerx
                header_rect.bottom = first_object.rect.top - .5*header_rect.height
                match layout_group.header.header_type:
                    case HeaderType.Default:
                        screen.main_screen.blit(header_surface, header_rect)
                        header_rect.width = min(self.size, 1.5*header_rect.width)
                        header_rect.centerx = self.rect.centerx
                        pg.draw.line(screen.main_screen, "white", header_rect.bottomleft, header_rect.bottomright)
                    case HeaderType.Hidden:
                        header_rect.width = 2/3*self.size
                        header_rect.centerx = self.rect.centerx
                        pg.draw.line(screen.main_screen, "white", header_rect.bottomleft, header_rect.bottomright)

            for ui_object in layout_group.objects:
                ui_object.draw(screen)

            if layout_group.footer != None:
                last_object: UIObject = layout_group.objects[-1]
                footer_surface = main_font.render(layout_group.footer.text, False, "white")
                footer_rect = footer_surface.get_rect()
                footer_rect.centerx = self.rect.centerx
                footer_rect.top = last_object.rect.bottom + .5*footer_rect.height
                match layout_group.footer.footer_type:
                    case FooterType.Default:
                        screen.main_screen.blit(footer_surface, footer_rect)
                        footer_rect.width = min(self.size, 1.5*footer_rect.width)
                        footer_rect.centerx = self.rect.centerx
                        pg.draw.line(screen.main_screen, "white", footer_rect.topleft, footer_rect.topright)
                    case FooterType.Hidden:
                        footer_rect.width = 2/3*self.size
                        footer_rect.centerx = self.rect.centerx
                        pg.draw.line(screen.main_screen, "white", footer_rect.topleft, footer_rect.topright)

    def update(self, wrapping_box: pg.Rect):
        sidebar_rect = pg.Rect((0,0),(0,0))
        match self.alignment_mode:
            case AlignmentMode.Left:
                sidebar_rect = pg.Rect(wrapping_box.topleft, (self.size, wrapping_box.height))
            case AlignmentMode.Right:
                sidebar_rect = pg.Rect(wrapping_box.topleft, (self.size, wrapping_box.height))
                sidebar_rect.right = wrapping_box.right
        if self.rect == None:
            self.rect = sidebar_rect
            return
        right_shift = sidebar_rect.right - self.rect.right
        self.rect = sidebar_rect

        if len(self.side_layouts) == 0 or len(self.side_layouts) < self.active_side:
            return
        
        side: SideLayout = self.side_layouts[self.active_side]
        for layout_group in side.groups:
            if len(layout_group.objects) == 0:
                continue
            
            for ui_object in layout_group.objects:
                ui_object.move(right_shift, 0)