from ce.components.die import Die


class Stage:
    def __init__(self):
        self.dice = [Die() for _ in range(5)]
        self.on_stage = self.dice
        self.off_stage = []

    def take_die(self, die):
        if die in self.on_stage:
            self.on_stage.remove(die)
            self.off_stage.append(die)
        return die.upper_face

    def reroll(self):
        self.on_stage = self.dice
        for die in self.dice:
            die.roll()
        self.off_stage = []

    def upper_faces(self):
        return [die.upper_face for die in self.dice]

    def roll_off(self, face):
        for die in self.off_stage:
            die.roll()
        return len([die for die in self.off_stage if die.upper_face == face])
