Requires Pygame
Run GameOfLife.py and ta-da!

The rules are the following:
If cell is alive, it continues alive if double of alive cells minus 4 is greater than 5
If cell is dead, it turns alive if 3 or 6 cells around it are alive or has 8 cells around it

In the game:

Press A to fill the board randomly;
Press SPACE to start the game;
Press Q to manually give the next step;
Click on a black square to make it infected


Change the values of variables
SINGER_POPULARITY
MEDIA_DIVULGATION

in range 1...10  in GameOfLife.py to modify contamination and cure rates

Based on http://www.pygame.org/project-John+Conway%27s+Game+of+Life-2899-.html, with optimizations and corrections

