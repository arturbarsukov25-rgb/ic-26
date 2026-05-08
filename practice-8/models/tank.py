from typing import List, Tuple
from random import random
from math import floor
from utils.config import AMMO_COUNT, LIFE_COUNT
from models.coords import Coords
from models.size import Size
from models.direction import Direction
from models.shot import Shot


class Tank:
    model = "Базовая модель"
    def __init__(
        self,
        x: int,
        y: int,
        direction: Direction,
        map_width: int,
        map_height: int,
        ammo_count: int = AMMO_COUNT,
        life_count: int = LIFE_COUNT,
        gun_angle: float = 0
    ):
        self.coords = Coords(x=x, y=y)
        self.direction = direction
        self.map = Size(width=map_width, height=map_height)
        self.ammo = ammo_count
        self.life = life_count
        self.angle = gun_angle
        self.targets = {}
    

    def is_ammo_finished(self):
        return self.ammo <= 0
    

    def is_life_finished(self):
        return self.life <= 0
    

    def decrease_ammo(self):
        if not self.is_ammo_finished():
            self.ammo -= 1
    

    def decrease_life(self):
        if not self.is_life_finished():
            self.life -= 1


    def show_stats(self):
        print(f"> {self.model} (жизнь: {self.life}, снаряды: {self.ammo})")

    
    def next(self, origin: Coords, targets: List[Coords], shots: List[Coords]) -> Tuple[Direction, Shot]:
        """
        Return next step's decision

        :param targets: List[Coords] list of target coordinates
        :return: Tuple[Direction, Shot]
        """
        if not self.is_ammo_finished() and len(targets) > 0 and floor(2 * random()) == 0:
            target_zone_size = 3
            target_index = floor(len(targets) * random())
            shot_x = floor(target_zone_size * random()) + 1
            if shot_x > target_zone_size:
                shot_x = target_zone_size
            shot_y = floor(target_zone_size * random()) + 1
            if shot_y > target_zone_size:
                shot_y = target_zone_size
            shot = Shot(
                x=targets[target_index].coords.x - int((target_zone_size - 1) / 2) + shot_x,
                y=targets[target_index].coords.y - int((target_zone_size - 1) / 2) + shot_y
            )
            return (self.direction, shot)
        else:
            d = floor(4 * random())
            return (Direction(d), None)
    

    def show(self, point_character: str = "B") -> str:
        return point_character


class CustomTank(Tank):
    model = "Кастомизированная модель"
    def next(self, origin: Coords, targets: List[Coords], shots: List[Coords]) -> Tuple[Direction, Shot]:
        return (self.direction, None)
    

    def show(self, point_character: str = "С") -> str:
        return point_character
