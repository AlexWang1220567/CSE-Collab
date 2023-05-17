"""
title: the player class
author: Mengqi Wang
date-created: 05/12/2023
"""

from mySprite import mySprite
import pygame

class Platform(mySprite):
    def __init__(self, HEIGHT=0, WIDTH=0):
        mySprite.__init__(self, HEIGHT, WIDTH)
        self._COLOR = (0, 0, 0)
        self._SURFACE = pygame.Surface(self._DIM, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._COLOR)


if __name__ == "__main__":

    from window import Window

    pygame.init()

    WINDOW = Window("Image Sprite Test")
    PLATFORM = Platform(30, WINDOW.getWidth())

    PLATFORM.setPosition((0, WINDOW.getHeight()-PLATFORM.getHeight()))

    PLATFORMS = []
    PLATFORM_2 = Platform(100, 100)
    #PLATFORM_2.setPosition(())
    PLATFORM.setColor((200, 200, 200))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        PRESSED_KEYS = pygame.key.get_pressed()


        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
        WINDOW.updateFrames()
