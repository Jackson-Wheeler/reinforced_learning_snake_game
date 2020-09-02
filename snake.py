import pygame
import random
import math

# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

class Snake:
    def __init__(self, x, y, FRAME_DIM):
        # Snake pos/body
        self.snake_pos = [x, y]
        self.snake_body = [[x, y], [x-10, y], [x-(2*10), y]]
        # Direction
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.change_to = self.direction
        # Score
        self.score = 0
        # Add food object
        self.food = Food(FRAME_DIM)
        self.time_in_current_size = 0

    # Moving
    def move(self, turn, genome):
        # Old dist
        old_distx, old_disty = self.distance()
        # Move
        self.turn(turn)
        self.change_pos()
        self.grow_snake_body(genome)
        # Spawn Food
        self.food.spawn_food()
        # Check distance to food
        self.checkDist(genome, old_distx, old_disty)

    def turn(self, turn):
        all_dir = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        # Turn
        if turn == 'straight':
            pass # keep same direction
        elif turn == 'left':
            curr_dir_idx = all_dir.index(self.direction)
            new_dir_idx = curr_dir_idx - 1  # move left in list
            if new_dir_idx < 0: # if out of bounds
                new_dir_idx == 3
            self.direction = all_dir[new_dir_idx]
        elif turn == 'right':
            curr_dir_idx = all_dir.index(self.direction)
            new_dir_idx = curr_dir_idx - 1 # move right in list
            if new_dir_idx > 3: # if out of bounds
                new_dir_idx == 0
            self.direction = all_dir[new_dir_idx]
                
    def change_pos(self):
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10
    
    def grow_snake_body(self, genome):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food.food_pos[0] and self.snake_pos[1] == self.food.food_pos[1]:
            self.score += 1
            genome.fitness += 100
            self.time_in_current_size = 0
            self.food.food_spawn = False
        else:
            self.snake_body.pop()
            genome.fitness -= 0.1 # loses points longer it stays on board
            self.time_in_current_size += 1
            self.food.food_spawn = True

    def checkDist(self, genome, old_distx, old_disty):
        new_distx, new_disty = self.distance()
        # print("Before:", genome.fitness)
        if self.direction == 'UP' or self.direction == 'DOWN':
            if new_disty != 0:
                if new_disty < old_disty:
                    genome.fitness += 1.5/new_disty
                    # print("New:", genome.fitness, "; Added", 1.0/new_disty)
                else:
                    genome.fitness -= 2.0/new_disty
                    # print("New:", genome.fitness, "; Subtracted", 1.5/new_disty)
        elif self.direction == 'LEFT' or self.direction == 'RIGHT':
            if new_distx != 0:
                if new_distx < old_distx:
                    genome.fitness += 1.5/new_distx
                    # print("New:", genome.fitness, "; Added", 1.0/new_disty)
                else:
                    genome.fitness -= 2.0/new_distx
                    # print("New:", genome.fitness,"; Subtracted", 1.5/new_disty)

    def distance(self):
        xvals = (self.snake_pos[0],self.food.food_pos[0])
        yvals = (self.snake_pos[1],self.food.food_pos[1])
        distx = abs(xvals[0]-xvals[1])
        disty = abs(yvals[0]-yvals[1])
        #totalDist = math.sqrt((disty) ** 2 + (disty) ** 2)
        return distx, disty

    def get_distances_to_body(self, head_x, head_y):
        tail_distances = {'UP': [0], 'DOWN': [0], 'LEFT': [0], 'RIGHT': [0]}
        # for each block of the snake body
        for x, block_pos in enumerate(self.snake_body):
            if x == 0:
                continue  # index 0 has pos of snake head
            # UP/DOWN (x-value equal)
            if block_pos[0] == head_x:
                # UP
                if block_pos[1] < head_y:
                    tail_distances['UP'].append(head_y - block_pos[1])
                # Down
                elif block_pos[1] > head_y:
                    tail_distances['DOWN'].append(block_pos[1] - head_y)
            # Right/Left (y-value equal)
            elif block_pos[1] == head_y:
                # Right
                if block_pos[0] > head_x:
                    tail_distances['RIGHT'].append(block_pos[0] - head_x)
                # Left
                elif block_pos[0] < head_x:
                    tail_distances['LEFT'].append(head_x - block_pos[1])
        return tail_distances

    # Draw
    def draw_snake_and_food(self, GAME_WINDOW):
        # Snake
        for pos in self.snake_body:
            pygame.draw.rect(GAME_WINDOW, GREEN,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        # Food
        self.food.draw_food(GAME_WINDOW)
            

class Food:
    def __init__(self, FRAME_DIM):
        self.FRAME_DIM = FRAME_DIM
        self.food_pos = [random.randrange(
            1, (self.FRAME_DIM[0]//10)) * 10, random.randrange(1, (self.FRAME_DIM[1]//10)) * 10]
        self.food_spawn = True
        
    def spawn_food(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(
                1, (self.FRAME_DIM[0]//10)) * 10, random.randrange(1, (self.FRAME_DIM[1]//10)) * 10]
        self.food_spawn = True

    def draw_food(self, GAME_WINDOW):
        pygame.draw.rect(GAME_WINDOW, WHITE, pygame.Rect(
            self.food_pos[0], self.food_pos[1], 10, 10))
