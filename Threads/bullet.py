from time import sleep
from threading import Thread, Lock

from Threads import settings
from Threads.settings import *
import pygame as pg


class Bullet(Thread):
    def __init__(self, x, y, surface, bullets, direction):
        Thread.__init__(self)
        self.speed = BULLET_SPEED
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x
        self.y = y
        self.surface = surface
        self.color = BULLET_COLOR
        self.living = True
        self.bullets = bullets
        self.bullets.append(self)
        self.lock = Lock()
        self.direction = direction

    def run(self):
        while self.living and settings.running:
            with self.lock:
                pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
                self.move()
                self.update()
                self.check_life()

            sleep(0.04)

    def update(self):
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.direction * self.speed

    def check_life(self):
        if (self.y + self.height < 0 and self.direction == -1) or (self.y > HEIGHT and self.direction == 1):
            self.destroy()

    def destroy(self):
        pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
        self.living = False
        self.bullets.remove(self)

