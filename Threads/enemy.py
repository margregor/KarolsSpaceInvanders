import random
from time import sleep
from threading import Thread, Lock
from Threads import settings
from Threads.bullet import Bullet
from Threads.settings import *
import pygame as pg


class Enemy(Thread):
    def __init__(self, x, y, surface, enemies, bullets):
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
        self.lock = Lock()
        self.bullets = bullets

    def run(self):
        while self.living and settings.running:
            with self.lock:
                pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
                self.move()
                self.update()
                self.check_life()
                if random.randint(1, 10) == 1:
                    Bullet(self.x + self.width // 2 - BULLET_WIDTH // 2, self.y + self.height,
                           self.surface, self.bullets, 1).start()
            sleep(0.02)

    def update(self):
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        #pg.display.update()

    def move(self):
        self.y += self.speed
        self.x += self.speed//2 * random.choice([-1, 0, 1])
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
        elif self.x < 0:
            self.x = 0

    def check_life(self):
        if self.y > HEIGHT:
            self.kill()

    def kill(self):
        pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
        self.living = False
        self.enemies.remove(self)
