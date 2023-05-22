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
from imageSprite import ImageSprite


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
        self.__BG = ImageSprite("sprite_images/shrubs.png")

        self.__BOSS = object
        self.__LASER_HAND = object
        self.__THUMB = object
        self.__FIRE_HAND = object

    def bossRoom(self):

        self.__WINDOW = Window("Image Sprite Test")
        self.__PLAYER = Player()
        self.__PLAYER.setScale(0.1)
        self.__PLAYER.setFlipX()
        self.__PLAYER.setPosition((0, self.__WINDOW.getHeight() - self.__PLAYER.getHeight()))

        PLATFORM = Platform(30, self.__WINDOW.getWidth())
        PLATFORM.setPosition((0, self.__WINDOW.getHeight() - PLATFORM.getHeight()))

        while True:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            PRESSED_KEYS = pygame.key.get_pressed()

            ### PROCESSING
            self.__PLAYER.movePlayer(PRESSED_KEYS)
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
            #   PLAYER.setPosition((PLAYER.getPOS()[0], PLAYER.getPOS()[1]-PLAYER.getSPD()))

            # else:
            # if not PLAYER.IS_JUMPING and PLAYER.JUMPING_Y >= PLAYER.JUMP_HEIGHT:
            #       PLAYER.fall()

            ### OUTPUT
            self.__WINDOW.ClearScreen()
            self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())
            self.__WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
            self.__WINDOW.updateFrames()


if __name__ == "__main__":
    pygame.init()
    GAME = Engine()
    GAME.bossRoom()




