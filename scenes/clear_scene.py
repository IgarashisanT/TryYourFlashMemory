import pyxel as pyxel

from constants import Resource

SHOW_TICKS = 90

TELOP_1 = "ALL CLEAR!"
TELOP_2 = "CONGRATULATIONS!"
TELOP_MARGIN_Y = 10
TELOP_1_Y = Resource.Display.TOP_Y + Resource.Display.HEIGHT / 2 - TELOP_MARGIN_Y / 2
TELOP_2_Y = Resource.Display.TOP_Y + Resource.Display.HEIGHT / 2 + TELOP_MARGIN_Y / 2

class ClearScene:
    def __init__(self, game) -> None:
        self.game = game
        self.input = self.game.app.input
        
        self.tick_count = 0
    
    def on_exit(self):
        pyxel.stop()

    def update(self):
        self.tick_count += 1
        if self.tick_count == SHOW_TICKS:
            self.state = self.game.go_to_title()

    def draw(self):
        telop_1_x = Resource.Display.TOP_X + (Resource.Display.WIDTH - len(TELOP_1) * 4) / 2
        telop_2_x = Resource.Display.TOP_X + (Resource.Display.WIDTH - len(TELOP_2) * 4) / 2

        pyxel.text(telop_1_x, TELOP_1_Y, TELOP_1, pyxel.COLOR_WHITE)
        pyxel.text(telop_2_x, TELOP_2_Y, TELOP_2, pyxel.COLOR_WHITE)