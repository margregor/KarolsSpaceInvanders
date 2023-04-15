import random
import time
from threading import Timer
import sys

import settings
from settings import *
import pygame as pg
from player import Player
from enemy import Enemy

score = 0


def spawn_enemy(number):
    print(number)
    for _ in range(random.randint(number//2, int(number))):
        Enemy(WIDTH*random.random() % (WIDTH - ENEMY_WIDTH), -ENEMY_HEIGHT - random.randint(0, HEIGHT), screen).start()
    t = Timer(3, spawn_enemy, kwargs={"number": number + 0.5})
    t.start()


def draw_score():
    if not settings.running:
        return
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    pg.draw.rect(screen, BACKGROUND_COLOR, (10, 10, score_text.get_width() + 10, score_text.get_height()))
    screen.blit(score_text, [10, 10])
    Timer(0.1, draw_score).start()


def update_score():
    global score
    if not settings.running:
        return
    score += 1
    Timer(1, update_score).start()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    pg.display.set_caption(TITLE)
    font = pg.font.SysFont(None, 40)
    Player(WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, screen).start()
    spawn_enemy(10.0)
    update_score()
    draw_score()

    while settings.running:
        #screen.fill(BACKGROUND_COLOR)
        #draw_score()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings.running = False
                time.sleep(1)
                pg.quit()
                sys.exit()
        #print(threading.activeCount())

