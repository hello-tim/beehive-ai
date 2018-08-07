import pygame as pg
import math
from brain import Brain


class Bee:
    def __init__(self, scWidth, scHeight, goalX, goalY):
        self.width = 15
        self.height = 10
        self.scWidth = scWidth
        self.scHeight = scHeight
        self.goalX = goalX
        self.goalY = goalY
        # initial position bottom middle of screen
        self.pos = [self.scWidth/2 - self.width/2, self.scHeight - self.height - 10]
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.bee = pg.image.load("resources/bee.png")
        self.brain = Brain(1000) # initialize brain with 400 vectors
        self.dead = False
        self.fitness = 0
        self.reachGoal = False
        self.isBest = False

    def show(self, screen):
        # draw bee at current position
        screen.blit(self.bee, (self.pos[0], self.pos[1]))

    def move(self):
        if len(self.brain.directions) > self.brain.step:
            # change random radian into x, y vectors and assign
            self.acc[0] = math.cos(self.brain.directions[self.brain.step])
            self.acc[1] = math.sin(self.brain.directions[self.brain.step])
            self.brain.step += 1
        else:
            self.dead = True
        self.vel[0] = self.vel[0] + self.acc[0]
        self.vel[1] = self.vel[1] + self.acc[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def update(self):
        if not (self.dead or self.reachGoal):
            self.move()
            if (self.pos[0] < 255 > 10 and self.pos[1] < 215 and self.pos[1] > 130):
                self.dead = True # dead if collide fence 1
            elif (self.pos[0] > 230 and self.pos[1] < 415 and self.pos[1] > 330):
                self.dead = True # dead if collide fence 2
            elif (self.pos[0] < 8 or self.pos[0] > self.scWidth - self.width or self.pos[1] < 8 or self.pos[1] > self.scHeight - self.height):
                self.dead = True
            elif math.hypot(self.goalX - self.pos[0], self.goalY - self.pos[1]) < 5: # distance to goal < 5 accept
                self.reachGoal = True

    def calcFitness(self):
        if self.reachGoal:
            self.fitness = 1.0/16.0 + 10000.0/(self.brain.step ** 2)
        else:
            dist = math.hypot(self.goalX - self.pos[0], self.goalY - self.pos[1])
            self.fitness = 1.0/(dist ** 2) # inverse, bees with shortest distance to goal is most fit

    def makeChild(self):
        # makes child with copy of parent's brain
        child = Bee(self.scWidth, self.scHeight, self.goalX, self.goalY)
        child.brain = self.brain.clone()
        return child
