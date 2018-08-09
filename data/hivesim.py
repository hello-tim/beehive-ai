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
        self.goal = [width/2 - 5, 40] # Goal is inside the hive

    def run(self):
        # Initialize bee population
        swarm = Swarm(1000, self.scWidth, self.scHeight, self.goal[0], self.goal[1])
        # Draw hive on back ground
        self.bg.blit(self.hive, (self.scWidth/2 - 25, 0))
        # Draw electrical fence obstacle
        self.bg.blit(self.fence, (-23, 100))
        self.bg.blit(self.fence, (205, 300))
        # Game loop
        running = True
        while running:
            # Exit loop if quit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    # Obtain clean copy of background for clearing screen
            bgcopy = pg.Surface.copy(self.bg)
            if (swarm.allDead()):
                # Genetic algorithm
                swarm.calcFitness()
                swarm.naturalSelect()
                swarm.mutate()
            else:
                swarm.update()
                swarm.show(bgcopy)
                self.sc.blit(bgcopy, (0, 0))
                pg.display.update()

if __name__ == "__main__":
    pg.init() # Initialize pygame module
    screen = pg.display.set_mode((500, 500)) # Set screen 500 x 500
    pg.display.set_caption("Hive AI Simulation")
    # Initialize app and run
    app = App(screen, 500, 500)
    app.run()
    pg.quit()
