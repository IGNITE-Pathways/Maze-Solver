**maze_generator.py** uses recursive backtracking to create a maze. 

We basically mark cells as we visit them and move through the grid, randomly selecting unvisited neighbors until we reach a dead end. Then, we backtrack to find an unvisited path, continuing until all cells are visited. 

**maze_solver.py** uses a recursive algorithm and random choice selection to solve a maze. 
The player automatically navigates through a maze, updating the display to show the current path taken until the exit is reached or the player gets stuck. 
