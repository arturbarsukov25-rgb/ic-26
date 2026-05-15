from typing import List, Tuple
from models.size import Size
from models.coords import Coords
from models.direction import Direction
from models.tank import Tank
from models.shot import Shot
from random import random
from math import floor


class Field:
    def __init__(
        self,
        map_width: int,
        map_height: int,
    ):
        self.size = Size(width=map_width, height=map_height)


    def move(self, coords: Coords, direction: Direction) -> Coords:
        if coords.x == 1 and direction == Direction.Left:
            return coords
        elif coords.x == self.size.width and direction == Direction.Right:
            return coords
        elif coords.y == 1 and direction == Direction.Up:
            return coords
        elif coords.y == self.size.height and direction == Direction.Down:
            return coords
        elif direction == Direction.Left:
            coords.x -= 1
        elif direction == Direction.Right:
            coords.x += 1
        elif direction == Direction.Up:
            coords.y -= 1
        elif direction == Direction.Down:
            coords.y += 1
        return coords
    

    def show(self, tanks: List[Tank], shots: List[Shot]) -> List[List[str]]:
        map = []
        for _ in range(self.size.height):
            row = ["·" for _ in range(self.size.width)]
            map.append(row)
        for tank_index in range(len(tanks)):
            map[tanks[tank_index].coords.y - 1][tanks[tank_index].coords.x - 1] = tanks[tank_index].show(point_character=str(tank_index + 1))
        for shot in shots:
            map[shot.coords.y - 1][shot.coords.x - 1] = shot.show()
        return map
        

    def get_random_player_params(self) -> Tuple[Coords, Direction]:
        x = floor(self.size.width * random()) + 1
        if x > self.size.width:
            x = self.size.width
        y = floor(self.size.height * random()) + 1
        if y > self.size.height:
            y = self.size.height
        raw_d = floor(4 * random())
        d = Direction.Stop
        if raw_d == 1:
            d = Direction.Up
        elif raw_d == 2:
            d = Direction.Right
        elif raw_d == 3:
            d = Direction.Down
        elif raw_d == 4:
            d = Direction.Left
        return (Coords(x=x, y=y), d)
