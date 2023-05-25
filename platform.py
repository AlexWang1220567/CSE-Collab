"""
title: the player class
author: Mengqi Wang
date-created: 05/12/2023
"""

from mySprite import mySprite
import pygame

class Platform(mySprite):
    def __init__(self, HEIGHT=0, WIDTH=0):
        mySprite.__init__(self, HEIGHT, WIDTH)
        self._COLOR = (0, 0, 0)
        self._SURFACE = pygame.Surface(self._DIM, pygame.SRCALPHA, 32)
        self._SURFACE.fill(self._COLOR)

    def isCollidingPlatform(self, POSITION, DIMINSION):
        SPRITE_X = POSITION[0]
        SPRITE_Y = POSITION[1]
        SPRITE_W = DIMINSION[0]
        SPRITE_H = DIMINSION[1]

        if SPRITE_X >= self._X - SPRITE_W and SPRITE_X <= self._X + self.getWidth():
            if SPRITE_Y >= self._Y - SPRITE_H and SPRITE_Y <= self._Y + self.getHeight():
                return True
        return False


class PlatfromPlacement():
    def __init__(self):
        pass

    def placement(self, PLATFORMS, WINDOW):
        for i in PLATFORMS:
            for x in range(3):
                print(x)
                for j in range(2):
                    print(j)
                    i.setPoistion(
                        (
                            (50 + (100 * j)),
                            (50 + (100 * x))
                        )
                    )



if __name__ == "__main__":

    from window import Window
    from player import Player
    from boss import Boss
    from imageSprite import ImageSprite

    pygame.init()

    WINDOW = Window("Image Sprite Test")
    PLATFORMS = []
    for i in range(6):
        PLATFORMS.append(Platform(25, 150))
    PLATFORM_COUNTER = -1
    for x in range(3):
        print(x)
        for j in range(2):
            print(j)
            PLATFORM_COUNTER += 1
            PLATFORMS[PLATFORM_COUNTER].setPosition(
                (
                    (200 + (300 * j)),
                    (100 + (170 * x))
                )
            )

    PLAYER = Player()
    # PLAYER.setScale(0.1)

    TIME_ELAPSED = 0

    # SPRITE CHANGE
    PLAYER.setFlipX()
    PLAYER.setPosition((0, WINDOW.getHeight() - PLAYER.getHeight()))

    PLATFORM = Platform(40, WINDOW.getWidth())
    PLATFORM.setPosition((0, WINDOW.getHeight() - PLATFORM.getHeight()))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        PRESSED_KEYS = pygame.key.get_pressed()

        ### PROCESSING
        PLAYER.WALK_TIME_ELAPSED += 1
        PLAYER.movePlayer(PRESSED_KEYS)
        COLLIDING_PLATFORM = 0
        # JUMP
        if PLAYER.IS_JUMPING:
            PLAYER.jumpPlayer()
            PLAYER.ATTACK_EFFECT.setPosition((PLAYER.getPOS()[0] + PLAYER.getWidth(), PLAYER.getPOS()[1]))
        # PLAYER IS FALLING
        else:
            for platform in PLATFORMS:
                #########################################
                if platform.isSpriteColliding(PLAYER.getPOS(), PLAYER.getDiminsoins()):
                ##########################################
                    if platform.isCollidingPlatform(PLAYER.getPOS(), PLAYER.getDiminsoins()):
                        PLAYER.JUMPING_Y = 0
                        PLAYER.IS_JUMPING = False
                        COLLIDING_PLATFORM += 1
            if COLLIDING_PLATFORM == 0:
                PLAYER.fall()
                PLAYER.ATTACK_EFFECT.setPosition((5000, 5000))
        PLAYER.checkBoundries(WINDOW.getWidth(), WINDOW.getHeight() - PLATFORM.getHeight())

        WINDOW.ClearScreen()
        WINDOW.getSurface().blit(PLAYER.getSurface(), PLAYER.getPOS())
        # PLATFORM
        for platform in PLATFORMS:
            WINDOW.getSurface().blit(platform.getSurface(), platform.getPOS())
        WINDOW.getSurface().blit(PLATFORM.getSurface(), PLATFORM.getPOS())
        # ATTACK EFFECT
        WINDOW.getSurface().blit(PLAYER.ATTACK_EFFECT.getSurface(), PLAYER.ATTACK_EFFECT.getPOS())
        WINDOW.updateFrames()
