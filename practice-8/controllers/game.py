from typing import List
from models.tank import Tank
from models.field import Field


class Game:
    def __init__(self, field: Field, tanks: List[Tank]):
        self.field = field
        self.players = tanks
        self.shots = []


    def is_finished(self) -> bool:
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
        return len(self.players) < 2
    

    def play(self):
        current_shots = self.shots
        next_shots = []
        for tank_index in range(len(self.players)):
            current_targets = []
            for enemy_index in range(len(self.players)):
                if enemy_index != tank_index:
                    current_targets.append(self.players[enemy_index])
            new_coords = self.field.move(coords=self.players[tank_index].coords, direction=self.players[tank_index].direction)
            direction, shot = self.players[tank_index].next(origin=new_coords, targets=current_targets, shots=current_shots)
            self.players[tank_index].direction = direction
            if shot != None and not self.players[tank_index].is_ammo_finished():
                self.players[tank_index].decrease_ammo()
                next_shots.append(shot)
            print(f"Tank <{self.players[tank_index].model}>: {direction, shot}")
        map = self.field.show(tanks=self.players, shots=current_shots)
        for row in map:
            print(" ".join(row))
        self.shots = next_shots
