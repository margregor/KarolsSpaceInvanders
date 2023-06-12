from threading import Thread
from time import sleep

from game.settings import SYNC


class PlayerEnemiesCollisions(Thread):
    """Class checking player and enemies collisions"""
    def __init__(self, player, enemies, update_score):
        Thread.__init__(self)
        self.player = player
        self.enemies = enemies
        self.update_score = update_score

    def run(self):
        while self.player.living:
            for enemy in self.enemies:
                with self.player.lock, enemy.lock:
                    if self.player.pos.y < enemy.pos.y + enemy.height \
                            and self.player.pos.y + self.player.height > enemy.pos.y \
                            and self.player.pos.x < enemy.pos.x + enemy.width \
                            and self.player.pos.x + self.player.width > enemy.pos.x:
                        enemy.kill()
                        self.update_score()
                        self.player.damage()
            sleep(SYNC)
