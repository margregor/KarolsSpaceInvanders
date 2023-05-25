from time import sleep
from threading import Thread, Timer, Lock

from Threads import settings
from Threads.settings import *
from Threads.bullet import Bullet
import pygame as pg


class Player(Thread):
    def __init__(self, x, y, surface, bullets, lock):
        Thread.__init__(self)
        self.speed = PLAYER_SPEED
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = x
        self.y = y
        self.surface = surface
        self.surface_lock = lock
        self.color = PLAYER_COLOR
        self.lives = 100
        self.living = True
        self.can_fire = True
        self.bullets = bullets
        self.lock = Lock()
        self.clock = pg.time.Clock()
        #self.image = pg.image.load('./graphics/player/0.png')
        #self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def run(self):
        while self.living and settings.running:
            with self.lock:
                dt = self.clock.tick() / 1000
                pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))
                self.move(dt)
                self.update()

            sleep(PLAYER_SYNC)
        pg.draw.rect(self.surface, BACKGROUND_COLOR, (self.x, self.y, self.width, self.height))

    def update(self):
        #self.surface.fill((0, 0, 0))
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        #self.surface.blit(self.image, (self.x, self.y))
        #pg.display.update()

    def move(self, dt):
        #pg.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, self.width, self.height))
        if pg.key.get_pressed()[pg.K_LEFT] and self.x > 0:
            #self.x -= self.speed
            self.x -= self.speed*dt*(1/PLAYER_SYNC)
            #self.rect.centerx = self.x
        elif pg.key.get_pressed()[pg.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

        if pg.key.get_pressed()[pg.K_UP] and self.y > 0:
            self.y -= self.speed
        elif pg.key.get_pressed()[pg.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed

        if pg.key.get_pressed()[pg.K_SPACE] and self.can_fire:
            self.fire()

    def fire(self):
        Bullet(self.x + self.width//2 - BULLET_WIDTH//2, self.y - BULLET_HEIGHT, self.surface, self.bullets, -1).start()
        self.can_fire = False
        Timer(BULLET_RATE_OF_FIRE, self.cooled).start()

    def cooled(self):
        self.can_fire = True

    def damage(self):
        self.lives -= 1
        if self.lives < 0:
            self.living = False
