from time import sleep
from threading import Thread

import settings
from settings import *
import pygame as pg


class Collisions(Thread):
    def __init__(self, score, player, bullets, enemies):
        Thread.__init__(self)
        self.score = score
        self.player = player
        self.enemies = enemies
        self.bullets = bullets

    def run(self):
        while settings.running:
            #print(self.enemies)
            self.player_enemies_collisions()
            self.enemies_player_bullets_collision()

    def player_enemies_collisions(self):
        for enemy in self.enemies:
            if self.player.y < enemy.y + enemy.height and self.player.y + self.player.height > enemy.y \
                    and self.player.x < enemy.x + enemy.width and self.player.x + self.player.width > enemy.x:
                enemy.kill()
                self.player.damage()

    def enemies_player_bullets_collision(self):
        for enemy in self.enemies:
            for bullet in self.bullets:
                if bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y \
                        and bullet.x < enemy.x + enemy.width and bullet.x + bullet.width > enemy.x:
                    bullet.destroy()
                    enemy.kill()
                    self.score[0] += 1
