import random
from time import sleep
from threading import Thread, Lock
import pygame as pg

from game.support import enemies_images
from sprites.bullet import Bullet
from game.settings import FIRE_PROBABILITY, ENEMY_SPEED, ENEMY_WIDTH,\
    ENEMY_HEIGHT, BULLET_WIDTH, WIDTH, HEIGHT, SYNC


class Enemy(Thread):
    """Class representing enemy thread"""
    def __init__(self, x, y, surface, sprites, enemies, bullets):
        Thread.__init__(self)
        self.speed = ENEMY_SPEED
        self.width = ENEMY_WIDTH - 5
        self.height = ENEMY_HEIGHT - 5
        self.pos = pg.Vector2(x, y)
        self.surface = surface
        self.image = random.choice(enemies_images)
        self.image = pg.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.living = True
        self.enemies = enemies
        self.enemies.append(self)
        self.sprites = sprites
        self.sprites.append(self)
        self.lock = Lock()
        self.bullets = bullets
        self.clock = pg.time.Clock()

    def run(self):
        """Main function of enemy thread"""
        while self.living:
            with self.lock:
                delta = self.clock.tick() / 1000
                self.move(delta)
                self.check_life()
                if random.randint(1, FIRE_PROBABILITY) == 1:
                    Bullet(self.pos.x + self.width // 2 - BULLET_WIDTH // 2, self.pos.y
                           + self.height, self.surface, self.sprites, self.bullets, 1).start()
            sleep(SYNC)

    def update(self):
        """Function drawing enemy image"""
        with self.lock:
            self.surface.blit(self.image, self.rect)

    def move(self, delta):
        """Function moving enemy rectangle position"""
        self.pos.y += self.speed * delta
        self.pos.x += self.speed//2 * random.choice([-1, 0, 1]) * delta
        if self.pos.x + self.width > WIDTH:
            self.pos.x = WIDTH - self.width
        elif self.pos.x < 0:
            self.pos.x = 0

        self.rect.topleft = self.pos

    def check_life(self):
        """Function checking if enemy is out of screen"""
        if self.pos.y > HEIGHT:
            self.kill()

    def kill(self):
        """Function killing thread"""
        self.lock.locked()

        self.living = False
        self.enemies.remove(self)
        self.sprites.remove(self)
