from ce.components.die import Die
from typing import List

DICE_COUNT = 5


class Stage:
    def __init__(self):
        self.dice: List[Die] = [Die() for _ in range(DICE_COUNT)]
        self.on_stage: List[Die] = self.dice
        self.off_stage: List[Die] = []

    def take_die(self, die: Die) -> str:
        if die in self.on_stage:
            self.on_stage.remove(die)
            self.off_stage.append(die)
        if len(self.on_stage) == DICE_COUNT:
            self.reroll_all_dice()
        return die.upper_face

    def reroll_all_dice(self) -> None:
        self.on_stage = self.dice
        for die in self.dice:
            die.roll()
        self.off_stage = []

    def can_reroll(self) -> bool:
        return len(list(set(self.upper_faces_on_stage()))) == 1

    def upper_faces_on_stage(self) -> List[str]:
        return [die.upper_face for die in self.dice]

    def upper_faces_off_stage(self) -> List[str]:
        return [die.upper_face for die in self.dice]

    def off_stage_count(self) -> int:
        return len(self.off_stage)

    def roll_dice_off_stage(self, face) -> int:
        for die in self.off_stage:
            die.roll()
        return len([die for die in self.off_stage if die.upper_face == face])
