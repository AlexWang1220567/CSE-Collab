"""
title: the image sprite
author: Mengqi Wang
date-created: 05/12/2023
"""
import pygame
from mySprite import mySprite
from window import Window


class ImageSprite(mySprite):
    def __init__(self, IMAGE):
        mySprite.__init__(self)

        self.__FILE_LOC = IMAGE
        # load with transparency (convert_alpha)
        self._SURFACE = pygame.image.load(self.__FILE_LOC).convert_alpha() ## PROBLEM IS LOAD WITH TRANSPARENCY
        # self._SURFACE = pygame.image.load("sprite_images/PumpkinSage.png")
        self.__X_FLIP = False

    ### MODIFIERS

    def setFlipX(self):
        """
        Flip image on the Y axis
        :return:
        """
        self._SURFACE = pygame.transform.flip(self._SURFACE, True, False)

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

if __name__ == "__main__":

    pygame.init()
    ATTACK_EFFECT = ImageSprite("sprite_images/cut.png")
    WINDOW = Window("Image Sprite Test")
    ATTACK_EFFECT.setPosition((WINDOW.getWidth()-ATTACK_EFFECT.getWidth(), 0))


    while True:
        ### INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(ATTACK_EFFECT.getSurface(), ATTACK_EFFECT.getPOS())
        WINDOW.updateFrames()




