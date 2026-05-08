from typing import List, Type
from seeders.tank_factory import generate_tank
from utils.config import FIELD_WIDTH, FIELD_HEIGHT, MAX_ROUND_COUNT
from models.tank import Tank, CustomTank
from models.field import Field
from controllers.game import Game


APPROVED_TANK_MODELS = [
    Tank,
    CustomTank
]


def init_field() -> Field:
    return Field(map_width=FIELD_WIDTH, map_height=FIELD_HEIGHT)


def select_player_models() -> List[Type[Tank]]:
    models = []
    player_count = int(input("Выберете количество игроков: "))
    print("В игре есть следующие модели танков:")
    for i in range(len(APPROVED_TANK_MODELS)):
        print(f"{i + 1}. {APPROVED_TANK_MODELS[i].model}")
    for i in range(player_count):
        model_number = int(input(f"Выберете номер модели танка #{i + 1}: "))
        while(model_number <= 0 and model_number > len(APPROVED_TANK_MODELS) + 1):
            model_number = input(f"Такой модели не существует. Выберете номер модели танка #{i + 1}: ")
        models.append(APPROVED_TANK_MODELS[model_number - 1])
    return models


def init_tanks(field: Field, tank_models: List[Type[Tank]]) -> List[Tank]:
    tanks = []
    for tank_class in tank_models:
        tanks.append(generate_tank(model_class=tank_class, field=field))
    return tanks


def run():
    battle_field = init_field()
    player_models = select_player_models()
    players = init_tanks(field=battle_field, tank_models=player_models)
    game = Game(field=battle_field, tanks=players)
    round_counter = 1
    print(">>>>>>> Игра началась! <<<<<<<\n\n")

    while(round_counter <= MAX_ROUND_COUNT and not game.is_finished()):
        print(f"\nRound #{round_counter}")
        game.play()
        round_counter += 1
    
    print("\n>>>>>>> Игра завершена! <<<<<<<")
    print("\n------- Результаты! -------\n")
    for p in players:
        p.show_stats()
    print("\n---------------------------\n")


if __name__ == "__main__":
    run()
