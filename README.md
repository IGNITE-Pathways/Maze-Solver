**maze_generator.py** uses recursive backtracking to create a maze. 

We basically mark cells as we visit them and move through the grid, randomly selecting unvisited neighbors until we reach a dead end. Then, we backtrack to find an unvisited path, continuing until all cells are visited. 
