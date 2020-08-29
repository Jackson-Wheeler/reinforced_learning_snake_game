import pygame


class Snake:
    def __init__(self, x, y):
        self.snake_pos = [x, y]
        self.snake_body = [[x, y], [x-10, y], [x-(2*10), y]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        # Add food object
        
    def changeDirection(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
            
    def move(self):
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

    def grow_snake_body(self, score, food_pos):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == food_pos[0] and self.snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            self.snake_body.pop()
            food_spawn = True
        return food_spawn, score
            
    def draw_snake(self, game_window, color):
        for pos in self.snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, color, pygame.Rect(pos[0], pos[1], 10, 10))
            
