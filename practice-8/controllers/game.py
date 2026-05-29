from copy import deepcopy
from enum import Enum
from time import sleep
from sys import stdout
from typing import List
from models.shot import Shot
from models.direction import Direction
from models.tank import Tank
from models.field import Field

from utils.config import MAX_ROUND_COUNT


class ANSI_Escape_Codes(Enum):
    UP_FOR_ONE_LINE = "\033[F"
    ERASE_FOLLOWING_STRING = "\033[K"


class Game:
    def __init__(self, field: Field, tanks: List[Tank]):
        self.field = field
        self.players = tanks
        self.shots = []
        self.output_string_counter = 0


    def is_finished(self, round: int = 1) -> bool:
        if MAX_ROUND_COUNT > 0 and round > MAX_ROUND_COUNT:
            return True
        target_players = []
        for tank_index in range(len(self.players)):
            other_tanks = self.players[:tank_index] + self.players[tank_index + 1:]
            for enemy in other_tanks:
                if enemy.coords.x == self.players[tank_index].coords.x and enemy.coords.y == self.players[tank_index].coords.y:
                    target_players.append(tank_index)
        for tank_index in range(len(target_players) - 1, 0, -1):
            self.players[tank_index].decrease_life()
        for tank in self.players:
            for shot in self.shots:
                if shot.coords.x == tank.coords.x and shot.coords.y == tank.coords.y:
                    tank.decrease_life()
        removed_players = []
        for tank_index in range(len(self.players)):
            if self.players[tank_index].is_life_finished():
                removed_players.append(tank_index)
        for tank_index in range(len(target_players) - 1, 0, -1):
            self.players.pop(tank_index)
        if self.output_string_counter > 0:
            stdout.write("".join([ANSI_Escape_Codes.UP_FOR_ONE_LINE.value for _ in range(self.output_string_counter)]))
        return len(self.players) < 2
    

    def play(self, round: int = 1):
        current_shots = self.shots
        next_shots = []
        self.write_into_console(output=f"Round #{round}\n", default_prefix="\n")
        players_counter = len(self.players)
        for tank_index in range(players_counter):
            current_targets = []
            for enemy_index in range(players_counter):
                if enemy_index != tank_index:
                    current_targets.append(self.players[enemy_index])
            new_coords = self.field.move(coords=self.players[tank_index].coords, direction=self.players[tank_index].direction)
            direction, shot = self.players[tank_index].next(origin=new_coords, targets=current_targets, shots=current_shots)
            self.players[tank_index].direction = direction
            if shot and not self.players[tank_index].is_ammo_finished():
                self.players[tank_index].decrease_ammo()
                next_shots.append(shot)
            self.write_into_console(output=f"Tank <{self.players[tank_index].get_player_info()}> ({tank_index + 1}): {self.prepare_direction_output(direction=direction)}, {self.prepare_shot_output(shot)}, Жизнь={self.players[tank_index].life}, Снаряды={self.players[tank_index].ammo}\n")
        map = self.field.show(tanks=self.players, shots=current_shots)
        for row in map:
            self.write_into_console(output=" ".join(row) + '\n')
        self.shots = deepcopy(next_shots)
        self.output_string_counter = players_counter + len(map) + 1
        sleep(1)


    def write_into_console(self, output: str, default_prefix: str = ""):
        stdout.write(f"{ANSI_Escape_Codes.ERASE_FOLLOWING_STRING.value if self.output_string_counter > 0 else default_prefix}{output}")

    
    def prepare_shot_output(self, shot: Shot) -> str:
        return 'Не стреляет' if shot == None else 'Стреляет'


    def prepare_direction_output(self, direction: Direction) -> str:
        if direction == Direction.Stop:
            return "Остановился"
        elif direction == Direction.Up:
            return "Едет вверх"
        elif direction == Direction.Right:
            return "Едет вправо"
        elif direction == Direction.Down:
            return "Едет вниз"
        elif direction == Direction.Left:
            return "Едет влево"
