import pygame as pg

from enum import Enum
from dataclasses import dataclass

class KeyFunctionality(Enum):
    #Algo updates
    EditPoints = 0
    ChangeAlgoMode = 1
    ChangeSolvingType = 2

    Run = 10

    ActivateAnimation = 50

    #Ui inputs
    ChangeWindow = 100
    ChangeProjection = 101
    ChangeSidebars = 102


@dataclass
class KeyInfo:
    key_code: pg.key
    key_functionality: KeyFunctionality
    mode: int = 0
    amount: int = 0