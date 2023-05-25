from time import sleep
from threading import Thread

from Threads import settings
import pygame as pg


class Collisions(Thread):
    def __init__(self, score, player, bullets, enemies, enemy_bullets):
        Thread.__init__(self)
        self.score = score
        self.player = player
        self.enemies = enemies
        self.bullets = bullets
        self.enemies_bullets = enemy_bullets
        self.clock = pg.time.Clock()

    def run(self):
        while settings.running:
            #print(self.enemies)
            dt = self.clock.tick() / 1000
            self.player_enemies_collisions()
            self.enemies_player_bullets_collision()
            self.player_enemies_bullets_collisions()
            sleep(0.01)

    def player_enemies_collisions(self):
        for enemy in self.enemies:
            with self.player.lock, enemy.lock:
                if self.player.y < enemy.y + enemy.height and self.player.y + self.player.height > enemy.y \
                        and self.player.x < enemy.x + enemy.width and self.player.x + self.player.width > enemy.x:
                    enemy.kill()
                    self.score[0] += 1
                    self.player.damage()

    def enemies_player_bullets_collision(self):
        for bullet in self.bullets:
            for enemy in self.enemies:
                with bullet.lock, enemy.lock:
                    if bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y \
                            and bullet.x < enemy.x + enemy.width and bullet.x + bullet.width > enemy.x:
                        bullet.destroy()
                        enemy.kill()
                        self.score[0] += 1

    def player_enemies_bullets_collisions(self):
        for bullet in self.enemies_bullets:
            with self.player.lock, bullet.lock:
                if bullet.y < self.player.y + self.player.height and bullet.y + bullet.height > self.player.y \
                        and bullet.x < self.player.x + self.player.width and bullet.x + bullet.width > self.player.x:
                    bullet.destroy()
                    self.player.damage()

