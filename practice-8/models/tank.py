from typing import List, Tuple
from utils.config import AMMO_COUNT, LIFE_COUNT
from models.coords import Coords
from models.size import Size
from models.direction import Direction
from models.shot import Shot


class Tank:
    model = "BaseModel"
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
        print(f"> {self.model} (life: {self.life}, ammo: {self.ammo})")

    
    def next(self, origin: Coords, targets: List[Tuple[Coords, bool]], shots: List[Coords]) -> Tuple[Direction, Shot]:
        """
        Return next step's decision

        :param targets: List[Tuple[Coords, bool]] of target coordinates and shooting attribute
        :return: Tuple[Direction, Shot]
        """
        return (self.direction, None)
    

    def show(self) -> str:
        return "B"


class FirstTank(Tank):
    model = "FirstModel"
    def next(self, origin: Coords, targets: List[Tuple[Coords, bool]], shots: List[Coords]) -> Tuple[Direction, Shot]:
        return (self.direction, None)
    

    def show(self) -> str:
        return "F"


class SecondTank(Tank):
    model = "SecondModel"
    def next(self, origin: Coords, targets: List[Tuple[Coords, bool]], shots: List[Coords]) -> Tuple[Direction, Shot]:
        return (self.direction, None)
    

    def show(self) -> str:
        return "S"
