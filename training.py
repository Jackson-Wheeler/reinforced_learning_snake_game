from snake import *
import pygame, sys, time, random
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

GRAPHICS = True

# Window size
FRAME_DIM = (780, 420)
# Initialise game window
if GRAPHICS:
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
        dist_straight_body = min(distances_to_body['UP'])
        dist_left_body = min(distances_to_body['LEFT'])
        dist_right_body = min(distances_to_body['RIGHT'])
        
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
        dist_straight_body = min(distances_to_body['DOWN'])
        dist_left_body = min(distances_to_body['RIGHT'])
        dist_right_body = min(distances_to_body['LEFT'])
        
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
        dist_straight_body = min(distances_to_body['LEFT'])
        dist_left_body = min(distances_to_body['DOWN'])
        dist_right_body = min(distances_to_body['UP'])
        
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
        dist_straight_body = min(distances_to_body['RIGHT'])
        dist_left_body = min(distances_to_body['UP'])
        dist_right_body = min(distances_to_body['DOWN'])
        
    # Obstacles distances
    dist_straight_obstacle = min(dist_straight_wall, dist_straight_wall)
    dist_left_obstacle = min(dist_left_wall, dist_left_wall)
    dist_right_obstacle = min(dist_right_wall, dist_right_wall)
            
    return [dist_straight_obstacle, dist_straight_food,
            dist_left_obstacle, dist_left_food,
            dist_right_obstacle, dist_right_food]#,
            #snake.time_in_current_size]

def get_distances_to_body(snake, head_x, head_y):
    tail_distances = {'UP': [head_y], 'DOWN': [FRAME_DIM[1] - head_y],
                      'LEFT': [head_x], 'RIGHT': [FRAME_DIM[0] - head_x]}
    # for each block of the snake body
    for x, block_pos in enumerate(snake.snake_body):
        if x == 0:
            continue # index 0 has pos of snake head
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
        x = random.randrange(0, FRAME_DIM[0], 10)
        y = random.randrange(0, FRAME_DIM[1], 10)
        length = 200
        snakes.append(Snake(x, y, length, FRAME_DIM))
        
    num_out_bounds = 0
    num_hit_themself = 0
    num_run_out_time = 0

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
            # if x == 0:
            #     print(snake.direction, snake.snake_pos)
            #     print(inputs)            
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
        if GRAPHICS:
            GAME_WINDOW.fill(BLACK)
            for snake in snakes:
                snake.draw_snake_and_food(GAME_WINDOW)

        # Snake Losing Conditions
        for x, snake in enumerate(snakes):
            try:
                # Getting out of bounds
                if snake.snake_pos[0] < 0 or snake.snake_pos[0] > FRAME_DIM[0]-10:
                    ge[x].fitness -= 200 #removing fitness for crossing x boundaries
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                    num_out_bounds += 1
                elif snake.snake_pos[1] < 0 or snake.snake_pos[1] > FRAME_DIM[1]-10:
                    ge[x].fitness -= 200 #removing fitness for crossing y boundaries
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                    num_out_bounds += 1
                # Touching the snake body
                for block in snake.snake_body[1:]:
                    if snake.snake_pos[0] == block[0] and snake.snake_pos[1] == block[1]:
                        ge[x].fitness -= 200 #removing fitness for hitting a part of the body
                        snakes.pop(x)
                        ge.pop(x)
                        nets.pop(x)
                        num_hit_themself += 1
                        # if len(snakes) < 10:
                        #     print("Hit Myself") 
                # Too long with same size
                min_time_threshold = 1.2 * (FRAME_DIM[0]/10 + FRAME_DIM[1]/10)
                time_threshold = min_time_threshold + (2 * length)
                if snake.time_in_current_size > time_threshold:
                    ge[x].fitness -= 200 # remove fitness
                    snakes.pop(x)
                    ge.pop(x)
                    nets.pop(x)
                    num_run_out_time += 1
                    # if len(snakes) < 10:
                    #     print("Ran out of Time")
                    
            except IndexError:
                pass
        
        # print(len(snakes))
        # if len(snakes) < 50:
        #     max_g = -10000000
        #     for g in ge:
        #         if g.fitness > max_g:
        #             max_g = g.fitness
        #     print(max_g)
                
        # Check if no more snakes left
        if len(snakes) == 0:
            running = False
            print("Out of Bounds:", num_out_bounds)
            print("Hit Themself:", num_hit_themself)
            print("Ran out of Time:", num_run_out_time)
            
        # # Refresh game screen
        if GRAPHICS:
            pygame.display.update()
        # # Refresh rate
        # fps_controller.tick(DIFFICULTY)



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
    winner = pop.run(train, 50)
    print('\nBest genome:\n{!s}'.format(winner))
    # Save best genome
    pickle.dump(pop, open('best_genome.p', "wb"))
    
def main():
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'configuration.txt')
    run(config_path)

if __name__ == "__main__":
    main()
    
