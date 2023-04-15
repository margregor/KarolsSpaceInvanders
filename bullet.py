from time import sleep
from threading import Thread

import settings
from settings import *
import pygame as pg


class Bullet(Thread):
    def __init__(self, x, y, surface):
        Thread.__init__(self)
        self.speed = BULLET_SPEED
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x
        self.y = y
        self.surface = surface
        self.color = BULLET_COLOR
        self.living = True

    def run(self):
        while self.living and settings.running:
            self.move()
            #sleep(1)
            self.update()
            self.check_life()
            sleep(0.04)

    def update(self):
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        pg.display.update()

    def move(self):
        self.y -= self.speed

    def check_life(self):
        if self.y + self.height < 0:
            self.living = False
