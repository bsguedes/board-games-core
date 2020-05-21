from typing import List
from ce.objectives.objective import Objective
from random import shuffle


class ObjectiveBoard:
    def __init__(self, objective_list):
        self.objectives: List[Objective] = objective_list
        self.round_objectives = self.draw_objectives(4)

    def shuffle_objectives(self) -> None:
        shuffle(self.objectives)

    def draw_objectives(self, amount: int) -> List[Objective]:
        objectives = self.objectives[len(self.objectives) - amount:]
        self.objectives = self.objectives[:len(self.objectives) - amount]
        return objectives
