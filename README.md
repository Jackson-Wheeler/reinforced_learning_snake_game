Watch PROJECT_VIDEO for a 3 minute overview of the project!

# Reinforced Learning Snake Game
Our program utilized the NEAT-python library and its reinforced learning to train the program how to play the snake game. It is not complete, as the snake has not learned how not to hit itself, but the snake has still learned a lot and can get pretty far! Important Note: The snake game itself was NOT created by us, we borrowed the snake game code from rajatdiptabiswas/snake-pygame on Github. This was done so that we could focus our project on the reinforced learning aspect of this program.

## Requirements
The packages that need to be install are as followed:
1. neat-python
2. pygame

Run each of the following in the terminal to install the packages
```
pip3 install neat-python
pip3 install pygame
```

# Running
To run the program type the following from the terminal
```
python3 main.py
```
Then, you will be asked to input what type of mode you would like to run.

Human- play the classic snake game as a human! Using the arrow keys to play.
Training- Run the training of the snake population. This will run many snakes at the same time. The final generation will be saved to the local file 'best_genome.p'.
AI- This will be run using the generation saved into the local file 'best_genome.p'. It will take the best snake from that snake population and run it on the screen. If the snake happens to die, then it will reboot and run that same snake again, but with a different random starting position and random food positions.


## Developed By
Our reinforced learning work and implementation of the neat-python library.
* **Jackson Wheeler and Sidharth Srinath**

## Credit
As stated above credit for the basic snake game code (playing the game normally), as seen in human.py, goes 100% to rajatdiptabiswas/snake-pygame on Github. This code was borrowed so that we could focus on implementing reinforced learning. In training.py and ai.py his code was refractured and altered to fit our need, but much of his code governing the basic functionality of the game remained the same. 
