from typing import List, Tuple
from random import random
from math import floor
from utils.config import AMMO_COUNT, LIFE_COUNT, FIELD_WIDTH, FIELD_HEIGHT
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
            raw_shot_x = floor(target_zone_size * random()) + 1
            if raw_shot_x > target_zone_size:
                raw_shot_x = target_zone_size
            raw_shot_y = floor(target_zone_size * random()) + 1
            if raw_shot_y > target_zone_size:
                raw_shot_y = target_zone_size
            shot_x = targets[target_index].coords.x - int((target_zone_size - 1) / 2) + raw_shot_x
            shot_y = targets[target_index].coords.y - int((target_zone_size - 1) / 2) + raw_shot_y
            shot = Shot(x=shot_x, y=shot_y) if shot_x > 0 and shot_x <= FIELD_WIDTH and shot_y > 0 and shot_y <= FIELD_HEIGHT else None
            return (self.direction, shot)
        else:
            d = floor(4 * random())
            return (Direction(d), None)
    

    def show(self, point_character: str = "B") -> str:
        return point_character


class RamTank(Tank):
    model = "Таран"

    def __init__(self, x, y, direction, map_width, map_height):
        Tank.__init__(self, x, y, direction, map_width, map_height,
                      ammo_count=4, life_count=8)

    def is_life_finished(self):
        return self.life <= 0

    def is_ammo_finished(self):
        return self.ammo <= 0

    def _dist(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def next(self, origin, targets, shots):
        if not targets:
            return (Direction.Stop, None)

        # Находим ближайшего врага
        nearest = targets[0]
        min_d = self._dist(origin, nearest.coords)
        for t in targets[1:]:
            d = self._dist(origin, t.coords)
            if d < min_d:
                min_d = d
                nearest = t

        # Если есть патроны и враг близко (≤2) — стреляем
        if not self.is_ammo_finished() and min_d <= 2:
            return (self.direction, Shot(x=nearest.coords.x, y=nearest.coords.y))

        # Если патронов нет или враг далеко — идём на сближение
        dx = nearest.coords.x - origin.x
        dy = nearest.coords.y - origin.y
        if abs(dx) >= abs(dy):
            new_dir = Direction.Right if dx > 0 else Direction.Left
        else:
            new_dir = Direction.Down if dy > 0 else Direction.Up
        return (new_dir, None)

    def show(self, point_character="R"):
        return point_character
