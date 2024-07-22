import pyxel as pyxel

from constants import Difficulty,Window,General,Resource
from lib.input import Input

TITLE_X = ( Resource.Display.WIDTH - len(General.GAME_TITLE) * 4 + Resource.Display.TOP_X) / 2
TITLE_Y = Resource.Display.HEIGHT / 4 + Resource.Display.TOP_Y

MENU_TOP_X = ( Resource.Display.WIDTH - 16 * 4  + Resource.Display.TOP_X) / 2
MENU_TOP_Y = Resource.Display.HEIGHT * 2 / 3 + Resource.Display.TOP_Y

CLEARED_ICON_U = 0
CLEARED_ICON_V = 24
CLEARED_ICON_W = 8
CLEARED_ICON_H = 8

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
                pyxel.tri(selector_x, selector_y, selector_x + 4, selector_y + 2, selector_x, selector_y + 4,pyxel.COLOR_WHITE)

            pyxel.text(loc[0],loc[1],v["label"],pyxel.COLOR_WHITE)

            # TODO クリア済難易度( = game.game_vars.cleared_difficultiesに存在するもの)には印をつける
            if v["difficulty"] in self.game.game_vars.cleared_difficulties :
                a = []
                pyxel.blt(loc[0] + 75, loc[1], 0, CLEARED_ICON_U, CLEARED_ICON_V, CLEARED_ICON_W, CLEARED_ICON_H, pyxel.COLOR_BLACK)

            pyxel.text(TITLE_X, TITLE_Y, General.GAME_TITLE, pyxel.COLOR_WHITE)