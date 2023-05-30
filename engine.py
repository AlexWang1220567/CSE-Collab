"""
title: the engine class
author: Mengqi Wang, Pushkar Talwar
date-created: 05/12/2023
"""
import pygame
from boss import Boss
from platform import Platform
from player import Player
from window import Window
#from text import Text
#from imageSprite import ImageSprite
from handEnemy import HandEnemy
from handEnemy import Laser
#from mySprite import mySprite
#from text import Text


class Engine:

    def __init__(self):
        self.__WINDOW = Window("Halloween")

        ### PLAYER
        self.__PLAYER = Player()
        self.__PLAYER.setFlipX()

        ### BOSS
        self.__BOSS = Boss()
        ### BOSS HANDS
        self.__THUMB = HandEnemy("sprite_images/thumb.png")
        self.__FIRE_HAND = HandEnemy("sprite_images/fireHand.png")
        self.__LASER_HAND = HandEnemy("sprite_images/laserHand.png")
        self.__FIRE_2 = Laser("sprite_images/fire.png")
        self.__FIRE_1 = Laser("sprite_images/fire.png")  # LASER2
        self.__LASER_BEAM = Laser("sprite_images/laserBeam.png")
        self.initializeHands()
        self.__ATTACK_THUMB = True  # ATTACK

        ### GROUND
        self.__GROUND = Platform(50, self.__WINDOW.getWidth())
        self.__GROUND.setPosition((0, self.__WINDOW.getHeight() - self.__GROUND.getHeight()))

        ### PLATFORMS
        self.__PLATFORMS = []
        for i in range(6):
            self.__PLATFORMS.append(Platform(15, 100))

        ### LEVELS
        self.__AT_BOSS_LEVEL = True

    def initializeHands(self):
        ### Set scales
        self.__LASER_HAND.setScale(2.5)
        self.__FIRE_2.setScale(0.5)
        self.__FIRE_1.setScale(0.5)
        self.__LASER_BEAM.setScale(1.5)
        self.__THUMB.setScale(1.2)

        ### Set SPD
        self.__LASER_HAND.setSPD(5)
        self.__FIRE_2.setSPD(5)
        self.__FIRE_2.setSPD_Y(3)
        self.__FIRE_1.setSPD(5)
        self.__FIRE_1.setSPD_Y(3)
        self.__THUMB.setSPD(7)
        self.__LASER_BEAM.setSPD(20)

        ### Set DIR
        self.__FIRE_2.setDIR_Y((-1))
        self.__FIRE_1.setDIR_Y((-1))
        self.__FIRE_1.setDIR_X((-1))
        self.__LASER_BEAM.setDIR_X(-1)

        ### Set Flips
        self.__THUMB.setFlipX()
        self.__FIRE_1.setFlipX()
        self.__LASER_BEAM.setFlipX()

    def setPositionsBossRoom(self):

        ### PLAYER HEALTH
        BAR_COUNT = 0
        for bar in self.__PLAYER.HEALTH_BAR:
            BAR_COUNT += 1
            bar.setPosition((BAR_COUNT * 20, self.__WINDOW.getHeight() - bar.getHeight() - 20))

        ### PLATFORMS
        PLATFORM_COUNTER = -1
        for x in range(3):
            for j in range(2):
                PLATFORM_COUNTER += 1
                self.__PLATFORMS[PLATFORM_COUNTER].setPosition(
                    (
                        (200 + (300 * j)),
                        (100 + (170 * x))
                    )
                )

        ### HANDS
        self.__FIRE_HAND.setFireHand(self.__WINDOW, self.__GROUND.getHeight())
        self.__FIRE_2.resetLaserPOS(self.__FIRE_HAND)
        self.__FIRE_1.resetLaserPOS(self.__FIRE_HAND)
        self.__THUMB.setPosition(
            (
                0, 0
            )
        )
        # LASER HAND
        self.__LASER_HAND.setPosition(
            (
                self.__WINDOW.getWidth() - self.__LASER_HAND.getWidth(),
                self.__WINDOW.getHeight() // 2
            )
        )
        # LASER HORIZONTAL
        self.__LASER_BEAM.setPosition(
            (
                self.__LASER_HAND.getPOS()[0],
                self.__LASER_HAND.getPOS()[1] + self.__LASER_HAND.getHeight() // 2
            )
        )
        # PLAYER
        self.__PLAYER.setPosition((0, self.__WINDOW.getHeight()))
        # BOSS
        self.__BOSS.setPosition(
            (self.__WINDOW.getWidth() - self.__BOSS.getWidth(),
             self.__WINDOW.getHeight() - self.__GROUND.getHeight() - self.__BOSS.getHeight()))
        ### BOSS HEALTH
        BAR_COUNT = 0
        for bar in self.__BOSS.HEALTH_BAR:
            bar.setPosition((self.__BOSS.getPOS()[0] + BAR_COUNT * 20, self.__BOSS.getPOS()[1]))
            BAR_COUNT += 1



    def bossRoom(self):


        ### HANDS
        time_since_fall = 0
        time_since_laser = 0
        clock = pygame.time.Clock()
        boss_hit = False

        ### POSITIONS
        self.setPositionsBossRoom()

        while self.__AT_BOSS_LEVEL:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            PRESSED_KEYS = pygame.key.get_pressed()
            TIME = clock.tick()
            time_since_fall += TIME
            time_since_laser += TIME

            ### PROCESSING

            ### HANDS ATTACK
            if self.__ATTACK_THUMB:
                self.__THUMB.setPosition((self.__PLAYER.getPOS()[0], 0))
            if time_since_fall > 1200:
                if self.__ATTACK_THUMB:
                    self.__THUMB.setPosition((self.__PLAYER.getPOS()[0], self.__THUMB.getPOS()[1]))
                    self.__ATTACK_THUMB = False
                self.__THUMB.fall()
                if self.__THUMB.getPOS()[1] >= self.__WINDOW.getHeight():
                    time_since_fall = 0
                    self.__THUMB.moveThumb(self.__WINDOW)
                    self.__ATTACK_THUMB = True

            self.__FIRE_2.laserMovment()
            if self.__FIRE_2.getPOS()[0] > self.__WINDOW.getWidth():
                self.__FIRE_2.resetLaserPOS(self.__FIRE_HAND)

            self.__FIRE_1.laserMovment()
            if self.__FIRE_1.getPOS()[0] < 0:
                self.__FIRE_1.resetLaserPOS(self.__FIRE_HAND)

            if time_since_laser > 50:
                self.__LASER_BEAM.shootLaser(self.__LASER_HAND)
                if self.__LASER_BEAM.getPOS()[0] < (0 - self.__LASER_BEAM.getWidth()):
                    time_since_laser = 0
                    self.__LASER_BEAM.setPosition(
                        (
                            self.__LASER_HAND.getPOS()[0],
                            self.__LASER_HAND.getPOS()[1] + self.__LASER_HAND.getHeight() // 2
                        )
                    )
            self.__LASER_HAND.bounceY(self.__LASER_HAND.getHeight(), self.__WINDOW.getHeight())

            ### PLAYER
            self.__PLAYER.WALK_TIME_ELAPSED += TIME
            self.__PLAYER.movePlayer(PRESSED_KEYS)
            COLLIDING_PLATFORM = 0
            # JUMP
            if self.__PLAYER.IS_JUMPING:
                self.__PLAYER.jumpPlayer()
                self.__PLAYER.ATTACK_EFFECT.setPosition((self.__PLAYER.getPOS()[0] + self.__PLAYER.getWidth(), self.__PLAYER.getPOS()[1]))
            else:
                for platform in self.__PLATFORMS:
                    if self.__PLAYER.isSpriteColliding(platform.getPOS(), platform.getDiminsoins()):
                        if self.__PLAYER.isFallOnPlatform(platform.getPOS(), platform.getDiminsoins()):
                            self.__PLAYER.JUMPING_Y = 0
                            self.__PLAYER.IS_JUMPING = False
                            COLLIDING_PLATFORM += 1
                        self.__PLAYER.ATTACK_EFFECT.setPosition((5000, 5000))
                if COLLIDING_PLATFORM == 0:
                    self.__PLAYER.fall()
                    self.__PLAYER.ATTACK_EFFECT.setPosition((5000, 5000))
            self.__PLAYER.checkBoundries(self.__WINDOW.getWidth(), self.__WINDOW.getHeight() - self.__GROUND.getHeight())
            if self.__PLAYER.isSpriteColliding(self.__GROUND.getPOS(), self.__GROUND.getDiminsoins()):
                self.__PLAYER.JUMPING_Y = 0

            ######################### ATTACK

            if self.__BOSS.IMM_FRAME >= 500:
                self.__BOSS.IMM_FRAME = 0
                boss_hit = False

            if self.__PLAYER.ATTACK_EFFECT.isSpriteColliding(self.__BOSS.getPOS(), self.__BOSS.getDiminsoins()) and \
                    not boss_hit:
                boss_hit = True
                if len(self.__BOSS.HEALTH_BAR) > 0:
                    self.__BOSS.deductHealth()

            if boss_hit:
                self.__BOSS.IMM_FRAME += TIME

            ################### END
            if len(self.__BOSS.HEALTH_BAR) <= 0:
                pass
            if len(self.__PLAYER.HEALTH_BAR) <= 0:
                pass



            ###### BLIT
            self.blitBossLevel()


    def blitBossLevel(self):
        self.__WINDOW.ClearScreen()
        ##### BOSS - BLIT BEFORE PLAYER #####
        self.__WINDOW.getSurface().blit(self.__BOSS.getSurface(), self.__BOSS.getPOS())
        # BOSS HEALTH
        for bar in self.__BOSS.HEALTH_BAR:
            self.__WINDOW.getSurface().blit(bar.getSurface(), bar.getPOS())
        # PLAYER
        self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())
        # PLATFORM
        for platform in self.__PLATFORMS:
            self.__WINDOW.getSurface().blit(platform.getSurface(), platform.getPOS())
        # ATTACK EFFECT
        self.__WINDOW.getSurface().blit(self.__PLAYER.ATTACK_EFFECT.getSurface(), self.__PLAYER.ATTACK_EFFECT.getPOS())
        # THUMB
        self.__WINDOW.getSurface().blit(self.__THUMB.getSurface(), self.__THUMB.getPOS())
        # FIRE HAND
        self.__WINDOW.getSurface().blit(self.__FIRE_HAND.getSurface(), self.__FIRE_HAND.getPOS())
        # GROUND
        self.__WINDOW.getSurface().blit(self.__GROUND.getSurface(), self.__GROUND.getPOS())
        # PLAYER HEALTH
        ###################
        for health_bar in self.__PLAYER.HEALTH_BAR:
            self.__WINDOW.getSurface().blit(health_bar.getSurface(), health_bar.getPOS())
        # FIRE RIGHT?
        self.__WINDOW.getSurface().blit(self.__FIRE_2.getSurface(), self.__FIRE_2.getPOS())
        # FIRE LEFT?
        self.__WINDOW.getSurface().blit(self.__FIRE_1.getSurface(), self.__FIRE_1.getPOS())
        # LASER HORIZONTAL
        self.__WINDOW.getSurface().blit(self.__LASER_BEAM.getSurface(), self.__LASER_BEAM.getPOS())
        # LASER HAND
        self.__WINDOW.getSurface().blit(self.__LASER_HAND.getSurface(), self.__LASER_HAND.getPOS())

        self.__WINDOW.updateFrames()


if __name__ == "__main__":
    pygame.init()
    GAME = Engine()
    GAME.bossRoom()




