from time import sleep
from threading import Thread, Lock

import pygame as pg

from game.settings import BULLET_SPEED, BULLET_WIDTH, BULLET_HEIGHT, SYNC, HEIGHT
from game.support import bullet_image


class Bullet(Thread):
    """Class representing bullet thread"""
    def __init__(self, x, y, surface, sprites, bullets, direction):
        Thread.__init__(self)
        self.speed = BULLET_SPEED
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.pos = pg.Vector2(x, y)
        self.surface = surface
        self.image = bullet_image
        self.image = pg.transform.scale(self.image, (BULLET_WIDTH, BULLET_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.living = True
        self.bullets = bullets
        self.bullets.append(self)
        self.lock = Lock()
        self.direction = direction
        self.sprites = sprites
        self.sprites.append(self)
        self.clock = pg.time.Clock()

    def run(self):
        """Main function of bullet thread"""
        while self.living:
            with self.lock:
                delta = self.clock.tick() / 1000
                self.move(delta)
                self.check_life()

            sleep(SYNC)

    def update(self):
        """Function drawing bullet image on screen"""
        self.surface.blit(self.image, self.rect)

    def move(self, delta):
        """Function moving bullet rectangle"""
        self.pos.y += self.direction * self.speed * delta
        self.rect.topleft = self.pos

    def check_life(self):
        """Function checking if bullet is out of screen"""
        if (self.pos.y + self.height < 0 and self.direction == -1) \
                or (self.pos.y > HEIGHT and self.direction == 1):
            self.kill()

    def kill(self):
        """Function killing thread"""
        self.living = False
        if self in self.bullets:
            self.bullets.remove(self)
            self.sprites.remove(self)
