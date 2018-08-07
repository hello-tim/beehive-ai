from bee import Bee
import random

class Swarm:
    def __init__(self, size, scWidth, scHeight, goalX, goalY):
        self.bees = list()
        self.size = size
        self.fitnessSum = 0
        self.populate(scWidth, scHeight, goalX, goalY)
        self.generation = 0
        self.bestBee = 0
        self.minStep = 1000

    def populate(self, scWidth, scHeight, goalX, goalY):
        for i in range(self.size):
            self.bees.append(Bee(scWidth, scHeight, goalX, goalY))

    def show(self, screen):
        for i in range(len(self.bees)):
            self.bees[i].show(screen)

    def update(self):
        for i in range(len(self.bees)):
            if self.bees[i].brain.step > self.minStep:
                self.bees[i].dead = True
            else:
                self.bees[i].update()

    def calcFitness(self):
        for i in range(len(self.bees)):
            self.bees[i].calcFitness()

    def allDead(self):
        for i in range(len(self.bees)):
            if not (self.bees[i].dead or self.bees[i].reachGoal):
                return False
        return True

    def naturalSelect(self):
        self.sumFitness()
        self.setBestBee()
        newGen = list()
        for i in range(len(self.bees)):
            if i == 0: # first is best bee, must survive
                newGen.append(self.bees[self.bestBee].makeChild())
                newGen[i].isBest = True
            else:
                parent = self.selectParent()
                newGen.append(parent.makeChild())
        self.bees = newGen
        self.fitnessSum = 0
        self.generation += 1

    def sumFitness(self):
        for i in range(len(self.bees)):
            self.fitnessSum += self.bees[i].fitness

    def selectParent(self):
        rand = random.uniform(0, self.fitnessSum)
        runningSum = 0
        for i in range(len(self.bees)):
            runningSum += self.bees[i].fitness
            if runningSum > rand:
                return self.bees[i]
        return None

    def mutate(self):
        for i in range(len(self.bees)):
            if not self.bees[i].isBest: # don't mutate if best
                self.bees[i].brain.mutate()


    def setBestBee(self): # find bee with best fitness to survive
        max = 0
        maxIndex = 0
        for i in range(len(self.bees)):
            if self.bees[i].fitness > max:
                max = self.bees[i].fitness
                maxIndex = i
        self.bestBee = maxIndex
        if self.bees[self.bestBee].reachGoal:
            self.minStep = self.bees[self.bestBee].brain.step
            # -------------------------------------------------------------------------
            # Optional: prints progression as steps and which generation
            print("Minimum step: ", self.minStep, " | Generation: ", self.generation)
