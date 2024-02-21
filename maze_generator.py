import random, math
import pygame, os, sys, gc
import time
pygame.init()

WHITE, BLACK, GREY = (255,255,255), (0,0,0), (128,128,128)
PURPLE, RED, BLUE = (100,0,100), (255,0,0), (0,0,255)
GREEN, YELLOW = (0,255,0), (255,255,0)

size = (801,801)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

width = 40 # 25
cols = int(size[0] / width)
rows = int(size[1] / width)
stack = []
traversed_path=[]
solved=False

class Cell():
    def __init__(self,x,y):
        global width
        self.x, self.y = x * width, y * width
        
        # We keep a track of which squares we've visited and which we have not.
        self.visited, self.current = False, False        
        self.walls = [True,True,True,True] # top , right , bottom , left
        
        # neighbors
        self.neighbors = []
        self.top, self.right, self.bottom, self.left = 0, 0, 0, 0        
        self.next_cell = 0
    
    def get_rect(self):
        return pygame.rect.Rect((self.x,self.y),(width,width))
    
    def draw(self, bg=WHITE, fill=True, small=False):
        if self.visited:
            if not fill:
                pygame.draw.rect(screen,bg,(self.x,self.y,width,width), width//4)
            else:
                if small:
                    pygame.draw.rect(screen,bg,(self.x+width//4,self.y+width//4,width-width//2,width-width//2))
                else:
                    pygame.draw.rect(screen,bg,(self.x,self.y,width,width))   
                    
            if self.walls[0]:
                pygame.draw.line(screen,GREY,(self.x,self.y),((self.x + width),self.y),1) # top
            if self.walls[1]:
                pygame.draw.line(screen,GREY,((self.x + width),self.y),((self.x + width),(self.y + width)),1) # right
            if self.walls[2]:
                pygame.draw.line(screen,GREY,((self.x + width),(self.y + width)),(self.x,(self.y + width)),1) # bottom
            if self.walls[3]:
                pygame.draw.line(screen,GREY,(self.x,(self.y + width)),(self.x,self.y),1) # left
    
    def checkNeighbors(self):
        if int(self.y / width) - 1 >= 0:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]
        if int(self.x / width) - 1 >= 0:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]
        
        if self.top != 0:
            if self.top.visited == False:
                self.neighbors.append(self.top)
        if self.right != 0:
            if self.right.visited == False:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if self.bottom.visited == False:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if self.left.visited == False:
                self.neighbors.append(self.left)
        
        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(0,len(self.neighbors))]
            return self.next_cell
        else:
            return False


# When travelling to this new square we remove the wall to the new square and this is what carves out the maze.
def removeWalls(current_cell,next_cell):
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)
    if x == -1: # right of current
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1: # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1: # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1: # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False
        
# -------- Draw the maze -----------
def draw_maze(flip=True):
    screen.fill(GREY)
    for y in range(rows):
        for x in range(cols):
            grid[y][x].draw()
    if flip:
        pygame.display.flip()
        clock.tick(60)
        
# -------- Generate Maze -----------
def generate_maze():
    global current_cell, next_cell, player, exit_cell, traversed_path
    maze_generated = False
    while not maze_generated:
        # print("Stack depth", len(stack))
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        current_cell.visited = True
        current_cell.current = True
        
        # Examining all the neigbours of the current square and 
        # selecting (at random) any of the unvisited squares, moving 
        # into it, then mark this new location as also visited.
        next_cell = current_cell.checkNeighbors()
        
        if next_cell != False:
            current_cell.neighbors = []
            stack.append(current_cell)
            removeWalls(current_cell,next_cell)
            current_cell.current = False
            current_cell = next_cell
        elif len(stack) > 0:
            # No next_cell, dead end! Take a step backwards to see if there  
            # are any unvisted neigbours from the last visited square
            current_cell.current = False
            current_cell = stack.pop()
        elif len(stack) == 0:
            draw_maze()
            maze_generated=True

    # Define Entry and Exit Cells

    player = grid[0][random.randrange(0,cols)]
    exit_cell = grid[rows-1][random.randrange(0,cols)]
    
    print("rows", rows, "cols", cols)
    print("player rect", player.get_rect())
    print("exit rect", exit_cell.get_rect())
    print("player.x", player.x//width, "player.y", player.y//width)
    print("exit_cell.x", exit_cell.x//width, "exit_cell.y", exit_cell.y//width)
    traversed_path.append(player) # First path cell
    traversed_path[0].draw(GREEN, False)
    exit_cell.draw(YELLOW, False)
    pygame.image.save(screen,"maze.png")
    
# Initialize empty grid
grid = []
for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x,y))

current_cell = grid[0][0]
next_cell = 0

generate_maze()
