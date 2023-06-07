"""
title: the engine class
author: Mengqi Wang, Pushkar Talwar
date-created: 05/12/2023
"""
import random
import time

import pygame
from boss import Boss
from platform import Platform
from player import Player
from window import Window
#from text import Text
from imageSprite import ImageSprite
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
        self.__FIRE_HAND = HandEnemy("sprite_images/fireHand (1).png")
        self.__LASER_HAND = HandEnemy("sprite_images/laserHand (1).png")
        self.__FIRE_2 = Laser("sprite_images/fire.png")
        self.__FIRE_1 = Laser("sprite_images/fire.png")  # LASER2
        self.__LASER_BEAM = Laser("sprite_images/laserBeam.png")
        self.initializeHands()
        self.__ATTACK_THUMB = True  # ATTACK

        ### WHAT CAN DAMAGE THE PLAYER
        self.__DANGER_LIST = []
        self.__DANGER_LIST.append(self.__FIRE_1)
        self.__DANGER_LIST.append(self.__FIRE_2)
        self.__DANGER_LIST.append(self.__LASER_BEAM)
        self.__DANGER_LIST.append(self.__THUMB)

        ### GROUND
        self.__GROUND = Platform(50, self.__WINDOW.getWidth())
        self.__GROUND.setPosition((0, self.__WINDOW.getHeight() - self.__GROUND.getHeight()))

        ### PLATFORMS
        self.__PLATFORMS = []
        for i in range(6):
            self.__PLATFORMS.append(Platform(20, 100))

        ### LEVELS
        self.__AT_BOSS_LEVEL = True
        self.__AT_START_LEVEL = True
        self.__WIN = False
        ### BG
        self.__BG = ImageSprite("sprite_images/BG.png")
        self.__BG_PEACEFUL_NIGHT = ImageSprite("sprite_images/BG_PEACEFUL_NIGHT.png")
        self.__BG.setScale(2)
        self.__BG_PEACEFUL_NIGHT.setScale(2)
        ### TITLE SCREEN
        self.__MAIN_TITLE = ImageSprite("sprite_images/main_title.png")
        ### DEATH
        self.__DEATH_BG = ImageSprite("sprite_images/DEATH.png")
        ### LIVES
        self.__EXPLOSION = ImageSprite("sprite_images/2_explosion.png")
        self.__EXPLOSION.setScale(4)
        self.__EXPLOSION_SOUND = pygame.mixer.Sound("sound_effects/hq-explosion-6288.mp3")
        self.__END_SOUND = pygame.mixer.Sound("sound_effects/thehand.mp3")
        self.__THIS_IS_NOT_MTH = ImageSprite("sprite_images/ThisIsNotMth.png")
        self.__NOT_MATH_SOUND = pygame.mixer.Sound("sound_effects/ThisIsNotMath.mp3")
        ### INTRO
        self.__INTRO_IMAGES = []
        self.__INTRO_IMAGES.append(ImageSprite("sprite_images/SAGE_TITLE_3.png"))
        self.__INTRO_IMAGES.append(ImageSprite("sprite_images/SAGE_TITLE_2.png"))
        self.__INTRO_IMAGES.append(ImageSprite("sprite_images/SAGE_TITLE_4.png"))
        self.__INTRO_IMAGES.append(ImageSprite("sprite_images/SAGE_TITLE_1.png"))
        self.__DRUM_KICKS = pygame.mixer.Sound("sound_effects/safari-kick-2-37314.mp3")
        self.__DRUM_KICKS.set_volume(2)


        ### MUSIC
        pygame.mixer.init()
        self.__MUSIC_BOSS = pygame.mixer.Sound("sound_effects/PumpkinMoonLord.mp3")
        #self.__MUSIC_BOSS.set_volume(1)
        self.__MUSIC_HOME = pygame.mixer.Sound("sound_effects/The Caretaker - Everywhere at the end of time - 09 B3 - Quiet internal rebellions.mp3")
        self.__SLASH = pygame.mixer.Sound("sound_effects/swinging-staff-whoosh-strong-08-44658.mp3")
        self.__MUSIC_HOME.set_volume(0.1)
        self.__SLASH.set_volume(0.05)
        self.__HIT = pygame.mixer.Sound("sound_effects/punch-140236.mp3")
        self.__DEATH_SOUND = pygame.mixer.Sound("sound_effects/deathScene.mp3")

    def initializeHands(self):
        ### Set scales
        self.__LASER_HAND.setScale(2.5)
        self.__FIRE_2.setScale(0.5)
        self.__FIRE_1.setScale(0.5)
        self.__LASER_BEAM.setScale(1.5)
        self.__THUMB.setScale(1.2)
        self.__FIRE_HAND.setScale(1.2)

        ### Set SPD
        self.__LASER_HAND.setSPD(3)
        self.__FIRE_2.setSPD(5)
        self.__FIRE_2.setSPD_Y(3)
        self.__FIRE_1.setSPD(5)
        self.__FIRE_1.setSPD_Y(3)
        self.__THUMB.setSPD(3)
        self.__LASER_BEAM.setSPD(10)

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
                        (190 + (300 * j)),
                        (90 + (150 * x))
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

    def peacefulNight(self):
        ###################################################
        self.__MUSIC_HOME.play(-1)
        ###################################################
        BAR_COUNT = 0
        for bar in self.__PLAYER.HEALTH_BAR:
            BAR_COUNT += 1
            bar.setPosition((5000, 5000))

        ### PLATFORMS
        PLATFORM_COUNTER = -1
        for x in range(3):
            for j in range(2):
                PLATFORM_COUNTER += 1
                self.__PLATFORMS[PLATFORM_COUNTER].setPosition(
                    (
                        (5000),
                        (5000)
                    )
                )

        ### HANDS
        self.__FIRE_HAND.setPosition((5000, 5000))
        self.__FIRE_2.resetLaserPOS(self.__FIRE_HAND)
        self.__FIRE_1.resetLaserPOS(self.__FIRE_HAND)
        self.__THUMB.setPosition(
            (
                5000, 5000
            )
        )
        # LASER HAND
        self.__LASER_HAND.setPosition(
            (
                5000,
                5000
            )
        )
        # LASER HORIZONTAL
        self.__LASER_BEAM.setPosition(
            (
                5000,
                5000
            )
        )
        # PLAYER
        self.__PLAYER.setPosition((0, self.__WINDOW.getHeight()))
        # BOSS
        self.__BOSS.setPosition((5000, 5000))
        ### BOSS HEALTH
        BAR_COUNT = 0
        for bar in self.__BOSS.HEALTH_BAR:
            bar.setPosition((5000, 5000))
            BAR_COUNT += 1

        clock = pygame.time.Clock()

        while self.__AT_START_LEVEL:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            PRESSED_KEYS = pygame.key.get_pressed()
            TIME = clock.tick()
            ### PLAYER
            self.__PLAYER.WALK_TIME_ELAPSED += TIME
            self.__PLAYER.movePlayer(PRESSED_KEYS)
            COLLIDING_PLATFORM = 0
            # JUMP
            if self.__PLAYER.IS_JUMPING:
                ##############################
                self.__SLASH.play(0)
                ##############################
                self.__PLAYER.jumpPlayer()
                self.__PLAYER.ATTACK_EFFECT.setPosition(
                    (self.__PLAYER.getPOS()[0] + self.__PLAYER.getWidth(), self.__PLAYER.getPOS()[1]))
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
            self.__PLAYER.checkBoundries(self.__WINDOW.getWidth(),
                                         self.__WINDOW.getHeight() - self.__GROUND.getHeight())
            if self.__PLAYER.isSpriteColliding(self.__GROUND.getPOS(), self.__GROUND.getDiminsoins()):
                self.__PLAYER.JUMPING_Y = 0

            self.blitPeacefulNight()

            if self.__PLAYER.getPOS()[0] > (self.__WINDOW.getWidth() * (9/10)):
                self.__AT_START_LEVEL = False
        self.bossIntro()

    def bossIntro(self):
        #####################################
        self.__MUSIC_HOME.stop()
        self.__MUSIC_BOSS.play(-1)
        #####################################
        clock = pygame.time.Clock()
        intro = True
        time_since_frame = 0
        index = 0
        self.__DRUM_KICKS.play(0)
        while intro:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            TIME = clock.tick()
            time_since_frame += TIME
            if time_since_frame >= 400:
                self.__DRUM_KICKS.stop()
                #############################
                self.__DRUM_KICKS.play(0)
                #############################
                index += 1
                time_since_frame = 0
            if index <= 3:
                self.__WINDOW.ClearScreen()
                ###### BG
                self.__WINDOW.getSurface().blit(self.__INTRO_IMAGES[index].getSurface(),
                                                    self.__INTRO_IMAGES[index].getPOS())
                self.__WINDOW.updateFrames()
            else:
                intro = False

        self.bossRoom()

    def titleScreen(self):
        title = True
        while title:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            PRESSED_KEYS = pygame.key.get_pressed()
            if PRESSED_KEYS[pygame.K_SPACE]:
                time.sleep(1)
                title = False
            self.__WINDOW.ClearScreen()
            self.__WINDOW.getSurface().blit(self.__MAIN_TITLE.getSurface(), self.__MAIN_TITLE.getPOS())
            self.__WINDOW.updateFrames()
        self.peacefulNight()


    def bossRoom(self):



        ### HANDS
        time_since_fall = 0
        time_since_laser = 0
        clock = pygame.time.Clock()
        boss_hit = False
        player_hit = False

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
                self.__THUMB.setSprite("sprite_images/thumb.png")
                self.__THUMB.setScale(1.2)
            if time_since_fall > 1200:
                if self.__ATTACK_THUMB:
                    self.__THUMB.setPosition((self.__PLAYER.getPOS()[0], self.__THUMB.getPOS()[1]))
                    self.__ATTACK_THUMB = False
                self.__THUMB.fall()
                self.__THUMB.setSprite("sprite_images/thumb (3).png")
                self.__THUMB.setScale(1.2)
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
                ##############################
                self.__SLASH.stop()
                self.__SLASH.play(0)
                ##############################
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

            ######################### BOSS IMMUNITY FRAME
            if self.__BOSS.IMM_FRAME >= 500:
                self.__BOSS.IMM_FRAME = 0
                boss_hit = False

            if self.__PLAYER.ATTACK_EFFECT.isSpriteColliding(self.__BOSS.getPOS(), self.__BOSS.getDiminsoins()) and \
                    not boss_hit:
                boss_hit = True
                if len(self.__BOSS.HEALTH_BAR) > 0:
                    self.__BOSS.deductHealth()
                    self.__HIT.play(0)

            if boss_hit:
                self.__BOSS.IMM_FRAME += TIME

            ######################### PLAYER IMMUNITY
            if self.__PLAYER.IMM_FRAME >= 500:
                self.__PLAYER.IMM_FRAME = 0
                player_hit = False
            ##### TAKES DAMAGE
            for i in range(len(self.__DANGER_LIST)):
                if self.__PLAYER.isSpriteColliding(self.__DANGER_LIST[i].getPOS(), self.__DANGER_LIST[i].getDiminsoins()) and \
                        not player_hit:
                    player_hit = True
                    if len(self.__PLAYER.HEALTH_BAR) > 0:
                        ######### if hit by the thumb, which is last in the list, take 3 pts damage
                        if i == len(self.__DANGER_LIST)-1:
                            self.__PLAYER.deductHealth(3)
                        else:
                            self.__PLAYER.deductHealth(1)
            if player_hit:
                self.__PLAYER.IMM_FRAME += TIME

            ################### END
            if len(self.__BOSS.HEALTH_BAR) <= 0:
                self.__MUSIC_BOSS.fadeout(2000)
                self.__WIN = True
                self.__AT_BOSS_LEVEL = False
                # self.__AT_BOSS_LEVEL = False
            if len(self.__PLAYER.HEALTH_BAR) <= 0:
                self.__MUSIC_BOSS.fadeout(3000)
                self.__AT_BOSS_LEVEL = False

            ###### BLIT
            self.__WINDOW.ClearScreen()
            self.blitBossLevel()
            self.__WINDOW.updateFrames()
        if self.__WIN:
            time.sleep(2)
            self.notMth()
            self.winScreen()
        elif not self.__WIN:
            time.sleep(1)
            self.deathScreen()

    def notMth(self):
        math = True
        clock = pygame.time.Clock()
        time_since_frame = 0
        ###################################
        self.__MUSIC_BOSS.stop()
        self.__NOT_MATH_SOUND.play()
        ##################################3
        while math:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            TIME = clock.tick()
            time_since_frame += TIME
            if time_since_frame >= 4000:
                math = False
            self.__WINDOW.ClearScreen()
            self.__WINDOW.getSurface().blit(self.__THIS_IS_NOT_MTH.getSurface(),
                                            self.__THIS_IS_NOT_MTH.getPOS())
            self.__WINDOW.updateFrames()

    def winScreen(self):
        from random import randrange
        clock = pygame.time.Clock()
        explode = True
        time_since_frame = 0
        self.__EXPLOSION_SOUND.play(0)
        explosion_counter = 0
        self.__EXPLOSION.setPosition((randrange(self.__BOSS.getPOS()[0],
                                                self.__BOSS.getPOS()[0] +
                                                self.__BOSS.getWidth() - 450),
                                      randrange(self.__BOSS.getPOS()[1],
                                                self.__BOSS.getPOS()[1] +
                                                self.__BOSS.getHeight() - 400)))
        end = True
        while explode:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            TIME = clock.tick()
            time_since_frame += TIME
            if explosion_counter < 16:
                if time_since_frame >= 30:
                    self.__EXPLOSION.setPosition((2000, 2000))
                if time_since_frame >= 110:
                    flip = randrange(0,2)
                    if flip == 0:
                        self.__EXPLOSION.setFlipX()
                    self.__EXPLOSION_SOUND.stop()
                    self.__EXPLOSION_SOUND.play(0)
                    time_since_frame = 0
                    # EXPLOSION
                    explosion_counter += 1
                    self.__EXPLOSION.setPosition((randrange(self.__BOSS.getPOS()[0],
                                                            self.__BOSS.getPOS()[0] +
                                                            self.__BOSS.getWidth() - 450),
                                                  randrange(self.__BOSS.getPOS()[1],
                                                            self.__BOSS.getPOS()[1] +
                                                            self.__BOSS.getHeight() - 400)))
                self.__WINDOW.ClearScreen()
                self.blitBossLevel()
                self.__WINDOW.getSurface().blit(self.__EXPLOSION.getSurface(),
                                                self.__EXPLOSION.getPOS())
                self.__WINDOW.updateFrames()
            else:
                if end:
                    self.__END_SOUND.play(0)
                    end = False
                self.__WINDOW.ClearScreen()
                self.__WINDOW.getSurface().blit(self.__INTRO_IMAGES[0].getSurface(), self.__INTRO_IMAGES[0].getPOS())
                self.__WINDOW.updateFrames()


    def deathScreen(self):
        #####################################
        self.__DEATH_SOUND.play(0)
        #####################################
        death = True
        while death:
            ### INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            PRESSED_KEYS = pygame.key.get_pressed()
            if PRESSED_KEYS[pygame.K_SPACE]:
                death = False


            self.__WINDOW.ClearScreen()
            ###### BG
            self.__WINDOW.getSurface().blit(self.__DEATH_BG.getSurface(),
                                            self.__DEATH_BG.getPOS())
            self.__WINDOW.updateFrames()


    def blitPeacefulNight(self):
        self.__WINDOW.ClearScreen()
        ###### BG
        self.__WINDOW.getSurface().blit(self.__BG_PEACEFUL_NIGHT.getSurface(), self.__BG_PEACEFUL_NIGHT.getPOS())
        # ATTACK EFFECT
        self.__WINDOW.getSurface().blit(self.__PLAYER.ATTACK_EFFECT.getSurface(), self.__PLAYER.ATTACK_EFFECT.getPOS())
        # GROUND
        self.__WINDOW.getSurface().blit(self.__GROUND.getSurface(), self.__GROUND.getPOS())
        # PLAYER HEALTH
        ###################
        for health_bar in self.__PLAYER.HEALTH_BAR:
            self.__WINDOW.getSurface().blit(health_bar.getSurface(), health_bar.getPOS())
        # PLAYER
        self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())

        self.__WINDOW.updateFrames()

    def blitBossLevel(self):

        ###### BG
        self.__WINDOW.getSurface().blit(self.__BG.getSurface(), self.__BG.getPOS())
        ##### BOSS - BLIT BEFORE PLAYER #####
        self.__WINDOW.getSurface().blit(self.__BOSS.getSurface(), self.__BOSS.getPOS())

        # PLATFORM
        for platform in self.__PLATFORMS:
            self.__WINDOW.getSurface().blit(platform.getSurface(), platform.getPOS())
        # ATTACK EFFECT
        self.__WINDOW.getSurface().blit(self.__PLAYER.ATTACK_EFFECT.getSurface(), self.__PLAYER.ATTACK_EFFECT.getPOS())
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
        # PLAYER
        self.__WINDOW.getSurface().blit(self.__PLAYER.getSurface(), self.__PLAYER.getPOS())
        # THUMB
        self.__WINDOW.getSurface().blit(self.__THUMB.getSurface(), self.__THUMB.getPOS())
        # BOSS HEALTH
        for bar in self.__BOSS.HEALTH_BAR:
            self.__WINDOW.getSurface().blit(bar.getSurface(), bar.getPOS())



if __name__ == "__main__":
    pygame.init()
    GAME = Engine()
    GAME.titleScreen()




