from threading import Thread
from time import sleep

from game.settings import SYNC


class PlayerBulletsCollisions(Thread):
    """Class checking player bullets and enemies collisions"""
    def __init__(self, score, bullets, enemies, player):
        Thread.__init__(self)
        self.bullets = bullets
        self.enemies = enemies
        self.score = score
        self.player = player

    def run(self):
        while self.player.living:
            for bullet in self.bullets:
                for enemy in self.enemies:
                    with bullet.lock, enemy.lock:
                        if bullet.pos.y < enemy.pos.y + enemy.height \
                                and bullet.pos.y + bullet.height > enemy.pos.y \
                                and bullet.pos.x < enemy.pos.x + enemy.width \
                                and bullet.pos.x + bullet.width > enemy.pos.x:
                            bullet.kill()
                            enemy.kill()
                            self.score[0] += 1
            sleep(SYNC)
