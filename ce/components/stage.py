from ce.components.die import Die
from typing import List


class Stage:
    def __init__(self):
        self.dice: List[Die] = [Die() for _ in range(5)]
        self.on_stage: List[Die] = self.dice
        self.off_stage: List[Die] = []

    def take_die(self, die: Die) -> str:
        if die in self.on_stage:
            self.on_stage.remove(die)
            self.off_stage.append(die)
        return die.upper_face

    def reroll_all(self) -> None:
        self.on_stage = self.dice
        for die in self.dice:
            die.roll()
        self.off_stage = []

    def upper_faces_on_stage(self) -> List[str]:
        return [die.upper_face for die in self.dice]

    def upper_faces_off_stage(self) -> List[str]:
        return [die.upper_face for die in self.dice]

    def roll_off(self, face) -> int:
        for die in self.off_stage:
            die.roll()
        return len([die for die in self.off_stage if die.upper_face == face])
