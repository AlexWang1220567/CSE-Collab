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

class PlatfromPlacement():
    def __init__(self):
        pass

    def placement(self, PLATFORMS, WINDOW):
        for i in PLATFORMS:
            for x in range(3):
                print(x)
                for j in range(2):
                    print(j)
                    i.setPoistion(
                        (
                            (50 + (100 * j)),
                            (50 + (100 * x))
                        )
                    )


if __name__ == "__main__":

    from window import Window

    pygame.init()

    WINDOW = Window("Image Sprite Test")
    PLATFORMS = []
    for i in range(6):
        PLATFORMS.append(Platform(25, 150))
    PLATFORM = -1
    for x in range(3):
        print(x)
        for j in range(2):
            print(j)
            PLATFORM += 1
            PLATFORMS[PLATFORM].setPosition(
                (
                    (100 + (300 * j)),
                    (50 + (150 * x))
                )
            )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        PRESSED_KEYS = pygame.key.get_pressed()


        WINDOW.ClearScreen()
        for platform in PLATFORMS:
            WINDOW.getSurface().blit(platform.getSurface(), platform.getPOS())
        WINDOW.updateFrames()
