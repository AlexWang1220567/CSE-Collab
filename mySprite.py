"""
"""

import pygame


class mySprite:
    """
    Many of common attributes and methods for sprites in pygame
    """

    def __init__(self, HEIGHT=0, WIDTH=0, X=0, Y=0, SPD=0, COLOR=(255, 255, 255)):
        self.__HEIGHT = HEIGHT
        self.__WIDTH = WIDTH
        self._DIM = (self.__WIDTH, self.__HEIGHT)
        self._SURFACE = pygame.Surface
        self.__X = X
        self.__Y = Y
        self.__POS = (self.__X, self.__Y)
        self.__SPD = SPD
        self._COLOR = COLOR
        self.__DIR_X = 1
        self.__DIR_Y = 1

    def setWidth(self, WIDTH):
        self.__WIDTH = WIDTH
        self._DIM = (self.__WIDTH, self.__HEIGHT)

    def setHeight(self, HEIGHT):
        self.__HEIGHT = HEIGHT
        self.__DIM = (self.__WIDTH, self.__HEIGHT)

    def setPosition(self, TUPLE):
        self.__X = TUPLE[0]
        self.__Y = TUPLE[1]
        self.__POS = (self.__X, self.__Y)

    def setColor(self, TUPLE):
        self._COLOR = TUPLE

    def setSPD(self, SPD):
        self.__SPD = SPD

    # Movement Method

    def marqueeX(self, MAX_WIDTH, MIN_WIDTH=0):
        self.__X += self.__SPD
        if self.__X > MAX_WIDTH:
            self.__X = MIN_WIDTH - self.getWidth()

        self.__POS = (self.__X, self.__Y)

    def bounceX(self, SPRITE_WIDTH, MAX_WIDTH, MIN_WIDTH=0):
        self.__X += self.__SPD * self.__DIR_X
        if self.__X > MAX_WIDTH - SPRITE_WIDTH:
            self.__DIR_X = -1
        if self.__X < MIN_WIDTH:
            self.__DIR_X = 1
        self.__POS = (self.__X, self.__Y)

    def moveWASD(self, KEYS_PRESSED):
        """
        move Sprite with WASD
        :param KEYS_PRESSED: list
        :return: None
        """
        if KEYS_PRESSED[pygame.K_d]:
            self.__X += self.__SPD
        if KEYS_PRESSED[pygame.K_a]:
            self.__X -= self.__SPD
        if KEYS_PRESSED[pygame.K_w]:
            self.__Y -= self.__SPD
        if KEYS_PRESSED[pygame.K_s]:
            self.__Y += self.__SPD
        self.__POS = (self.__X, self.__Y)

    def checkBoundries(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0):
        if self.__X > MAX_X - self.getWidth():
            self.__X = MAX_X - self.getWidth()
        if self.__X < MIN_X:
            self.__X = MIN_X
        if self.__Y > MAX_Y - self.getHeight():
            self.__Y = MAX_Y - self.getHeight()
        if self.__Y < MIN_Y:
            self.__Y = MIN_Y
        self.__POS = (self.__X, self.__Y)

    def getWidth(self):
        return self._SURFACE.get_width()

    def getHeight(self):
        return self._SURFACE.get_height()

    def getDiminsoins(self):
        return (self._SURFACE.get_width(), self._SURFACE.get_height())

    def getPOS(self):
        return self.__POS

    def getSurface(self):
        return self._SURFACE

    def isSpriteColliding(self, POSITION, DIMINSION):
        """
        Check sprite is colliding with current sprite
        :param POSITION: tuple
        :param DIMINSION: tuple
        :return: bool
        """

        SPRITE_X = POSITION[0]
        SPRITE_Y = POSITION[1]
        SPRITE_W = DIMINSION[0]
        SPRITE_H = DIMINSION[1]

        if SPRITE_X >= self.__X - SPRITE_W and SPRITE_X <= self.__X + self.getWidth():
            if SPRITE_Y >= self.__Y - SPRITE_H and SPRITE_Y <= self.__Y + self.getHeight():
                return True
        return False