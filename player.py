"""
title: the player class
author: Mengqi Wang
date-created: 05/10/2023
"""

from mySprite import mySprite
import pygame

class Player(mySprite):

    def __init__(self):
        mySprite.__init__(self)
        self._SURFACE = pygame.image.load("sprite_images/shrubs.png").convert_alpha()
        self.__X_FLIP = False
        self.__JUMPING_Y = 0
        self.IS_JUMPING = False
        self.__HEALTH = 100

    def setHealth(self, HEALTH):
        self.__HEALTH = HEALTH

    def movePlayer(self, KEYS_PRESSED):


        if KEYS_PRESSED[pygame.K_a]:
            self._X -= self._SPD
            if self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = False
        if KEYS_PRESSED[pygame.K_d]:
            self._X += self._SPD
            if not self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = True

    def isJumping(self, KEYS_PRESSED):
        # JUMPING
        if KEYS_PRESSED[pygame.K_SPACE]:
            self.IS_JUMPING = True
            return True

    def jumpPlayer(self):

        if self.__JUMPING_Y <= 50 and not self.__JUMPING:
            self.__JUMPING = True
            self.__JUMPING_Y += 10
            self._Y += 10

        self.setPosition((self._X, self._Y))

    def fall(self):
        self._Y -= 10
        self.setPosition((self._X, self._Y))

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

    def getHealth(self):
        return self.__HEALTH


if __name__ == "__main__":

    from window import Window

    pygame.init()

    WINDOW = Window("Image Sprite Test")
    PLAYER = Player()
    PLAYER.setSPD(15)
    PLAYER.setScale(0.1)
    PLAYER.setFlipX()
    PLAYER.setPosition((0, WINDOW.getHeight()-PLAYER.getHeight()))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        PRESSED_KEYS = pygame.key.get_pressed()
        PLAYER.movePlayer(PRESSED_KEYS)

        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        WINDOW.updateFrames()






