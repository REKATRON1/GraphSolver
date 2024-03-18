import pygame as pg

from ui import KeyInfo, KeyFunctionality

class InputData():
    def __init__(self, key_infos: list[KeyInfo]) -> None:
        self.key_infos: list[KeyInfo] = key_infos
    def get_all_key_infos(self) -> list[KeyInfo]:
        return self.key_infos
    def get_all_key_codes(self) -> list[pg.key]:
        return [k.key_code for k in self.key_infos]
    def get_all_key_infos_with_functionality(self, functionality: KeyFunctionality) -> list[KeyInfo]:
        return [k for k in self.key_infos if k.functionality == functionality]