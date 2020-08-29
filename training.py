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

def get_key_pressed(event):
    key_pressed = None
    # Whenever a key is pressed down
    if event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if event.key == pygame.K_UP or event.key == ord('w'):
            key_pressed = 0
            #snake.change_to = 'UP'
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            key_pressed = 1
            #snake.change_to = 'DOWN'
        elif event.key == pygame.K_LEFT or event.key == ord('a'):
            key_pressed = 2
            #snake.change_to = 'LEFT'
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            key_pressed = 3
            #snake.change_to = 'RIGHT'
        # Esc -> Create event to quit the game
        # if event.key == pygame.K_ESCAPE:
        #     pygame.event.post(pygame.event.Event(pygame.QUIT))
    return key_pressed

# def game_over():
#     my_font = pygame.font.SysFont('times new roman', 90)
#     game_over_surface = my_font.render('YOU DIED', True, RED)
#     game_over_rect = game_over_surface.get_rect()
#     game_over_rect.midtop = (FRAME_DIM[0]/2, FRAME_DIM[1]/4)
#     GAME_WINDOW.fill(BLACK)
#     GAME_WINDOW.blit(game_over_surface, game_over_rect)
#     show_score(0, RED, 'times', 20)
#     pygame.display.flip()
#     time.sleep(3)
#     pygame.quit()
#     sys.exit()
#
# def show_score(choice, color, font, size):
#     score_font = pygame.font.SysFont(font, size)
#     score_surface = score_font.render('Score : ' + str(score), True, color)
#     score_rect = score_surface.get_rect()
#     if choice == 1:
#         score_rect.midtop = (FRAME_DIM[0]/10, 15)
#     else:
#         score_rect.midtop = (FRAME_DIM[0]/2, FRAME_DIM[1]/1.25)
#     GAME_WINDOW.blit(score_surface, score_rect)
#     # pygame.display.flip()

# Main
def train():
    # Window size
    FRAME_DIM = (720, 480)
    
    # Check for errors
    check_for_errors()

    # Initialise game window
    pygame.display.set_caption('Snake Eater')
    GAME_WINDOW = pygame.display.set_mode((FRAME_DIM[0], FRAME_DIM[1]))

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Create Snake objects
    snakes = list()
    num_snakes = 1
    for _ in range(num_snakes):
        snake = Snake(100, 50, FRAME_DIM)
        snakes.append(snake)

    # Main logic
    running = True
    while running:    
        for event in pygame.event.get():
            # Quit Functionality
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            for snake in snakes:
                # Get pressed key / Neural network output
                key_pressed = get_key_pressed(event)
                # output = ....
                
                # Resond to pressed key
                if key_pressed == 0:
                    snake.change_to = 'UP'
                elif key_pressed == 1:
                    snake.change_to = 'DOWN'
                elif key_pressed == 2:
                    snake.change_to = 'LEFT'
                elif key_pressed == 3:
                    snake.change_to = 'RIGHT'
            
        # Move snake
        for snake in snakes:
            # Move snake (and spawn food)
            snake.move() 
            
        # Draw
        GAME_WINDOW.fill(BLACK)
        for snake in snakes:       
            snake.draw_snake_and_food(GAME_WINDOW)

        # Snake Losing Conditions
        for x, snake in enumerate(snakes):
            try:
                # Getting out of bounds
                if snake.snake_pos[0] < 0 or snake.snake_pos[0] > FRAME_DIM[0]-10:
                    snakes.pop(x)
                elif snake.snake_pos[1] < 0 or snake.snake_pos[1] > FRAME_DIM[1]-10:
                    snakes.pop(x)
                # Touching the snake body
                for block in snake.snake_body[1:]:
                    if snake.snake_pos[0] == block[0] and snake.snake_pos[1] == block[1]:
                        snakes.pop(x)
            except IndexError:
                pass
                  
            # show_score(1, WHITE, 'consolas', 20)
            
            
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
    winner = pop.run(train, 50)


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'configuration.txt')
    run(config_path)
