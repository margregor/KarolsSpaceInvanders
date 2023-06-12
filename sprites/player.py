from random import choice
from time import sleep
from threading import Thread, Timer, Lock
import pygame as pg

from game.settings import PLAYER_SPEED, PLAYER_HEIGHT, PLAYER_WIDTH, \
    MAX_LIVES, SYNC, HEIGHT, BULLET_WIDTH, BULLET_HEIGHT, BULLET_RATE_OF_FIRE, WIDTH
from game.support import player_images
from sprites.bullet import Bullet


class Player(Thread):
    """Class representing player"""
    def __init__(self, x, y, surface, sprites, bullets):
        Thread.__init__(self)
        self.sprites = sprites
        self.sprites.append(self)
        self.speed = PLAYER_SPEED
        self.width = PLAYER_WIDTH - 5
        self.height = PLAYER_HEIGHT - 5
        self.pos = pg.Vector2(x, y)
        self.surface = surface
        self.lives = MAX_LIVES
        self.living = True
        self.can_fire = True
        self.bullets = bullets
        self.lock = Lock()
        self.damage_lock = Lock()
        self.clock = pg.time.Clock()
        self.image = choice(player_images)
        self.image = pg.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)

    def run(self):
        while self.living:
            with self.lock:
                delta_time = self.clock.tick() / 1000
                self.move(delta_time)
            sleep(SYNC)

    def update(self):
        """Function drawing player image on screen"""
        self.surface.blit(self.image, self.rect)

    def move(self, delta):
        """Function moving player rectangle based on keyboard input"""
        if pg.key.get_pressed()[pg.K_LEFT] and self.pos.x > 0:
            self.pos.x -= self.speed * delta
        elif pg.key.get_pressed()[pg.K_RIGHT] and self.pos.x < WIDTH - self.width:
            self.pos.x += self.speed * delta

        if pg.key.get_pressed()[pg.K_UP] and self.pos.y > 0:
            self.pos.y -= self.speed * delta
        elif pg.key.get_pressed()[pg.K_DOWN] and self.pos.y < HEIGHT - self.height:
            self.pos.y += self.speed * delta

        if pg.key.get_pressed()[pg.K_SPACE] and self.can_fire:
            self.fire()

        self.rect.topleft = self.pos

    def fire(self):
        """Function creating new bullet object"""
        Bullet(self.pos.x + self.width//2 + BULLET_WIDTH // 4, self.pos.y - BULLET_HEIGHT,
               self.surface, self.sprites, self.bullets, -1).start()
        self.can_fire = False
        Timer(BULLET_RATE_OF_FIRE, self.cooled).start()

    def cooled(self):
        """Function to control fire rate"""
        self.can_fire = True

    def damage(self):
        """Function lowering player life"""
        with self.damage_lock:
            self.lives -= 1
            if self.lives <= 0:
                self.kill()

    def kill(self):
        """Function killing player thread"""
        self.living = False
        self.sprites.remove(self)
