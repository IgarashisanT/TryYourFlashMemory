import pyxel as pyxel

from constants import Difficulty
from constants import Window
from constants.general import General
from lib.input import Input

TITLE_X = (Window.WIDTH - len(General.GAME_TITLE) * 4) / 2
TITLE_Y = Window.HEIGHT / 4

MENU_TOP_X = ( Window.WIDTH - 16 * 4 ) / 2
MENU_TOP_Y = Window.HEIGHT * 4 / 7

class TitleScene:
    def __init__(self, game) -> None:
        self.game = game
        self.input = self.game.app.input
        
        self.selections = {
            0 : {
                "loc" : [MENU_TOP_X,MENU_TOP_Y],
                "label" : "EASY   (5 digits)",
                "action" : self.game.go_to_game,
                "difficulty":Difficulty.EASY,
            },
            1 : {
                "loc" : [MENU_TOP_X,MENU_TOP_Y + 10],
                "label" : "NORMAL (7 digits)",
                "action" : self.game.go_to_game,
                "difficulty":Difficulty.NORMAL,
            },
            2 : {
                "loc" : [MENU_TOP_X,MENU_TOP_Y + 20],
                "label" : "HARD   (10 digits)",
                "action" : self.game.go_to_game,
                "difficulty":Difficulty.HARD,
            },
        }
        
        self.selected_index = 0
    
    def on_exit(self):
        pyxel.stop()

    def update(self):
        if self.input.has_tapped(Input.UP):
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = 2
        elif self.input.has_tapped(Input.DOWN):
            self.selected_index += 1
            if self.selected_index > 2:
                self.selected_index = 0

        if self.input.has_tapped(Input.BUTTON_1) or \
            self.input.has_tapped(Input.BUTTON_2):
            (self.selections[self.selected_index]["action"])(self.selections[self.selected_index]["difficulty"])
    
    def draw(self):
        for k, v in self.selections.items():
            loc = v["loc"]
            if k == self.selected_index:
                selector_x = loc[0] - 8
                selector_y = loc[1]
                pyxel.tri(selector_x, selector_y, selector_x + 4, selector_y + 2, selector_x, selector_y + 4,pyxel.COLOR_YELLOW)

            pyxel.text(loc[0],loc[1],v["label"],pyxel.COLOR_WHITE)

            pyxel.text(TITLE_X, TITLE_Y, General.GAME_TITLE, pyxel.COLOR_WHITE)