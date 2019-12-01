# -------------------------------------------------------
#                       by oognuyh
# -------------------------------------------------------
from pygame.locals import *
import pygame as pg
import random, sys, os
# -------------------------------------------------------
pg.init()
pg.display.set_caption("maze generator using hunt and kill")
width, height = 800, 800
screen = pg.display.set_mode((width, height))
# -------------------------------------------------------
BLACK = (0, 0, 0) # outline
WHITE = (255, 255, 255) # background
GREEN = (0, 157, 0) # the ending point
RED = (157, 0, 0) # the starting point
# -------------------------------------------------------
cellsize = 40
# -------------------------------------------------------
FPS = 60
# -------------------------------------------------------
class Cell:
    def __init__(self, coord):
        self.coord = coord
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        self.is_starting_point = False
        self.is_ending_point = False
    
    def the_count_is(self):
        count = 0

        if self.up:
            count = count + 1
        if self.down:
            count = count + 1
        if self.left:
            count = count + 1
        if self.right:
            count = count + 1
        
        return count
    
    def draw(self):
        # draw a rect and outlines
        x, y = self.coord[0] * cellsize, self.coord[1] * cellsize
        
        pg.draw.rect(screen, WHITE, (x, y, cellsize, cellsize))
        if self.up:
            pg.draw.line(screen, BLACK, (x, y), (x + cellsize, y))
        if self.down:
            pg.draw.line(screen, BLACK, (x, y + cellsize), (x + cellsize, y + cellsize))
        if self.left:
            pg.draw.line(screen, BLACK, (x, y), (x, y + cellsize))
        if self.right:
            pg.draw.line(screen, BLACK, (x + cellsize, y), (x + cellsize, y + cellsize))

        if self.is_starting_point:
            pg.draw.circle(screen, RED, (x + cellsize // 2, y + cellsize // 2), cellsize // 4)
        if self.is_ending_point:
            pg.draw.circle(screen, GREEN, (x + cellsize // 2, y + cellsize // 2), cellsize // 4)
        
        
# -------------------------------------------------------
class Huntandkill:
    def __init__(self):
        self.grid = [[Cell([x, y]) for y in range(height)] for x in range(width)]
        self.gridwidth = width // cellsize
        self.gridheight = height // cellsize
        self.start = None
        self.end = None
    
    def is_valid(self, coord):
        x, y = coord
        return -1 < x and x < self.gridwidth and -1 < y and y < self.gridheight

    def has_no_target(self, coord):
        return coord == [-1, -1]

    def neighbours(self, x, y, option = True):
        killable = []
        huntable = []
        
        if self.is_valid([x + 1, y]):
            if self.grid[x + 1][y].the_count_is() == 4: # if the count of outlines is 4, this cell is wall
                killable.append([x + 1, y])
            else: # else path
                huntable.append([x + 1, y])
        if self.is_valid([x - 1, y]):
            if self.grid[x - 1][y].the_count_is() == 4:
                killable.append([x - 1, y])
            else:
                huntable.append([x - 1, y])
        if self.is_valid([x, y + 1]):
            if self.grid[x][y + 1].the_count_is() == 4:
                killable.append([x, y + 1])
            else:
                huntable.append([x, y + 1])
        if self.is_valid([x, y - 1]):
            if self.grid[x][y - 1].the_count_is() == 4:
                killable.append([x, y - 1])
            else:
                huntable.append([x, y - 1])
        
        if option:
            return killable
        else:
            return huntable

    def hunt(self):
        # hunt a cell from the top left
        # the cell is not wall and has at least one path around
        for y in range(self.gridheight):
            for x in range(self.gridwidth):
                if self.grid[x][y].the_count_is() == 4:
                    huntable = self.neighbours(x, y, False)
                    if len(huntable) > 0:
                        move_from = random.choice(huntable)
                        if move_from == [x + 1, y]: # right
                            self.grid[x][y].right = False
                            self.grid[x + 1][y].left = False
                        elif move_from == [x - 1, y]: # left
                            self.grid[x][y].left = False
                            self.grid[x - 1][y].right = False
                        elif move_from == [x, y + 1]: # down
                            self.grid[x][y].down = False
                            self.grid[x][y + 1].up = False
                        elif move_from == [x, y - 1]: # up
                            self.grid[x][y].up = False
                            self.grid[x][y - 1].down = False
                        
                        return x, y

        return -1, -1

    def kill(self, coord):
        # kill a cell randomly 
        # if the cell has no wall around, stop
        x, y = coord
        while True:
            killable = self.neighbours(x, y)
            if len(killable) == 0:
                break
            
            move_to = random.choice(killable)

            if move_to == [x + 1, y]: # right
                self.grid[x][y].right = False
                self.grid[x + 1][y].left = False
            elif move_to == [x - 1, y]: # left
                self.grid[x][y].left = False
                self.grid[x - 1][y].right = False
            elif move_to == [x, y + 1]: # down
                self.grid[x][y].down = False
                self.grid[x][y + 1].up = False
            elif move_to == [x, y - 1]: # up
                self.grid[x][y].up = False
                self.grid[x][y - 1].down = False

            x, y = move_to


    def create_points(self):
        # create the starting point and the ending point randomly
        possible_points = []

        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                if self.grid[x][y].the_count_is() == 3:
                    possible_points.append([x, y])
        
        self.start = random.choice(possible_points)
        possible_points.remove(self.start) # prevent the same point
        self.end = random.choice(possible_points)

        self.grid[self.start[0]][self.start[1]].is_starting_point = True
        self.grid[self.end[0]][self.end[1]].is_ending_point = True

    def generate(self):
        x = random.randint(0, self.gridwidth - 1)
        y = random.randint(0, self.gridheight - 1)
        
        while True:
            self.kill([x, y])

            x, y = self.hunt()
            if self.has_no_target([x, y]):
                self.create_points()
                break
        
    def draw(self):
        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                self.grid[x][y].draw()

# -------------------------------------------------------
def execute():
    generator = Huntandkill()
    generator.generate()
    
    # run
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                # terminate this program
                pg.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    # pressing the return key will regenerate the maze
                    generator = Huntandkill()
                    generator.generate()
        
        screen.fill(BLACK)
        generator.draw()
      
        pg.display.flip()
        pg.time.Clock().tick(FPS)

# -------------------------------------------------------
if __name__ == "__main__":
    execute()