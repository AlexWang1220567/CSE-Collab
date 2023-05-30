"""
title: the window class
author: Pushkar Talwar
date-created: 05/10/2023
"""


import pygame


class Window:
    """
    Create window that will load the game
    :return: None
    """

    def __init__(self, TITLE, WIDTH=1200, HEIGHT=650, FPS=120):
        self.__TITLE = TITLE # text that appears in the title bar
        self.__FPS = FPS # the frames/second the window with refresh
        self.__WIDTH = WIDTH # Width of the window
        self.__HEIGHT = HEIGHT # height of the widow
        self.__SCREEN_DIM = (self.__WIDTH, self.__HEIGHT)
        self.__BG_COLOUR = (50, 50, 50)
        self.__FRAME = pygame.time.Clock()
        self.__SURFACE = pygame.display.set_mode(self.__SCREEN_DIM)
        self.__SURFACE.fill(self.__BG_COLOUR)
        pygame.display.set_caption(self.__TITLE) # updates the title of the window to the title text


    #Modifier
    def updateFrames(self):
        """
        Update the window object based on the FPS
        :return:
        """
        self.__FRAME.tick(self.__FPS)
        pygame.display.flip()

    def ClearScreen(self):
        """
        Fill the screen with the background color
        :return:
        """
        self.__SURFACE.fill(self.__BG_COLOUR)

    def getSurface(self):
        return self.__SURFACE

    def getWidth(self):
        return self.__WIDTH

    def getHeight(self):
        return self.__HEIGHT