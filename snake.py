import pygame
import random

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
        self.direction = 'RIGHT'
        self.change_to = self.direction
        # Score
        self.score = 0
        # Add food object
        self.food = Food(FRAME_DIM)
        
    def move(self, genome):
        genome.fitness +=1
        self.changeDirection()
        self.change_pos()
        self.grow_snake_body(genome)
        # Spawn Food
        self.food.spawn_food()
                
    # Moving
    def changeDirection(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
            
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
            genome.fitness +=20
            self.food.food_spawn = False
        else:
            self.snake_body.pop()
            self.food.food_spawn = True
                
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
