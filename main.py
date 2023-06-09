import sys
import pygame as pg
from game.game import Game
from game.settings import TITLE


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption(TITLE)
    g = Game()
    while g.running:
        g.update_screen()
        if not g.player.living:
            g.game_over()
            if g.running:
                g.new_game()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                while len(g.sprites):
                    sprite = g.sprites[0]
                    sprite.kill()
                    sprite.join()
                g.running = False

    pg.quit()
    sys.exit()
