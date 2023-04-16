import random
import threading
import time
from threading import Timer
import sys

import settings
from settings import *
import pygame as pg
from player import Player
from enemy import Enemy
from collisions import Collisions

score = [0]
enemies = []
bullets = []


def spawn_enemy(number):
    if not settings.running:
        return
    for _ in range(random.randint(number//2, int(number))):
        Enemy(WIDTH*random.random() % (WIDTH - ENEMY_WIDTH), -ENEMY_HEIGHT - random.randint(0, HEIGHT), screen,
              enemies).start()
    Timer(3, spawn_enemy, kwargs={"number": number + 0.5}).start()


def draw_score():
    if not settings.running:
        return
    score_text = font.render("Score: " + str(score[0]), True, (255, 255, 255))
    pg.draw.rect(screen, (150, 150, 150), (10, 10, score_text.get_width() + 10, score_text.get_height()))
    life_text = font.render("Lives: " + str(player.lives), True, (255, 255, 255))
    #life_text_rect = life_text.get_rect()
    pg.draw.rect(screen, BACKGROUND_COLOR, (655, 10, 135, life_text.get_height()))
    screen.blit(score_text, [10, 10])
    screen.blit(life_text, [655, 10])
    Timer(0.0, draw_score).start()


def update_score():
    global score
    if not settings.running:
        return
    score += 1
    Timer(1, update_score).start()


def update_screen():
    screen.fill(BACKGROUND_COLOR)
    pg.display.update()
    Timer(0.05, update_screen).start()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    pg.display.set_caption(TITLE)
    font = pg.font.SysFont(None, 40)
    player = Player(WIDTH//2, HEIGHT - PLAYER_HEIGHT - 10, screen, bullets)
    player.start()
    Collisions(score, player, bullets, enemies).start()
    spawn_enemy(10.0)
    #update_score()
    draw_score()

    while settings.running:
        #screen.fill(BACKGROUND_COLOR)
        #draw_score()
        #print(bullets)
        #print(enemies)
        pg.display.update()
        print(threading.active_count())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings.running = False
                time.sleep(1)
                pg.quit()
                sys.exit()

