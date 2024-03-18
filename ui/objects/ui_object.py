
from enum import Enum
from dataclasses import dataclass

class AlignmentMode(Enum):
    Default = 0
    Top = 1
    Left = 2
    Bottom = 3
    Right = 4
    Center = 5

class UIObject():
    def draw(self, screen) -> None:
        """draw object to screen"""
        from ui import Screen
        pass

@dataclass
class UICreateInfo:
    pass

@dataclass
class UIRequestCreateInfo:
    pass