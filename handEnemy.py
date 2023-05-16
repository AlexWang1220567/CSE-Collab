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

    def bounceY(self, SPRITE_HEIGHT, MAX_HIEGTH, MIN_HIEGTH=0):

        self._Y += self._SPD * self._DIR_Y
        if self._Y > MAX_HIEGTH - SPRITE_HEIGHT:
            self._DIR_Y = -1
        if self._Y < MIN_HIEGTH:
            self._DIR_Y = 1
        self.__POS = (self._X, self._Y)

    def fall(self):
        self._Y += self._SPD +5
        self.setPosition((self._X, self._Y))

    def moveThumb(self, Window):
        self.setPosition(
            (
                random.randrange(Window.getWidth() - self.getWidth()),
                (0 - self.getHeight())
            )
        )

    def setFireHand(self):
        self.setPosition(
            (
                WINDOW.getWidth()//2 - self.getWidth()//2,
                WINDOW.getHeight() - self.getHeight()
            )
        )



class Laser(mySprite):
    def __init__(self, IMAGE_FILE):
        mySprite.__init__(self)
        self.__FILE_LOC = IMAGE_FILE
        self._SURFACE = pygame.image.load(self.__FILE_LOC).convert_alpha()
        self.__X_FLIP = True

    def set_X_Flip(self, BOOL=True):
        self.__X_FLIP = BOOL

    def resetLaserPOS(self):
        self.setPosition(
            (
                FIRE_HAND.getPOS()[0] + FIRE_HAND.getWidth()//2,
                FIRE_HAND.getPOS()[1] + FIRE_HAND.getHeight()//2
            )
        )


    def laserMovment(self):
        self._X += self._SPD * self._DIR_X
        self.setPosition((self._X, self._Y))

if __name__ == "__main__":
    pygame.init()
    time_since_action = 0
    clock = pygame.time.Clock()
    WINDOW = Window("Hand enemy Test")
    BUNNY = HandEnemy("sprite_images/thumb.png")
    FIRE_HAND = HandEnemy("sprite_images/fireHand.png")
    LASER = Laser("sprite_images/laser (1).png")
    LASER.setSPD(15)
    BUNNY.setSPD(15)
    BUNNY.setScale(1)
    BUNNY.setFlipX()
    FIRE_HAND.setFireHand()
    LASER.resetLaserPOS()
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
        time_since_action += 1
        if time_since_action > 250:
            BUNNY.fall()
            if BUNNY.getPOS()[1] >= WINDOW.getHeight():
                time_since_action = 0
                BUNNY.moveThumb(WINDOW)
        LASER.laserMovment()
        if LASER.getPOS()[0] > WINDOW.getWidth():
            LASER.resetLaserPOS()
        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(BUNNY.getSurface(), BUNNY.getPOS())
        WINDOW.getSurface().blit(FIRE_HAND.getSurface(), FIRE_HAND.getPOS())
        WINDOW.getSurface().blit(LASER.getSurface(), LASER.getPOS())
        WINDOW.updateFrames()