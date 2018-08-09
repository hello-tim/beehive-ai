from bee import Bee
import random

class Swarm:
    def __init__(self, size, scWidth, scHeight, goalX, goalY):
        self.bees = list()
        self.size = size
        self.fitnessSum = 0
        # Populate list with Bee objects
        self.populate(scWidth, scHeight, goalX, goalY)
        self.generation = 0
        # Index of most fit Bee
        self.bestBee = 0
        # Minimum steps required to reach goal
        self.minStep = 1000

    def populate(self, scWidth, scHeight, goalX, goalY):
        for i in range(self.size):
            self.bees.append(Bee(scWidth, scHeight, goalX, goalY))

    def show(self, screen):
        # Draw function for updated positions on screen
        for i in range(len(self.bees)):
            self.bees[i].show(screen)

    def update(self):
        # Check if out of steps or move
        for i in range(len(self.bees)):
            if self.bees[i].brain.step > self.minStep:
                self.bees[i].dead = True
            else:
                self.bees[i].update()

    def calcFitness(self):
        # Calculate the fitness of each Bee
        for i in range(len(self.bees)):
            self.bees[i].calcFitness()

    def allDead(self):
        # Check if every Bee in population is dead
        for i in range(len(self.bees)):
            if not (self.bees[i].dead or self.bees[i].reachGoal):
                return False
        return True

    def naturalSelect(self):
        # Sum of all Bee fitness
        self.sumFitness()
        # Find the most fit Bee
        self.setBestBee()
        newGen = list()
        for i in range(len(self.bees)):
            if i == 0:
                # Most fit Bee always survives to next generation
                newGen.append(self.bees[self.bestBee].makeChild())
                newGen[i].isBest = True
            else:
                parent = self.selectParent()
                newGen.append(parent.makeChild())
        # Population is now children
        for i in range(len(newGen)):
            self.bees[i] = newGen[i]
        self.fitnessSum = 0 # Reset fitnessSum
        self.generation += 1

    def sumFitness(self):
        # Sum of all Bee fitness
        for i in range(len(self.bees)):
            self.fitnessSum += self.bees[i].fitness

    def selectParent(self):
        # Select random number between 0 and sum of all fitness
        rand = random.uniform(0, self.fitnessSum)
        runningSum = 0
        for i in range(len(self.bees)):
            runningSum += self.bees[i].fitness
            if runningSum > rand:
                # Select parent if running sum exceeds random number
                return self.bees[i]
        return None

    def mutate(self):
        for i in range(len(self.bees)):
            if not self.bees[i].isBest: # Best Bee exempt from mutation
                self.bees[i].brain.mutate()


    def setBestBee(self): # Find Bee with best fitness to survive
        max = 0
        maxIndex = 0
        for i in range(len(self.bees)):
            if self.bees[i].fitness > max:
                max = self.bees[i].fitness
                maxIndex = i
        # Grab index of best Bee
        self.bestBee = maxIndex
        # Set new minimum steps to reach goal
        if self.bees[self.bestBee].reachGoal:
            self.minStep = self.bees[self.bestBee].brain.step
            # Optional: prints progression as steps and which generation
            # print("Minimum step: ", self.minStep, " | Generation: ", self.generation)
