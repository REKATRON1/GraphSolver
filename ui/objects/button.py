import pygame as pg

from dataclasses import dataclass
from enum import Enum

from utility import iVector2
from runtime_stats import data
from .ui_object import UIObject, UICreateInfo, UIRequestCreateInfo, AlignmentMode

left_switch_text = ' < '
right_switch_text = ' > '

class ButtonType(Enum):
    Default = 0
    Numeric = 1

class ButtonFunctionality(Enum):
    Switch = 0
    Increase = 1
    Decrease = 2

class NumericAlignment(Enum):
    BottomCenter = 0
    BottomSided = 1
    TopCenter = 2
    TopSided = 3

    SideTop = 5
    SideCenter = 6
    SideBottom = 7

@dataclass
class ButtonRequestCreateInfo(UIRequestCreateInfo):
    texts: list[str]
    referencing_functionality_tag: list[str]
    button_type: ButtonType=ButtonType.Default
    numeric_alignment: NumericAlignment=NumericAlignment.BottomSided

@dataclass
class ButtonCreateInfo(UICreateInfo):
    texts: list[str]
    referencing_functionality_tag: list[str]
    wrapping_box: pg.Rect
    alignment: AlignmentMode
    size: iVector2=(None, None)
    button_type: ButtonType=ButtonType.Default
    numeric_alignment: NumericAlignment=NumericAlignment.BottomSided

@dataclass
class Button:
    rect: pg.Rect
    button_type: ButtonFunctionality

class UIButton(UIObject):
    def __init__(self, button_create_info: ButtonCreateInfo, active: bool=False, value:int = 0) -> None:
        self.enabled = True
        
        if type(button_create_info.texts) != list:
            button_create_info.texts = [button_create_info.texts]
        self.texts = button_create_info.texts
        self.active = active
        self.value = value
        self.button_type = button_create_info.button_type
        self.referencing_functionality_tag = button_create_info.referencing_functionality_tag
        
        self.alignment_mode = button_create_info.alignment
        self.size = button_create_info.size

        self.numeric_alignment: NumericAlignment = button_create_info.numeric_alignment
        self.rect: pg.Rect = None
        self.buttons: list[Button] = None

        self.set_rects(self.alignment_mode, button_create_info.wrapping_box, self.size)
        
    def set_rects(self, alignment: AlignmentMode, wrapping_box: pg.Rect, size: iVector2) -> None:
        from ui import main_font
        match self.button_type:
            case ButtonType.Default:
                self.set_rects_default(alignment, wrapping_box, size)
            case ButtonType.Numeric:
                self.set_rects_numeric(alignment, wrapping_box, size)

    def set_rects_default(self, alignment: AlignmentMode, wrapping_box: pg.Rect, size: iVector2) -> None:
        from ui import main_font
        rect = main_font.render(self.texts[0], False, "white").get_rect()
        if size[0] != None:
            rect.width = size[0]
        if size[1] != None:
            rect.height = size[1]
        rect.center = wrapping_box.center
        match alignment:
            case AlignmentMode.Center:
                pass
            case AlignmentMode.Default:
                rect.topleft = wrapping_box.topleft
            case AlignmentMode.Top:
                rect.top = wrapping_box.top
            case AlignmentMode.Left:
                rect.left = wrapping_box.left
            case AlignmentMode.Bottom:
                rect.bottom = wrapping_box.bottom
            case AlignmentMode.Right:
                rect.right = wrapping_box.right
        self.rect = rect
        self.buttons = [Button(rect, ButtonFunctionality.Switch)]

    def set_rects_numeric(self, alignment: AlignmentMode, wrapping_box: pg.Rect, size: iVector2) -> None:
        from ui import main_font
        text = max([(s, main_font.render(s, False, "white").get_rect().width) for s in self.texts], key=lambda item: item[1])[0]
        text_surface = main_font.render(text, False, "white")

        match self.numeric_alignment:
            case NumericAlignment.BottomCenter | NumericAlignment.BottomSided | NumericAlignment.TopCenter | NumericAlignment.TopSided:
                rect = text_surface.get_rect()
                rect.height += main_font.render(left_switch_text, False, "white").get_rect().height
                main_text_rect = text_surface.get_rect()
            case NumericAlignment.SideTop | NumericAlignment.SideCenter | NumericAlignment.SideBottom:
                rect = main_font.render(f'{text} {1000}', False, "white").get_rect()
                rect.width += 2*main_font.render(left_switch_text, False, "white").get_rect().width
                main_text_rect = main_font.render(f'{text} {1000}', False, "white").get_rect()
        if size[0] != None:
            rect.width = size[0]
        if size[1] != None:
            rect.height = size[1]
        rect.center = wrapping_box.center
        
        match alignment:
            case AlignmentMode.Center:
                pass
            case AlignmentMode.Default:
                rect.topleft = wrapping_box.topleft
            case AlignmentMode.Top:
                rect.top = wrapping_box.top
            case AlignmentMode.Left:
                rect.left = wrapping_box.left
            case AlignmentMode.Bottom:
                rect.bottom = wrapping_box.bottom
            case AlignmentMode.Right:
                rect.right = wrapping_box.right
        self.rect = rect
        main_text_rect.center = rect.center

        left_switch_rect = main_font.render(left_switch_text, False, "white").get_rect()
        right_switch_rect = main_font.render(right_switch_text, False, "white").get_rect()
        match self.numeric_alignment:
            case NumericAlignment.BottomCenter:
                main_text_rect.top = rect.top
                left_switch_rect.topleft = main_text_rect.bottomleft
                right_switch_rect.topright = main_text_rect.bottomright
            case NumericAlignment.BottomSided:
                main_text_rect.top = rect.top
                left_switch_rect.bottomleft = rect.bottomleft
                right_switch_rect.bottomright = rect.bottomright
            case NumericAlignment.TopCenter:
                main_text_rect.bottom = rect.bottom
                left_switch_rect.bottomleft = main_text_rect.topleft
                right_switch_rect.bottomright = main_text_rect.topright
            case NumericAlignment.TopSided:
                main_text_rect.bottom = rect.bottom
                left_switch_rect.topleft = rect.topleft
                right_switch_rect.topright = rect.topright
            case NumericAlignment.SideTop:
                left_switch_rect.topleft = rect.topleft
                right_switch_rect.topright = rect.topright
            case NumericAlignment.SideCenter:
                left_switch_rect.centery = rect.centery
                left_switch_rect.left = rect.left
                right_switch_rect.centery = rect.centery
                right_switch_rect.right = rect.right
            case NumericAlignment.SideBottom:
                left_switch_rect.bottomleft = rect.bottomleft
                right_switch_rect.bottomright = rect.bottomright

        self.buttons = [Button(left_switch_rect, ButtonFunctionality.Decrease), Button(right_switch_rect, ButtonFunctionality.Increase)]

    def move(self, x, y) -> None:
        self.rect.topleft = (self.rect.left+x, self.rect.top+y)
        match self.button_type:
            case ButtonType.Numeric:
                for button in self.buttons:
                    button.rect.topleft = (button.rect.left+x, button.rect.top+y)

    def update(self, wrapping_box: pg.Rect) -> None:
        self.set_rects(self.alignment_mode, wrapping_box, self.size)

    def get_buttons(self):
        #list[tuple[pg.Rect, str, UIButton]]
        match self.button_type:
            case ButtonType.Default:
                if self.active:
                    return [(self.rect, self.referencing_functionality_tag[0]+'_off',self)]
                else:
                    return [(self.rect, self.referencing_functionality_tag[0]+'_on',self)]
            case ButtonType.Numeric:
                if len(self.texts) == 1:
                    referencing_teg = self.referencing_functionality_tag[0]
                elif len(self.texts) > 1:
                    referencing_teg = self.referencing_functionality_tag[self.value]
                return [(self.buttons[0].rect, referencing_teg+'_dec',self),(self.buttons[1].rect, referencing_teg+'_inc',self)]
        return [(self.rect, '',self)]

    def switch(self, increase_amount: float=0, min_max: iVector2=(0,500)) -> None:
        match self.button_type:
            case ButtonType.Default:
                self.switch_default()
            case ButtonType.Numeric:
                self.switch_numeric(increase_amount, min_max)
    
    def switch_default(self) -> None:
        self.active = not self.active

    def switch_numeric(self, increase_amount: float, min_max: iVector2) -> None:
        if len(self.texts) > 1:
            self.value += increase_amount
            if self.value < 0:
                self.value = len(self.texts) - 1
            if self.value >= len(self.texts):
                self.value = 0
        else:
            if self.value + increase_amount >= min_max[0] and self.value + increase_amount <= min_max[1]:
                self.value += increase_amount
            elif self.value + increase_amount < min_max[0]:
                self.value = min_max[0]
            else:
                self.value = min_max[1]

    def draw(self, screen, draw_edges: bool=False) -> None:
        if not self.enabled:
            return
        match self.button_type:
            case ButtonType.Default:
                self.draw_default(screen, draw_edges=draw_edges)
            case ButtonType.Numeric:
                self.draw_numeric(screen, draw_edges=draw_edges)
    
    def draw_default(self, screen, draw_edges: bool=True) -> None:
        from ui import Screen, main_font
        if draw_edges:
            draw_edges_around_rect(screen, self.rect)
        
        if self.active:
            color = "green"
        else:
            color = "white"
        text_surface = main_font.render(self.texts[0], False, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.main_screen.blit(text_surface, text_rect)

    def draw_numeric(self, screen, draw_edges: bool=True) -> None:
        from ui import Screen, main_font
        if len(self.texts) > 1:
            try:
                text = self.texts[self.value]
            except IndexError:
                text = self.texts[0]
        else:
            text = self.texts[0]
        match self.numeric_alignment:
            case NumericAlignment.BottomCenter | NumericAlignment.BottomSided | NumericAlignment.TopCenter | NumericAlignment.TopSided:
                main_text_surface = main_font.render(text, False, "white")
                main_text_rect = main_text_surface.get_rect()
                text_width = main_text_rect.width
                main_text_rect.width = self.rect.width
                main_text_rect.left = self.rect.left

                value_text_surface = main_font.render(str(self.value), False, "white")
                value_text_rect = value_text_surface.get_rect(centerx=self.rect.centerx)

                match self.numeric_alignment:
                    case NumericAlignment.BottomCenter | NumericAlignment.BottomSided:
                        main_text_rect.top = self.rect.top
                        value_text_rect.bottom = self.rect.bottom
                    case NumericAlignment.TopCenter | NumericAlignment.TopSided:
                        value_text_rect.top = self.rect.top
                        main_text_rect.bottom = self.rect.bottom
                if draw_edges:
                    draw_edges_around_rect(screen, main_text_rect)
                main_text_rect.width = text_width
                main_text_rect.centerx = self.rect.centerx
                screen.main_screen.blit(main_text_surface, main_text_rect)
                if len(self.texts) < 2:
                    screen.main_screen.blit(value_text_surface, value_text_rect)

                left_text_surface = main_font.render(left_switch_text, False, "white")
                right_text_surface = main_font.render(right_switch_text, False, "white")
                left_text_rect = left_text_surface.get_rect()
                right_text_rect = right_text_surface.get_rect()
                
                numeric_bar = pg.Rect((0,0),(0,0))
                match self.numeric_alignment:
                    case NumericAlignment.BottomCenter:
                        numeric_bar = pg.Rect((main_text_rect.left, main_text_rect.bottom), (main_text_rect.right-main_text_rect.left, self.rect.bottom-main_text_rect.bottom))
                        left_text_rect.bottomleft = main_text_rect.left, self.rect.bottom
                        right_text_rect.bottomright = main_text_rect.right, self.rect.bottom
                    case NumericAlignment.BottomSided:
                        numeric_bar = pg.Rect((self.rect.left, main_text_rect.bottom), (self.rect.right-self.rect.left, self.rect.bottom-main_text_rect.bottom))
                        left_text_rect.bottomleft = self.rect.bottomleft
                        right_text_rect.bottomright = self.rect.bottomright
                    case NumericAlignment.TopCenter:
                        numeric_bar = pg.Rect((main_text_rect.left, self.rect.top), (main_text_rect.right-main_text_rect.left, main_text_rect.top-self.rect.top))
                        left_text_rect.topleft = main_text_rect.left, self.rect.top
                        right_text_rect.topright = main_text_rect.right, self.rect.top
                    case NumericAlignment.TopSided:
                        numeric_bar = pg.Rect((self.rect.left, self.rect.top), (self.rect.right-self.rect.left, main_text_rect.top-self.rect.top))
                        left_text_rect.topleft = self.rect.topleft
                        right_text_rect.topright = self.rect.topright

                left_text_rect = self.buttons[0].rect
                right_text_rect = self.buttons[1].rect
                numeric_bar = pg.Rect(left_text_rect.topleft, (right_text_rect.right-left_text_rect.left, left_text_rect.height))

                
                screen.main_screen.blit(left_text_surface, left_text_rect)
                screen.main_screen.blit(right_text_surface, right_text_rect)

                if draw_edges:
                    draw_edges_around_rect(screen, numeric_bar)
                    draw_edges_around_rect(screen, left_text_rect)
                    draw_edges_around_rect(screen, right_text_rect)

            case NumericAlignment.SideTop | NumericAlignment.SideCenter | NumericAlignment.SideBottom:
                if len(self.texts) < 2:
                    main_text_surface = main_font.render(f'{text} {self.value}', False, "white")
                else:
                    main_text_surface = main_font.render(f'{text}', False, "white")
                main_text_rect = main_text_surface.get_rect()
                main_text_rect.center = self.rect.center
                screen.main_screen.blit(main_text_surface, main_text_rect)
                
                left_text_surface = main_font.render(left_switch_text, False, "white")
                right_text_surface = main_font.render(right_switch_text, False, "white")
                left_text_rect = left_text_surface.get_rect(left=self.rect.left)
                right_text_rect = right_text_surface.get_rect(right=self.rect.right)

                match self.numeric_alignment:
                    case NumericAlignment.SideTop:
                        left_text_rect.top = self.rect.top
                        right_text_rect.top = self.rect.top
                    case NumericAlignment.SideCenter:
                        left_text_rect.centery = self.rect.centery
                        right_text_rect.centery = self.rect.centery
                    case NumericAlignment.SideBottom:
                        left_text_rect.bottom = self.rect.bottom
                        right_text_rect.bottom = self.rect.bottom

                screen.main_screen.blit(left_text_surface, left_text_rect)
                screen.main_screen.blit(right_text_surface, right_text_rect)

                if draw_edges:
                    draw_edges_around_rect(screen, left_text_rect)
                    draw_edges_around_rect(screen, right_text_rect)
                    main_text_rect.width = self.rect.width - left_text_rect.width - right_text_rect.width
                    main_text_rect.height = self.rect.height
                    main_text_rect.topleft = self.rect.left + left_text_rect.width, self.rect.top
                    draw_edges_around_rect(screen, main_text_rect)

def draw_edges_around_rect(screen, rect: pg.Rect, color="white") -> None:
    if rect.top > 0:
        pg.draw.line(screen.main_screen, color, rect.topleft, rect.topright)
    if rect.right < screen.size[0]:
        pg.draw.line(screen.main_screen, color, rect.topright, rect.bottomright)
    if rect.left > 0:
        pg.draw.line(screen.main_screen, color, rect.bottomleft, rect.topleft)
    if rect.bottom < screen.size[1]:
       pg.draw.line(screen.main_screen, color, rect.bottomright, rect.bottomleft)