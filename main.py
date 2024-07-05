import pyxel
from game import Game
from constants import Window
from lib.input import Input

class App:
    def __init__(self):
        pyxel.init(Window.WIDTH, Window.HEIGHT,title=Window.TITLE)

        self.input = Input()
        self.game = Game(self)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.input.update()
        self.game.update()

    def draw(self):
        pyxel.cls(0)
        self.game.draw()

App()