"""
Title: Actions file for image sprites
Author: Pushkar Talwar
Date-created: 05-11-2023
"""


import random

import pygame
from mySprite import mySprite
from window import Window
from  player import Player


class HandEnemy(mySprite):
    """
    Load and manipulate images
    """
    def __init__(self, IMAGE_FILE):
        mySprite.__init__(self)
        self.__FILE_LOC = IMAGE_FILE
        self._SURFACE = pygame.image.load(self.__FILE_LOC).convert_alpha()
        self.__X_FLIP = True

    def moveWASD(self, KEYS_PRESSED):

        mySprite.moveWASD(self, KEYS_PRESSED)
        if KEYS_PRESSED[pygame.K_a]:
            if self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = False
        if KEYS_PRESSED[pygame.K_d]:
            if not self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = True

    def setScale(self, SCALE_X, SCALE_Y=0):
        """
        Resize the image based on a factor
        :param SCALE_X: float
        :param SCALE_Y: float
        :return: None
        """

        if SCALE_Y == 0:
            SCALE_Y = SCALE_X
        self._SURFACE = pygame.transform.scale(
            self._SURFACE,
            (self.getWidth()*SCALE_X, self.getHeight()*SCALE_Y)
        )

    def setFlipX(self):
        """
        Flip image on the Y axis
        :return:
        """
        self._SURFACE = pygame.transform.flip(self._SURFACE, True, False)

    def handFallAttack(self, Window):
        self.setPosition(
            (
                random.randrange(Window.getWidth() - self.getWidth()),
                0
            )
        )

        self._Y += self._SPD * self._DIR_Y
        if self._Y >= Window.getHeight() - self.getHeight():
            pass

if __name__ == "__main__":
    pygame.init()
    time_since_action = 0
    clock = pygame.time.Clock()
    WINDOW = Window("Hand enemy Test")
    BUNNY = HandEnemy("sprite_images/thumb.png")
    BUNNY.setSPD(15)
    BUNNY.setScale(1)
    BUNNY.setFlipX()
    BUNNY.setPosition(
        (
            0,0
        )
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        TIME = clock.tick()
        PRESSED_KEYS = pygame.key.get_pressed()
        BUNNY.moveWASD(PRESSED_KEYS)
        BUNNY.handFallAttack(WINDOW)
        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(BUNNY.getSurface(), BUNNY.getPOS())
        WINDOW.updateFrames()