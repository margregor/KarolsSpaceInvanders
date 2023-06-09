import random

from threading import Timer
import pygame as pg

from collisions.enemies_bullets_collisions import EnemiesBulletsCollisions
from collisions.player_bullets_collisions import PlayerBulletsCollisions
from collisions.player_enemies_collisions import PlayerEnemiesCollisions
from sprites.player import Player
from sprites.enemy import Enemy
from game.settings import WIDTH, ENEMY_HEIGHT, HEIGHT,\
    ENEMY_WIDTH, PLAYER_HEIGHT


class Game:
    """Class representing game"""
    def __init__(self):
        self.spawn_timer = None
        self.player = None
        self.score = None
        self.enemies = None
        self.bullets = None
        self.enemy_bullets = None
        self.sprites = None
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.font = pg.font.SysFont(None, 40)
        self.running = True
        self.background = pg.image.load('./graphics/darkPurple.png')
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.new_game()

    def new_game(self):
        """Function starting new game"""
        self.score = [0]
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.sprites = []
        self.player = Player(WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10, self.screen,
                             self.sprites, self.bullets)
        self.player.start()
        PlayerEnemiesCollisions(self.score, self.player, self.enemies).start()
        PlayerBulletsCollisions(self.score, self.bullets, self.enemies, self.player).start()
        EnemiesBulletsCollisions(self.enemy_bullets, self.player).start()
        self.spawn_enemy(10.0)

    def spawn_enemy(self, number):
        """Function spawning new enemies every 3 seconds"""
        if not self.player.living:
            return
        for _ in range(random.randint(number // 2, int(number))):
            Enemy(WIDTH * random.random() % (WIDTH - ENEMY_WIDTH), -ENEMY_HEIGHT
                  - random.randint(0, HEIGHT), self.screen, self.sprites, self.enemies,
                  self.enemy_bullets).start()
        self.spawn_timer = Timer(3, self.spawn_enemy, kwargs={"number": number + 0.5})
        self.spawn_timer.start()

    def draw_score(self):
        """Function drawing score and player lives on screen"""
        score_text = self.font.render("Score: " + str(self.score[0]), True, (255, 255, 255))
        pg.draw.rect(self.screen, (150, 150, 150),
                     (10, 10, score_text.get_width() + 10, score_text.get_height()))
        life_text = self.font.render("Lives: " + str(self.player.lives), True, (255, 255, 255))
        pg.draw.rect(self.screen, (150, 150, 150), (655, 10, 135, life_text.get_height()))
        self.screen.blit(score_text, [10, 10])
        self.screen.blit(life_text, [655, 10])

    def update_screen(self):
        """Function updating screen"""
        #self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
        for sprite in self.sprites:
            sprite.update()
        self.draw_score()
        pg.display.update()

    def game_over(self):
        """Function displaying game over screen and waiting for any key"""
        self.spawn_timer.cancel()
        font = pg.font.SysFont(None, 100)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score[0]}", True, (255, 255, 255))
        waiting = True
        while waiting:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(game_over_text, [WIDTH // 2 - game_over_text.get_width() // 2,
                                              HEIGHT // 2 - game_over_text.get_height()])
            self.screen.blit(score_text, [WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2])
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    while len(self.sprites):
                        sprite = self.sprites[0]
                        sprite.kill()
                        sprite.join()
                    self.running = False
                    waiting = False
                if event.type == pg.KEYDOWN:
                    waiting = False
