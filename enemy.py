import random
from time import sleep
from threading import Thread
import settings
from settings import *
import pygame as pg


class Enemy(Thread):
    def __init__(self, x, y, surface, enemies):
        Thread.__init__(self)
        self.speed = ENEMY_SPEED
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.x = x
        self.y = y
        self.surface = surface
        self.color = ENEMY_COLOR
        self.living = True
        self.enemies = enemies
        self.enemies.append(self)

    def run(self):
        while self.living and settings.running:
            pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
            self.move()
            #sleep(1)
            self.update()
            self.check_life()
            sleep(0.04)

    def update(self):
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        #pg.display.update()

    def move(self):
        self.y += self.speed
        self.x += random.randint(-10, 10)
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
        elif self.x < 0:
            self.x = 0

    def check_life(self):
        if self.y > HEIGHT:
            self.kill()

    def kill(self):
        pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
        self.enemies.remove(self)
        self.living = False