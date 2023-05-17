"""
title: the engine class
author: Mengqi Wang, Pushkar Talwar
date-created: 05/12/2023
"""
import pygame
from platform import Platform
from player import Player
from window import Window
from text import Text
from bg_sprite import BGSprite


class Engine:

    def __int__(self):
        self.__WINDOW = Window("Halloween")
        self.__TITLE = Text("Halloween")

        self.__PLAYER = Player()
        self.__PLAYER.setPosition(
            (
                self.__WINDOW.getWidth() // 2 - self.__PLAYER.getWidth() // 2,
                self.__WINDOW.getHeight() // 2 - self.__PLAYER.getHeight() // 2
            )
        )

        self.__GROUND = Platform(30, self.__WINDOW.getWidth())
        self.__GROUND.setPosition((0, self.__WINDOW.getHeight()))

        self.__PLATFORMS = []
        self.__BG = BGSprite("sprite_images/shrubs.png")

        self.__BOSS = object
        self.__BOSS_HEALTH_BAR = object

        self.__LASER_HAND = object
        self.__THUMB = object
        self.__FIRE_HAND = object

        self.__TIME_ELAPSED = 0

    def bossRoom(self):

        self.__WINDOW = Window("Image Sprite Test")
        self.__PLAYER = Player()
        self.__PLAYER.setFlipX()
        self.__PLAYER.setPosition((0, self.__WINDOW.getHeight() - self.__PLAYER.getHeight()))

        PLATFORM = Platform(30, self.__WINDOW.getWidth())
        PLATFORM.setPosition((0, self.__WINDOW.getHeight() - PLATFORM.getHeight()))
        self.__TIME_ELAPSED = 0

        while True:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            PRESSED_KEYS = pygame.key.get_pressed()

            ### PROCESSING
            self.__PLAYER.movePlayer(PRESSED_KEYS)

            # ANIMATION
            self.__TIME_ELAPSED += 1
            if self.__TIME_ELAPSED >= 250:
                # NOT OUT OF SPRITES YET
                if self.__PLAYER.IMAGE_IND < len(self.__PLAYER.IMAGES) - 1:
                    self.__PLAYER.IMAGE_IND += 1
                else:
                    self.__PLAYER.IMAGE_IND = 0
                # REPLACE SPRITE
                PRESSED_KEYS = pygame.key.get_pressed()
                self.__PLAYER.setSprite(PRESSED_KEYS)
                self.__TIME_ELAPSED = 0

            # JUMP
            if self.__PLAYER.IS_JUMPING:
                self.__PLAYER.jumpPlayer()
            else:
                self.__PLAYER.fall()
                # PLAYER.JUMPING_Y = 0
            self.__PLAYER.checkBoundries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight() - PLATFORM.getHeight())

            # PLATFORM
            if self.__PLAYER.isSpriteColliding(PLATFORM.getPOS(), PLATFORM.getDiminsoins()):
                self.__PLAYER.JUMPING_Y = 0

            ### OUTPUT
            self.__WINDOW.ClearScreen()
            self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())
            self.__WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
            self.__WINDOW.updateFrames()


if __name__ == "__main__":
    pygame.init()
    GAME = Engine()
    GAME.bossRoom()




