import pygame as pg
from swarm import Swarm

class App():
    def __init__(self, screen, width, height):
        self.scWidth = width
        self.scHeight = height
        self.bg = pg.image.load("resources/bg.png") # 500 x 500
        self.hive = pg.image.load("resources/hive.png") # 50 x 53
        self.fence = pg.image.load("resources/fence.png") # 320 x 150
        self.sc = screen
        self.goal = [width/2 - 5, 40] # goal is inside the hive

    def run(self):
        # initialize bee population
        swarm = Swarm(1000, self.scWidth, self.scHeight, self.goal[0], self.goal[1])
        # draw hive on back ground
        self.bg.blit(self.hive, (self.scWidth/2 - 25, 0))
        # draw electrical fence obstacle
        self.bg.blit(self.fence, (-23, 100))
        self.bg.blit(self.fence, (205, 300))
        # game loop
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            bgcopy = pg.Surface.copy(self.bg) # obtain clean copy for clearing
            if (swarm.allDead()):
                # genetic algorithm
                swarm.calcFitness()
                swarm.naturalSelect()
                swarm.mutate()
            else:
                swarm.update()
                swarm.show(bgcopy)
                self.sc.blit(bgcopy, (0, 0)) # draw background on screen
                pg.display.update()

if __name__ == "__main__":
    pg.init() # initialize pygame module
    screen = pg.display.set_mode((500, 500)) # set screen 500 x 500
    pg.display.set_caption("Hive AI Simulation")
    # initialize app
    app = App(screen, 500, 500)
    app.run()
    pg.quit()
