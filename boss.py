"""
title: the boss class
author: Mengqi Wang, Pushkar Talwar
date-created: 05/17/2023
"""


from mySprite import mySprite
import pygame
from platform import Platform
from player import Player

class Boss(mySprite):


    def __init__(self):

        mySprite.__init__(self)
        from platform import Platform
        # self.IMAGES = []
        # self.IMAGES.append(pygame.image.load("sprite_images/fireHand.png").convert_alpha())
        # self.IMAGES.append(pygame.image.load("sprite_images/thumb.png").convert_alpha())
        # self.IMAGE_IND = 0
        # self._SURFACE = self.IMAGES[self.IMAGE_IND]
        self._SURFACE = pygame.image.load("sprite_images/PumpkinSage.png").convert_alpha()
        self.setScale(2.5)
        self.__X_FLIP = False
        # self.JUMPING_Y = 0
        # self.IS_JUMPING = False
        # self.JUMP_HEIGHT = 140
        # self.setSPD(5)

        #################### IMMUNITY FRAME
        self.IMM_FRAME = 0
        ###################
        self.HEALTH_BAR = []
        for i in range(25):
            BAR = Platform(15, 10)
            BAR.setColor((250, 100, 100))
            self.HEALTH_BAR.append(BAR)

        ####################

    def deductHealth(self):
        self.HEALTH_BAR.pop(0)



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

    def getHealth(self):
        return self.__HEALTH






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

    PLATFORM = Platform(40, WINDOW.getWidth())
    PLATFORM.setPosition((0, WINDOW.getHeight()-PLATFORM.getHeight()))


    ##### BOSS #####
    BOSS = Boss()
    BOSS.setPosition((WINDOW.getWidth()-BOSS.getWidth(), WINDOW.getHeight()-PLATFORM.getHeight()-BOSS.getHeight()))
    # BOSS_HEALTH_BAR = Platform(10, 200)
    # BOSS_HEALTH_BAR.setColor((250, 0, 0))
    BOSS.BOSS_HEALTH_BAR.setPosition((BOSS.getPOS()[0]+BOSS.BOSS_HEALTH_BAR.getWidth()//2,BOSS.getPOS()[1]+20))
    ##### MUSIC #####
    pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
    pygame.mixer.init()
    pygame.mixer.music.load('sound_effects/deathScene.mp3')
    pygame.mixer.music.play(-1)

    while True:
        ### INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        PRESSED_KEYS = pygame.key.get_pressed()

        ##### BOSS #####
        if PLAYER.isSpriteColliding(BOSS.getPOS(), BOSS.getDiminsoins()):
            pass


        ### PROCESSING
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
        TIME_ELAPSED += 1
        if TIME_ELAPSED >= 25:
            # NOT OUT OF SPRITES YET
            if PLAYER.IMAGE_IND < len(PLAYER.IMAGES) -1:
                PLAYER.IMAGE_IND += 1
            else:
                PLAYER.IMAGE_IND = 0
            # REPLACE SPRITE
            PRESSED_KEYS = pygame.key.get_pressed()
            PLAYER.setSprite(PRESSED_KEYS)
            TIME_ELAPSED = 0


        ### OUTPUT
        WINDOW.ClearScreen()
        ##### BOSS - BLIT BEFORE PLAYER #####
        WINDOW.getSurface().blit(BOSS.getSurface(), BOSS.getPOS())
        WINDOW.getSurface().blit(BOSS.BOSS_HEALTH_BAR.getSurface(), BOSS.BOSS_HEALTH_BAR.getPOS())
        # PLAYER
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        # PLATFORM
        WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())

        WINDOW.updateFrames()