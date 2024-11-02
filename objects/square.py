# Imports
import pygame

# Square
class Square:
    def __init__(self, boardSize):
        self.size = 800 / boardSize[0]
        self.rect = None
        self.type = None
        self.opened = False
        self.flagged = False