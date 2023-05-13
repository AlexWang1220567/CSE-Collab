"""
title: the engine class
author: Mengqi Wang, Pushkar Talwar
date-created: 05/12/2023
"""
import pygame
from handEnemy import HandEnemy
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
        self.__LASER_HAND = object
        self.__THUMB = object
        self.__FIRE_HAND = object

    def bossRoom(self):

        while True:
            # INPUTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            PRESSED_KEYS = pygame.key.get_pressed()

            # PROCESSING
            self.__PLAYER.movePlayer(PRESSED_KEYS)

            # OUTPUTS
            self.__WINDOW.ClearScreen()
            self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())
            self.__WINDOW.updateFrames()


if __name__ == "__main__":
    pygame.init()
    GAME = Engine()
    GAME.bossRoom()




