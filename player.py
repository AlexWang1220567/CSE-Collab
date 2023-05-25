"""
title: the player class
author: Mengqi Wang
date-created: 05/10/2023
"""

from mySprite import mySprite
from imageSprite import ImageSprite
import pygame

class Player(mySprite):

    def __init__(self):
        mySprite.__init__(self)
        self.IMAGES = []
        # self.IMAGES.append(pygame.image.load("sprite_images/player_walk_1.png").convert_alpha())
        # self.IMAGES.append(pygame.image.load("sprite_images/player_walk_3.png").convert_alpha())
        # self.IMAGES.append(pygame.image.load("sprite_images/player_walk_2.png").convert_alpha())
        # self.IMAGES.append(pygame.image.load("sprite_images/player_walk_3.png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/walk_3.png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/walk_1.png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/walk_3.png").convert_alpha())
        self.IMAGES.append(pygame.image.load("sprite_images/walk_2.png").convert_alpha())

        self.IMAGE_IND = 0
        self._SURFACE = self.IMAGES[self.IMAGE_IND]
        self.__X_FLIP = False
        self.JUMPING_Y = 0
        self.IS_JUMPING = False

        self.ATTACK_SPRITE = pygame.image.load("sprite_images/attack.png").convert_alpha()
        self.ATTACK_EFFECT = ImageSprite("sprite_images/cut.png")
        self.ATTACK_EFFECT.setPosition((5000,5000))
        # self.ATTACK_EFFECT.append(pygame.image.load("sprite_images/cut.png").convert_alpha())

        self.__JUMP_HEIGHT = 230

        ####################
        self.HEALTH_BAR = []
        for i in range(6):
            BAR = Platform(15, 10)
            BAR.setColor((250, 0, 0))
            self.HEALTH_BAR.append(BAR)
        ####################



        self.setSPD(10)

        self.WALK_TIME_ELAPSED = 0

    def setSprite(self, KEYS_PRESSED):

        if self.WALK_TIME_ELAPSED >= 20:

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


    def movePlayer(self, KEYS_PRESSED):

        if KEYS_PRESSED[pygame.K_a] and not self.IS_JUMPING:
            self._X -= self._SPD
            self.setSprite(KEYS_PRESSED)
            if self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = False

        if KEYS_PRESSED[pygame.K_d] and not self.IS_JUMPING:
            self._X += self._SPD
            # if not self.__X_FLIP:
            #     self.setFlipX()
            #     self.__X_FLIP = True
            self.setSprite(KEYS_PRESSED)
        ### JUMPING
        if KEYS_PRESSED[pygame.K_SPACE] and self.JUMPING_Y == 0:
            self._SURFACE = self.ATTACK_SPRITE
            if self.__X_FLIP:
                self.setFlipX()
            self.IS_JUMPING = True


        self.setPosition((self._X, self._Y))

    def jumpPlayer(self):

        if self.JUMPING_Y <= self.__JUMP_HEIGHT:
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

    def isFallOnPlatform(self, POS, DIM):
        """
        detect if the player is FALLING on platform
        :param POS: tuple
        :param DIM: tuple
        :return: bool
        """
        # is falling
        if not self.IS_JUMPING:
            pass


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

    PLATFORM = Platform(50, WINDOW.getWidth())
    PLATFORM.setPosition((0, WINDOW.getHeight()-PLATFORM.getHeight()))

    ###################
    BAR_COUNT = 0
    for bar in PLAYER.HEALTH_BAR:
        bar.setPosition((BAR_COUNT*30, WINDOW.getHeight()-bar.getHeight()-20))
        BAR_COUNT += 1


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
            PLAYER.ATTACK_EFFECT.setPosition((PLAYER.getPOS()[0]+PLAYER.getWidth(), PLAYER.getPOS()[1]))
        else:
            PLAYER.fall()
            PLAYER.ATTACK_EFFECT.setPosition((5000, 5000))
            #PLAYER.JUMPING_Y = 0
        PLAYER.checkBoundries(WINDOW.getWidth(), WINDOW.getHeight()-PLATFORM.getHeight())
        # PLATFORM
        if PLAYER.isSpriteColliding(PLATFORM.getPOS(), PLATFORM.getDiminsoins()):
            PLAYER.JUMPING_Y = 0




        ### OUTPUT
        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
        WINDOW.getSurface().blit(PLAYER.ATTACK_EFFECT.getSurface(), PLAYER.ATTACK_EFFECT.getPOS())
        ###################
        for health_bar in PLAYER.HEALTH_BAR:
            WINDOW.getSurface().blit(health_bar.getSurface(), health_bar.getPOS())
        WINDOW.updateFrames()






