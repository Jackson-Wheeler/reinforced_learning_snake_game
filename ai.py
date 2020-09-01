from snake import *
import pygame
import sys
import time
import random
import neat
import os
import pickle

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 25

# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

SCORE = 0

# Window size
FRAME_DIM = (780, 420)
# Initialise game window
pygame.display.set_caption('Snake Eater')
GAME_WINDOW = pygame.display.set_mode((FRAME_DIM[0], FRAME_DIM[1]))


# Other Functions
def check_for_errors():
    # Checks for errors encounteRED
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print('[!] Had ', check_errors[1],
              ' errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')


def get_inputs(x, snake):
    head_x, head_y = snake.snake_pos
    food_x, food_y = snake.food.food_pos
    dist_to_food_x = head_x - food_x
    dist_to_food_y = head_y - food_y
    # Body Distances
    distances_to_body = get_distances_to_body(snake, head_x, head_y)

    # Walls and Food
    if snake.direction == 'UP':
        # Walls
        dist_straight_wall = head_y
        dist_left_wall = head_x
        dist_right_wall = FRAME_DIM[0] - head_x
        # Food
        dist_straight_food = dist_to_food_y
        dist_left_food = dist_to_food_x
        dist_right_food = -dist_to_food_x
        # Body distances
        dist_straight_body = max(distances_to_body['UP'])
        dist_left_body = max(distances_to_body['LEFT'])
        dist_right_body = max(distances_to_body['RIGHT'])

    elif snake.direction == 'DOWN':
        # Walls
        dist_straight_wall = FRAME_DIM[1] - head_y
        dist_left_wall = FRAME_DIM[0] - head_x
        dist_right_wall = head_x
        # Food
        dist_straight_food = -dist_to_food_y
        dist_left_food = -dist_to_food_x
        dist_right_food = dist_to_food_x
        # Body distances
        dist_straight_body = max(distances_to_body['DOWN'])
        dist_left_body = max(distances_to_body['RIGHT'])
        dist_right_body = max(distances_to_body['LEFT'])

    elif snake.direction == 'LEFT':
        # Walls
        dist_straight_wall = head_x
        dist_left_wall = FRAME_DIM[1] - head_y
        dist_right_wall = head_y
        # Food
        dist_straight_food = dist_to_food_x
        dist_left_food = -dist_to_food_y
        dist_right_food = dist_to_food_y
        # Body distances
        dist_straight_body = max(distances_to_body['LEFT'])
        dist_left_body = max(distances_to_body['DOWN'])
        dist_right_body = max(distances_to_body['UP'])

    elif snake.direction == 'RIGHT':
        # Walls
        dist_straight_wall = FRAME_DIM[0] - head_x
        dist_left_wall = head_y
        dist_right_wall = FRAME_DIM[1] - head_y
        # Food
        dist_straight_food = -dist_to_food_x
        dist_left_food = dist_to_food_y
        dist_right_food = -dist_to_food_y
        # Body distances
        dist_straight_body = max(distances_to_body['RIGHT'])
        dist_left_body = max(distances_to_body['UP'])
        dist_right_body = max(distances_to_body['DOWN'])

    return [dist_straight_wall, dist_straight_food, dist_straight_body,
            dist_left_wall, dist_left_food, dist_left_body,
            dist_right_wall, dist_right_food, dist_right_body,
            snake.time_in_current_size]


def get_distances_to_body(snake, head_x, head_y):
    tail_distances = {'UP': [0], 'DOWN': [0], 'LEFT': [0], 'RIGHT': [0]}
    # for each block of the snake body
    for x, block_pos in enumerate(snake.snake_body):
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


# Main
def ai_play(genomes, config):
    # Check for errors
    check_for_errors()

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Create object lists
    snakes = []
    ge = []
    nets = []
    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        snakes.append(Snake(random.randrange(
            0, FRAME_DIM[0], 10), random.randrange(0, FRAME_DIM[1], 10), FRAME_DIM))

    # Main logic
    running = True
    while running:
        for event in pygame.event.get():
            # Quit Functionality
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # getting output from neural networks
        for x, snake in enumerate(snakes):

            inputs = get_inputs(x, snake)
            # [dist_straight_wall, dist_straight_food, dist_straight_tail, dist_left_wall,
            # dist_left_food, dist_left_tail, dist_right_wall, dist_right_food, dist_right_tail]

            outputs = nets[x].activate(inputs)
            output = outputs.index(max(outputs))

            #mapping output to direction 0 = straignt, 1 = turn_right, 2 = turn_left
            if output == 0:
                snake.move('straight', ge[x])  # Keep same direction
            elif output == 1:
                snake.move('left', ge[x])
            elif output == 2:
                snake.move('right', ge[x])

        # Draw
        GAME_WINDOW.fill(BLACK)
        for snake in snakes:
            snake.draw_snake_and_food(GAME_WINDOW)

        # Snake Losing Conditions
        for x, snake in enumerate(snakes):
            try:
                # Getting out of bounds
                if snake.snake_pos[0] < 0 or snake.snake_pos[0] > FRAME_DIM[0]-10:
                    # removing fitness for crossing x boundaries
                    ge[x].fitness -= 200
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                elif snake.snake_pos[1] < 0 or snake.snake_pos[1] > FRAME_DIM[1]-10:
                    # removing fitness for crossing y boundaries
                    ge[x].fitness -= 200
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                # Touching the snake body
                for block in snake.snake_body[1:]:
                    if snake.snake_pos[0] == block[0] and snake.snake_pos[1] == block[1]:
                        # removing fitness for hitting a part of the body
                        ge[x].fitness -= 200
                        # print("Snake Hit Itself. Dir:", snake.direction,
                        #       "; End Pos:", snake.snake_pos, "; Body", snake.snake_body)
                        # print(inputs)
                        snakes.pop(x)
                        ge.pop(x)
                        nets.pop(x)

            except IndexError:
                pass

        # Check if no more snakes left
        if len(snakes) == 0:
            running = False
            print("Snakes Died")

        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(DIFFICULTY)


def run(config_path):
    # Upload the config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # Load Population from 
    pop = pickle.load(open('best_genome.p', "rb"))
    # Run the game
    pop.run(ai_play, 70)
    # Save best genome


def main():
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'configuration.txt')
    run(config_path)


if __name__ == "__main__":
    main()
