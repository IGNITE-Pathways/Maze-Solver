**maze_generator.py** uses recursive backtracking to create a maze. 

We basically mark cells as we visit them and move through the grid, randomly selecting unvisited neighbors until we reach a dead end. Then, we backtrack to find an unvisited path, continuing until all cells are visited. 

**maze_solver.py** uses a recursive algorithm and random choice selection to solve a maze. 
The player automatically navigates through a maze, updating the display to show the current path taken until the exit is reached or the player gets stuck. 

Read more at https://www.ignitepathways.org/post/solving-a-maze

<img width="1289" alt="Maze" src="https://static.wixstatic.com/media/9c8449_eb48a8a9bee74ecb9daa1807a492e8c6~mv2.png/v1/fill/w_801,h_801,al_c,q_90,enc_auto/9c8449_eb48a8a9bee74ecb9daa1807a492e8c6~mv2.png">
