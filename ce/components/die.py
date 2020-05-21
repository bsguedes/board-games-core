from random import sample


class Die:
    def __init__(self):
        self.faces = ['X1', 'X2', 'X3', 'X4', 'X5', 'X1/X2']
        self.upper_face = None
        self.roll()

    def roll(self) -> None:
        self.upper_face = sample(self.faces, 1)[0]
