import random
import math

class Brain:
    def __init__(self, size):
        self.step = 0
        self.directions = [0] * size
        self.randomize()

    def randomize(self):
        for i in range(len(self.directions)):
            # load random radians for vectors
            self.directions[i] = random.uniform(0, 2 * math.pi)

    def clone(self):
        clone = Brain(len(self.directions))
        for i in range(len(clone.directions)):
            clone.directions[i] = self.directions[i]
        return clone

    def mutate(self):
        mutationRate = 0.01 # chance of vector in directions being changed
        for i in range(len(self.directions)):
            if random.random() < mutationRate:
                self.directions[i] = random.uniform(0, 2 * math.pi)
