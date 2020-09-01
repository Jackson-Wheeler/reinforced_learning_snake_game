from snake import *
import pygame, sys, time, random
import neat
import os

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
        print('[!] Had ',check_errors[1],' errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

def get_inputs(x, snake):
    head_x, head_y = snake.snake_pos
    food_x, food_y = snake.food.food_pos
    dist_to_food_x = head_x - food_x
    dist_to_food_y = head_y - food_y
    snakebody = snake.snake_body[1:len(snake.snake_body)]


    if snake.direction == 'UP':
        # Walls
        dist_straight_wall = head_y
        dist_left_wall = head_x
        dist_right_wall = FRAME_DIM[0] - head_x
        # Food 
        dist_straight_food = dist_to_food_y
        dist_left_food = dist_to_food_x
        dist_right_food = -dist_to_food_x
        
    elif snake.direction == 'DOWN':
        # Walls
        dist_straight_wall = FRAME_DIM[1] - head_y
        dist_left_wall = FRAME_DIM[0] - head_x
        dist_right_wall = head_x
        # Food 
        dist_straight_food = -dist_to_food_y
        dist_left_food = -dist_to_food_x
        dist_right_food = dist_to_food_x
        
    elif snake.direction == 'LEFT':
        # Walls
        dist_straight_wall = head_x
        dist_left_wall = FRAME_DIM[1] - head_y
        dist_right_wall = head_y
        # Food 
        dist_straight_food = dist_to_food_x
        dist_left_food = -dist_to_food_y
        dist_right_food = dist_to_food_y
        
    elif snake.direction == 'RIGHT':
        # Walls
        dist_straight_wall = FRAME_DIM[0] - head_x
        dist_left_wall = head_y
        dist_right_wall = FRAME_DIM[1] - head_y
        # Food 
        dist_straight_food = -dist_to_food_x
        dist_left_food = dist_to_food_y
        dist_right_food = -dist_to_food_y
    
    return [dist_straight_wall, dist_straight_food, 
            dist_left_wall, dist_left_food,
            dist_right_wall, dist_right_food]
    
# Main
def train(genomes,config):
    # Check for errors
    check_for_errors()

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Create object lists
    snakes = []
    ge = []
    nets = []
    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        snakes.append(Snake(random.randrange(0,FRAME_DIM[0],10), random.randrange(0,FRAME_DIM[1],10), FRAME_DIM))

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
                snake.move('straight', ge[x]) # Keep same direction
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
                    ge[x].fitness -= 10 #removing fitness for crossing x boundaries
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                elif snake.snake_pos[1] < 0 or snake.snake_pos[1] > FRAME_DIM[1]-10:
                    ge[x].fitness -= 10 #removing fitness for crossing y boundaries
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                # Touching the snake body
                for block in snake.snake_body[1:]:
                    if snake.snake_pos[0] == block[0] and snake.snake_pos[1] == block[1]:
                        ge[x].fitness -= 10 #removing fitness for hitting a part of the body
                        snakes.pop(x)
                        ge.pop(x)
                        nets.pop(x)
                # Too long with same size
                if snake.time_in_current_size > 150:
                    ge[x].fitness -= 10 # remove fitness
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                    
            except IndexError:
                pass

        # Check if no more snakes left
        if len(snakes) == 0:
            running = False
            print("Snake Died")

        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(DIFFICULTY)


def run(config_path):
    # Upload the config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)
    # Create a population
    pop = neat.Population(config)
    # Print population
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    # Get the winning genome from the play function
    winner = pop.run(train, 70)


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'configuration.txt')
    run(config_path)
