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
        self.JUMPING_Y = 0
        self.IS_JUMPING = False
        self.JUMP_HEIGHT = 100
        self.__HEALTH = 100
        self.setSPD(5)

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
        ### JUMPING
        if KEYS_PRESSED[pygame.K_SPACE]:
            self.IS_JUMPING = True

        self.setPosition((self._X, self._Y))

    def jumpPlayer(self):

        if self.JUMPING_Y <= self.JUMP_HEIGHT:
            self.JUMPING_Y += self._SPD +5
            self._Y -= self._SPD +5
        else:
            self.IS_JUMPING = False
            self.fall()


        self.setPosition((self._X, self._Y))

    def fall(self):
        self._Y += self._SPD +5
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

    def getSPD(self):
        return self._SPD


if __name__ == "__main__":

    from window import Window
    from platform import Platform
    pygame.init()

    WINDOW = Window("Image Sprite Test")
    PLAYER = Player()
    PLAYER.setScale(0.1)
    PLAYER.setFlipX()
    PLAYER.setPosition((0, WINDOW.getHeight()-PLAYER.getHeight()))

    PLATFORM = Platform(30, WINDOW.getWidth())
    PLATFORM.setPosition((0, WINDOW.getHeight()-PLATFORM.getHeight()))


    while True:
        ### INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        PRESSED_KEYS = pygame.key.get_pressed()

        ### PROCESSING
        PLAYER.movePlayer(PRESSED_KEYS)
        # JUMP
        if PLAYER.IS_JUMPING:
            PLAYER.jumpPlayer()
        else:
            PLAYER.fall()
            PLAYER.JUMPING_Y = 0
        PLAYER.checkBoundries(WINDOW.getWidth(), WINDOW.getHeight()-PLATFORM.getHeight())

        # PLATFORM
        #if PLAYER.isSpriteColliding(PLATFORM.getPOS(), PLATFORM.getDiminsoins()):
        #   PLAYER.setPosition((PLAYER.getPOS()[0], PLAYER.getPOS()[1]-PLAYER.getSPD()))

        #else:
            #if not PLAYER.IS_JUMPING and PLAYER.JUMPING_Y >= PLAYER.JUMP_HEIGHT:
         #       PLAYER.fall()



        ### OUTPUT
        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
        WINDOW.updateFrames()






