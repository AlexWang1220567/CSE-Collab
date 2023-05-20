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
        self.IMAGES = []
        self.IMAGES.append(pygame.image.load("sprite_images/player_walk_1.png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/player_walk_3.png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/player_walk_2 (1).png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/player_walk_3.png").convert_alpha())
        self.IMAGE_IND = 0
        self._SURFACE = self.IMAGES[self.IMAGE_IND]
        self.__X_FLIP = False
        self.JUMPING_Y = 0
        self.IS_JUMPING = False
        self.JUMP_HEIGHT = 230
        self.__HEALTH = 100
        self.setSPD(10)

        self.WALK_TIME_ELAPSED = 0

    def setSprite(self, KEYS_PRESSED):

        if self.WALK_TIME_ELAPSED >= 10:

            # NOT OUT OF SPRITES YET
            if self.IMAGE_IND < len(self.IMAGES) - 1:
                self.IMAGE_IND += 1
            else:
                self.IMAGE_IND = 0
            # REPLACE SPRITE

            self._SURFACE = self.IMAGES[self.IMAGE_IND]
            if KEYS_PRESSED[pygame.K_a]:
                self.__X_FLIP = True



            self.WALK_TIME_ELAPSED = 0


    def deductHealth(self, DAMAGE):
        self.__HEALTH -= DAMAGE

    def movePlayer(self, KEYS_PRESSED):


        if KEYS_PRESSED[pygame.K_a]:
            self._X -= self._SPD
            if self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = False
            self.setSprite(KEYS_PRESSED)
        if KEYS_PRESSED[pygame.K_d]:
            self._X += self._SPD
            if not self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = True
            self.setSprite(KEYS_PRESSED)
        ### JUMPING
        if KEYS_PRESSED[pygame.K_SPACE] and self.JUMPING_Y == 0:
            self.IS_JUMPING = True

        self.setPosition((self._X, self._Y))

    def jumpPlayer(self):

        if self.JUMPING_Y <= self.JUMP_HEIGHT:
            self.JUMPING_Y += self._SPD + 5
            self._Y -= self._SPD + 5
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
    def getFlip(self):
        return self.__X_FLIP


if __name__ == "__main__":

    from window import Window
    from platform import Platform
    pygame.init()

    WINDOW = Window("Image Sprite Test")
    PLAYER = Player()
    #PLAYER.setScale(0.1)

    TIME_ELAPSED = 0


    # SPRITE CHANGE
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
        PLAYER.WALK_TIME_ELAPSED += 1
        PLAYER.movePlayer(PRESSED_KEYS)
        # JUMP
        if PLAYER.IS_JUMPING:
            PLAYER.jumpPlayer()
        else:
            PLAYER.fall()
            #PLAYER.JUMPING_Y = 0
        PLAYER.checkBoundries(WINDOW.getWidth(), WINDOW.getHeight()-PLATFORM.getHeight())
        # PLATFORM
        if PLAYER.isSpriteColliding(PLATFORM.getPOS(), PLATFORM.getDiminsoins()):
            PLAYER.JUMPING_Y = 0
        #   PLAYER.setPosition((PLAYER.getPOS()[0], PLAYER.getPOS()[1]-PLAYER.getSPD()))

        # else:
        # if not PLAYER.IS_JUMPING and PLAYER.JUMPING_Y >= PLAYER.JUMP_HEIGHT:
        #       PLAYER.fall()

        # ANIMATION
        # PLAYER.WALK_TIME_ELAPSED += 1
        # if TIME_ELAPSED >= 15:
        #     # NOT OUT OF SPRITES YET
        #     if PLAYER.IMAGE_IND < len(PLAYER.IMAGES) -1:
        #         PLAYER.IMAGE_IND += 1
        #     else:
        #         PLAYER.IMAGE_IND = 0
        #     # REPLACE SPRITE
        # PRESSED_KEYS = pygame.key.get_pressed()
        # PLAYER.setSprite(PRESSED_KEYS)
        # TIME_ELAPSED = 0



        ### OUTPUT
        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
        WINDOW.updateFrames()






