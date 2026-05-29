from typing import Type
from models.tank import Tank
from models.field import Field


def generate_tank(model_class: Type[Tank], field: Field, player_index: int) -> Tank:
    coords, direction = field.get_random_player_params()
    return model_class(x = coords.x, y = coords.y, direction = direction, player_index=player_index, map_width = field.size.width, map_height = field.size.height)
