import pygame as pg
import math
from data.brain import Brain

class Bee:
    def __init__(self, scWidth, scHeight, goalX, goalY):
        # Bee's height and width
        self.width = 15
        self.height = 10
        # Screen height and width, Bee class shouldn't need this
        # but too lazy and brand new to Python/PyGame
        self.scWidth = scWidth
        self.scHeight = scHeight
        # Position of goal (beehive)
        self.goalX = goalX
        self.goalY = goalY
        # Initial position bottom middle of screen
        self.pos = [self.scWidth/2 - self.width/2, self.scHeight - self.height - 10]
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.bee = pg.image.load("data/resources/bee.png")
        # Initialize bee's brain with 1000 directions
        self.brain = Brain(1000)
        self.dead = False
        self.fitness = 0
        self.reachGoal = False
        self.isBest = False

    def show(self, screen):
        # Draw bee at current position
        screen.blit(self.bee, (self.pos[0], self.pos[1]))

    def move(self):
        if len(self.brain.directions) > self.brain.step:
            # Change random radian into x, y vectors and assign to acceleration
            self.acc[0] = math.cos(self.brain.directions[self.brain.step])
            self.acc[1] = math.sin(self.brain.directions[self.brain.step])
            self.brain.step += 1
        else:
            # Bee's brain has ran out of steps
            self.dead = True
        # Increase velocity by acceleration
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        # Increase position by velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def update(self):
        if not (self.dead or self.reachGoal):
            self.move()
            if (self.pos[0] < 255 > 10 and self.pos[1] < 215 and self.pos[1] > 130):
                self.dead = True # Dies if collide with fence 1
            elif (self.pos[0] > 230 and self.pos[1] < 415 and self.pos[1] > 330):
                self.dead = True # Dies if collide with fence 2
            elif (self.pos[0] < 8 or self.pos[0] > self.scWidth - self.width or self.pos[1] < 8 or self.pos[1] > self.scHeight - self.height):
                self.dead = True # Dies if touches edge/border/wall of screen
            elif math.hypot(self.goalX - self.pos[0], self.goalY - self.pos[1]) < 5:
                self.reachGoal = True # Reach goal is distance from goal is < 5

    def calcFitness(self):
        if self.reachGoal:
            # Fitness function
            self.fitness = 1.0/16.0 + 10000.0/(self.brain.step ** 2)
        else:
            # Inverse of distance means bee with shortest distance from goal is most fit
            dist = math.hypot(self.goalX - self.pos[0], self.goalY - self.pos[1])
            self.fitness = 1.0/(dist ** 2)

    def makeChild(self):
        # Makes child with copy of parent's brain (directions)
        child = Bee(self.scWidth, self.scHeight, self.goalX, self.goalY)
        child.brain = self.brain.clone()
        return child
