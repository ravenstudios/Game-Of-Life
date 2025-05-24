from constants import *
# we need this because were asking for TILE_SIZE
import pygame
class Grid(object):

    def __init__(self):
        pass

        # self must be the first arg in every function inside a class. Self refers to the instace created and not the class itself
        # added screen arg to be passed in from main
    def draw(self, screen, positions):
        for position in positions:
            col, row = position
            top_left = (col * TILE_SIZE, row * TILE_SIZE)
            pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))
