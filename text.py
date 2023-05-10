
import pygame

from mySprite import mySprite

class Text(mySprite):
    def __init__(self, TEXT, FONT_SIZE=36):
        mySprite.__init__(self)
        self.__TEXT = TEXT
        self.__FONT_SIZE = FONT_SIZE
        self.__FONT = pygame.font.SysFont("Arial", self.__FONT_SIZE)
        self._SURFACE = self.__FONT.render(self.__TEXT, True, self._COLOR)

    def setColor(self, TUPLE):
        mySprite.setColor(self, TUPLE)
        self._SURFACE = self.__FONT.render(self.__TEXT, True, self._COLOR)

    def setFontSize(self, NEW_SIZE):
        self.__FONT_SIZE = NEW_SIZE
        self.__FONT = pygame.font.SysFont("Arial", self.__FONT_SIZE)
        self._SURFACE = self.__FONT.render(self.__TEXT, True, self._COLOR)