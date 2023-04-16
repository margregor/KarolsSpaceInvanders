from time import sleep
from threading import Thread, Timer

import settings
from settings import *
from bullet import Bullet
import pygame as pg


class Player(Thread):
    def __init__(self, x, y, surface, bullets):
        Thread.__init__(self)
        self.speed = PLAYER_SPEED
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = x
        self.y = y
        self.surface = surface
        self.color = PLAYER_COLOR
        self.lives = 100
        self.living = True
        self.can_fire = True
        self.bullets = bullets

    def run(self):
        while self.living and settings.running:
            pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
            self.move()
            self.update()
            sleep(0.02)

    def update(self):
        #self.surface.fill((0, 0, 0))
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        #pg.display.update()

    def move(self):
        #pg.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, self.width, self.height))
        if pg.key.get_pressed()[pg.K_LEFT] and self.x > 0:
            self.x -= self.speed
        elif pg.key.get_pressed()[pg.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        if pg.key.get_pressed()[pg.K_SPACE] and self.can_fire:
            self.fire()

    def fire(self):
        Bullet(self.x + self.width//2 - BULLET_WIDTH//2, self.y - BULLET_HEIGHT, self.surface, self.bullets).start()
        self.can_fire = False
        Timer(BULLET_RATE_OF_FIRE, self.check_fire).start()

    def check_fire(self):
        self.can_fire = True

    def damage(self):
        self.lives -= 1
        if self.lives < 0:
            self.living = False
