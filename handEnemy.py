"""
Title: Actions file for image sprites
Author: Pushkar Talwar
Date-created: 05-11-2023
"""


import random

import pygame
from mySprite import mySprite
from window import Window
from player import Player


class HandEnemy(mySprite):
    """
    Load and manipulate images
    """
    def __init__(self, IMAGE_FILE):
        mySprite.__init__(self)
        self.__FILE_LOC = IMAGE_FILE
        self._SURFACE = pygame.image.load(self.__FILE_LOC).convert_alpha()
        self.__X_FLIP = True

    def moveWASD(self, KEYS_PRESSED):

        mySprite.moveWASD(self, KEYS_PRESSED)
        if KEYS_PRESSED[pygame.K_a]:
            if self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = False
        if KEYS_PRESSED[pygame.K_d]:
            if not self.__X_FLIP:
                self.setFlipX()
                self.__X_FLIP = True

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

    def bounceY(self, SPRITE_HEIGHT, MAX_HIEGTH, MIN_HIEGTH=0):

        self._Y += self._SPD * self._DIR_Y
        if self._Y > MAX_HIEGTH - SPRITE_HEIGHT:
            self._DIR_Y = -1
        if self._Y < MIN_HIEGTH:
            self._DIR_Y = 1
        self.setPosition((self._X, self._Y))

    def fall(self):
        self._Y += self._SPD +5
        self.setPosition((self._X, self._Y))

    def moveThumb(self, Window):
        self.setPosition(
            (
                random.randrange(Window.getWidth() - self.getWidth()),
                (0 - self.getHeight())
            )
        )

    def setFireHand(self, WINDOW):
        self.setPosition(
            (
                WINDOW.getWidth()//2 - self.getWidth()//2,
                WINDOW.getHeight() - self.getHeight()
            )
        )



class Laser(mySprite):

    def __init__(self, IMAGE_FILE, SPD=0):
        mySprite.__init__(self)
        self.__FILE_LOC = IMAGE_FILE
        self._SURFACE = pygame.image.load(self.__FILE_LOC).convert_alpha()
        self.__X_FLIP = False
        self._SPD_Y = SPD

    def set_X_Flip(self, BOOL=True):
        self.__X_FLIP = BOOL

    def setDIR_X(self, INT):
        self._DIR_X = INT

    def setDIR_Y(self, INT):
        self._DIR_Y = INT

    def resetLaserPOS(self, FIRE_HAND):
        self.setPosition(
            (
                FIRE_HAND.getPOS()[0] + FIRE_HAND.getWidth()//2,
                FIRE_HAND.getPOS()[1] + FIRE_HAND.getHeight()//2
            )
        )


    def laserMovment(self):
        self._X += self._SPD * self._DIR_X
        self._Y += self._SPD_Y * self._DIR_Y
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

    def setSPD_Y(self, SPD):
        self._SPD_Y = SPD

    def shootLaser(self, HAND):
        self._X += self._SPD * self._DIR_X
        self.setPosition((self._X, self._Y))

class Hand_Engine:
    def __init__(self):
        pass

    def run(self):
        ### Time since clocks
        time_since_fall = 0
        time_since_laser = 0
        clock = pygame.time.Clock()

        ### Objects
        WINDOW = Window("Hand enemy Test")
        BUNNY = HandEnemy("sprite_images/thumb.png")
        FIRE_HAND = HandEnemy("sprite_images/fireHand.png")
        LASER_HAND = HandEnemy("sprite_images/shrubs.png")
        LASER = Laser("sprite_images/fire.png")
        LASER2 = Laser("sprite_images/fire.png")
        LASER_BEAM = Laser("sprite_images/laser (1).png")

        ### Set scales
        LASER_HAND.setScale(0.125)
        LASER.setScale(0.5)
        LASER2.setScale(0.5)
        BUNNY.setScale(1)

        ### Set SPD
        LASER_HAND.setSPD(10)
        LASER.setSPD(15)
        LASER.setSPD_Y(8)
        LASER2.setSPD(15)
        LASER2.setSPD_Y(8)
        BUNNY.setSPD(15)
        LASER_BEAM.setSPD(30)

        ### Set DIR
        LASER.setDIR_Y((-1))
        LASER2.setDIR_Y((-1))
        LASER2.setDIR_X((-1))
        LASER_BEAM.setDIR_X(-1)

        ### Set Flips
        BUNNY.setFlipX()
        LASER2.setFlipX()
        LASER_BEAM.setFlipX()

        ### Set POS
        FIRE_HAND.setFireHand(WINDOW)
        LASER.resetLaserPOS(FIRE_HAND)
        LASER2.resetLaserPOS(FIRE_HAND)
        BUNNY.setPosition(
            (
                0, 0
            )
        )

        LASER_HAND.setPosition(
            (
                WINDOW.getWidth() - LASER_HAND.getWidth(),
                WINDOW.getHeight()//2
            )
        )

        LASER_BEAM.setPosition(
            (
                LASER_HAND.getPOS()[0],
                LASER_HAND.getPOS()[1] + LASER_HAND.getHeight()//2
            )
        )


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            TIME = clock.tick()
            time_since_fall += TIME
            time_since_laser += TIME
            if time_since_fall > 250:
                BUNNY.fall()
                if BUNNY.getPOS()[1] >= WINDOW.getHeight():
                    time_since_fall = 0
                    BUNNY.moveThumb(WINDOW)
            LASER.laserMovment()
            if LASER.getPOS()[0] > WINDOW.getWidth():
                LASER.resetLaserPOS(FIRE_HAND)
            LASER2.laserMovment()
            if LASER2.getPOS()[0] < 0:
                LASER2.resetLaserPOS(FIRE_HAND)

            if time_since_laser > 30:
                LASER_BEAM.shootLaser(LASER_HAND)
                if LASER_BEAM.getPOS()[0] < (0 - LASER_BEAM.getWidth()):
                    time_since_laser = 0
                    LASER_BEAM.setPosition(
                        (
                            LASER_HAND.getPOS()[0],
                            LASER_HAND.getPOS()[1] + LASER_HAND.getHeight() // 2
                        )
                    )
            LASER_HAND.bounceY(LASER_HAND.getHeight(), WINDOW.getHeight())
            WINDOW.ClearScreen()
            WINDOW.getSurface().blit(BUNNY.getSurface(), BUNNY.getPOS())
            WINDOW.getSurface().blit(FIRE_HAND.getSurface(), FIRE_HAND.getPOS())
            WINDOW.getSurface().blit(LASER.getSurface(), LASER.getPOS())
            WINDOW.getSurface().blit(LASER2.getSurface(), LASER2.getPOS())
            WINDOW.getSurface().blit(LASER_BEAM.getSurface(), LASER_BEAM.getPOS())
            WINDOW.getSurface().blit(LASER_HAND.getSurface(), LASER_HAND.getPOS())
            WINDOW.updateFrames()

if __name__ == "__main__":
    pygame.init()
    GAME = Hand_Engine()
    GAME.run()
