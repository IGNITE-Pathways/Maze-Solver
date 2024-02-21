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

width = 20 # 25
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

# Initialize empty grid
grid = []
for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x,y))

current_cell = grid[0][0]
next_cell = 0

# Draw the maze
def draw_maze(flip=True):
    screen.fill(GREY)
    for y in range(rows):
        for x in range(cols):
            grid[y][x].draw()
    if flip:
        pygame.display.flip()
        clock.tick(60)
    

def draw_path(onebefore, before, current):
    prev_x = before.x + width//2
    prev_y = before.y + width//2
    current_x = current.x + width//2
    current_y = current.y + width//2
    if onebefore.x == current.x:
        # moving vertically
        prev_x = onebefore.x + width//2
        prev_y = onebefore.y if onebefore.y > current.y else onebefore.y + width 
        current_y = current.y if onebefore.y < current.y else current.y + width
    elif onebefore.y == current.y:
        # moving horizontally
        prev_y = onebefore.y + width//2
        prev_x = onebefore.x if onebefore.x > current.x else onebefore.x + width 
        current_x = current.x if onebefore.x < current.x else current.x + width
    else:
        # turning
        if before.x == current.x:
            # moving vertically and turning
            prev_y = onebefore.y + width//2
            prev_x = onebefore.x if onebefore.x > current.x else onebefore.x + width 
            current_y = current.y if onebefore.y < current.y else current.y + width
        else:
            prev_x = onebefore.x + width//2
            prev_y = onebefore.y if onebefore.y > current.y else onebefore.y + width 
            current_x = current.x if onebefore.x < current.x else current.x + width

    if current_x == prev_x or current_y == prev_y:
        pygame.draw.line(screen,BLUE,(prev_x,prev_y),(current_x,current_y),3) # top 
    else:  
        starting_pi = 0
        if current_x > prev_x:
            if current_y > prev_y:
                if before.y == current.y:
                    # down right 
                    starting_pi = math.pi
                    prev_y = prev_y - width/2
                else:
                    # right down
                    prev_x = prev_x - width/2                    
            else:
                if before.y == current.y:
                    # up right
                    starting_pi = math.pi/2
                    prev_y = prev_y - width/2
                else:
                    # right up
                    prev_y = prev_y - width
                    prev_x = prev_x - width/2       
                    starting_pi = 3*math.pi/2
        else:
            if current_y > prev_y:
                if before.y == current.y:
                    # down left 
                    prev_y = prev_y - width/2
                    prev_x = prev_x - width      
                    starting_pi = 3*math.pi/2
                else:
                    # left down
                    prev_x = prev_x - width/2       
                    starting_pi = math.pi/2
            else:
                if before.y == current.y:
                    # up left 
                    prev_y = prev_y - width/2
                    prev_x = prev_x - width    
                    starting_pi = 0
                else:
                    # left up
                    prev_y = prev_y - width
                    prev_x = prev_x - width/2       
                    starting_pi = math.pi

        pygame.draw.arc(screen,BLUE,[prev_x-1, prev_y-1, width+2, width+2], starting_pi, starting_pi + math.pi/2,  3)
            
 
def draw_path_taken():
    for i in range(1,len(traversed_path)-1):
        draw_path(traversed_path[i-1], traversed_path[i], traversed_path[i+1])            
        
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

generate_maze()

last_traversed_cell = None

os.environ['SDL_VIDEO_CENTERED'] = '1'  # center SCREEN

def manual_play():   
    global player, last_traversed_cell
    done=False
    while not done:
        clock.tick(60)

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_LEFT] and player.walls[3] == False:
                    player = grid[player.y//width][player.x//width - 1] #player.move(-2, 0)
                    # print("K_LEFT", "player.x", player.x//width, "player.y", player.y//width)
                elif key[pygame.K_RIGHT] and player.walls[1] == False:
                    player = grid[player.y//width][player.x//width + 1]
                    # print("K_RIGHT", "player.x", player.x//width, "player.y", player.y//width)
                elif key[pygame.K_UP] and player.walls[0] == False:
                    player = grid[player.y//width - 1][player.x//width] #player.move(0, -2)
                    # print("K_UP", "player.x", player.x//width, "player.y", player.y//width)
                elif key[pygame.K_DOWN] and player.walls[2] == False:
                    player = grid[player.y//width + 1][player.x//width]
                    # print("K_DOWN", "player.x", player.x//width, "player.y", player.y//width)
                if player != traversed_path[len(traversed_path)-1]:
                    if len(traversed_path) > 2:
                        last_traversed_cell=traversed_path[len(traversed_path)-2]
                    if last_traversed_cell is not None and last_traversed_cell == player:
                        traversed_path.pop()
                    else:
                        traversed_path.append(player)
            
        draw_maze(flip=False)
        traversed_path[0].draw(GREEN, False)
        exit_cell.draw(YELLOW)
        player.draw(GREEN, True, True)
        draw_path_taken()
        pygame.display.flip()
        
        if player.get_rect().colliderect(exit_cell.get_rect()):
            exit_cell.draw(BLACK)
            pygame.display.flip()
            print("WON!")
            pygame.image.save(screen,"maze_solved.png")
            pygame.quit()
            sys.exit()
    
def get_previous_cell_side(previous, p):
    # 0,1,2,3 for top , right , bottom , left
    if previous.y + width == p.y:
        return 0
    elif previous.y == p.y + width:
        return 2
    elif previous.x == p.x + width:
        return 1 # previous is right of p 
    else:
        return 3 # previous left of p
        
def solve_maze(p,previous, stack=0):
    global player, last_traversed_cell
    traversed_path.append(p)
    
    time.sleep(.02)
    draw_maze(flip=False)
    traversed_path[0].draw(GREEN, False)
    exit_cell.draw(YELLOW, False)
    player.draw(GREEN, True, True)
    draw_path_taken()
    pygame.display.flip()
    
    # print(stack, "Player", p.x//width, p.y//width)  
    if p.get_rect().colliderect(exit_cell.get_rect()):
        return True
    walls_list = [0,1,2,3]
    for i in range(len(p.walls)):
        random_wall = random.choice(walls_list)
        walls_list.remove(random_wall)
        np = None
        if p.walls[random_wall] == False:
            coming_from = get_previous_cell_side(previous,p)
            # print(stack, "coming_from", coming_from)
            # no wall
            if random_wall == 3 and coming_from != 3:
                np = grid[p.y//width][p.x//width - 1] 
            elif random_wall == 1 and coming_from != 1:
                np = grid[p.y//width][p.x//width + 1]
            elif random_wall == 0 and coming_from != 0:
                np = grid[p.y//width - 1][p.x//width]
            elif random_wall == 2 and coming_from != 2:
                np = grid[p.y//width + 1][p.x//width]
            if np is not None:
                # print(stack, "Next Player", np.x//width, np.y//width)  
                player = np
                if solve_maze(player, p, stack + 1):
                    return True
            
    traversed_path.pop()
    gc.collect()
    return False
    
def auto_play():   
    global player, last_traversed_cell, solved
    done=False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # player
        if not solved:
            if solve_maze(player, player):
                # print("Solved")
                solved=True
                pygame.image.save(screen,"maze_solved.png")
            else:
                print("Got Stuck")

        draw_maze(flip=False)
        traversed_path[0].draw(GREEN, False)
        exit_cell.draw(YELLOW, False)
        player.draw(GREEN, True, True)
        draw_path_taken()
        pygame.display.flip()
        
auto_play()
