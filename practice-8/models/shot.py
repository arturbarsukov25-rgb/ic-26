from models.coords import Coords


class Shot():
    def __init__(self, x: int, y: int):
        self.coords = Coords(x=x, y=y)
    

    def show(self) -> str:
        return "⏺"
