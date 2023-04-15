import threading
import time
from threading import Thread

import settings
from settings import *
import pygame as pg
from player import Player

if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    player = Player(WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, screen)
    player.start()
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings.running = False
                time.sleep(1)
                pg.quit()
                quit()
        #print(threading.activeCount())

