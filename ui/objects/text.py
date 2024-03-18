import pygame as pg

from dataclasses import dataclass

from .ui_object import UIObject, UICreateInfo, UIRequestCreateInfo, AlignmentMode

@dataclass
class TextRequestCreateInfo(UIRequestCreateInfo):
    text: str

@dataclass
class TextCreateInfo(UICreateInfo):
    text: str
    wrapping_box: pg.Rect
    alignment: AlignmentMode

class UIText(UIObject):
    def __init__(self, text: str, wrapping_box: pg.Rect, alignment: AlignmentMode) -> None:
        self.enabled = True
        self.text = text

        self.rect = None
        self.set_rect(wrapping_box, alignment)

    def set_rect(self, wrapping_box: pg.Rect, alignment: AlignmentMode) -> None:
        from ui import main_font
        rect = main_font.render(self.text, False, "white").get_rect()
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

    def move(self, x, y) -> None:
        self.rect.topleft = (self.rect.left+x, self.rect.top+y)

    def draw(self, screen) -> None:
        if not self.enabled:
            return
        from ui import Screen, main_font
        
        text_surface = main_font.render(self.text, False, "white")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.main_screen.blit(text_surface, text_rect)