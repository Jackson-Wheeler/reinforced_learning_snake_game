import pygame #for snake game
import neat #for neural networks
import pickle #for saving best trained genome after training
import os
import sys
import time
import random

def main():
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'configuration.txt')
    run(config_path)

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


