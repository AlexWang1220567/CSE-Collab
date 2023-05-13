"""
title: the background
author: Mengqi Wang
date-created: 05/12/2023
"""
import pygame
from mySprite import mySprite


class BGSprite(mySprite):
    def __int__(self, IMAGE):
        mySprite.__init__(self)

        self.__FILE_LOC = IMAGE
        # load with transparency (convert_alpha)
        self._SURFACE = pygame.image.load(self.__FILE_LOC).convert_alpha()






