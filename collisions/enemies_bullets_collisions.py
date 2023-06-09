from threading import Thread
from time import sleep

from game.settings import SYNC


class EnemiesBulletsCollisions(Thread):
    """Class checking player and enemies bullets collisions"""
    def __init__(self, bullets, player):
        Thread.__init__(self)
        self.bullets = bullets
        self.player = player

    def run(self):
        while self.player.living:
            for bullet in self.bullets:
                with self.player.lock, bullet.lock:
                    if bullet.pos.y < self.player.pos.y + self.player.height \
                            and bullet.pos.y + bullet.height > self.player.pos.y \
                            and bullet.pos.x < self.player.pos.x + self.player.width \
                            and bullet.pos.x + bullet.width > self.player.pos.x:
                        bullet.kill()
                        self.player.damage()
            sleep(SYNC)
