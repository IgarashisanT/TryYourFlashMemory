from enum import auto
import pyxel as pyxel
from constants import Difficulty, General, Resource
from lib.input import Input

TITLE_X = ( Resource.Display.WIDTH - len(General.GAME_TITLE) * 4 + Resource.Display.TOP_X) / 2
TITLE_Y = Resource.Display.HEIGHT / 4 + Resource.Display.TOP_Y

MENU_TOP_X = ( Resource.Display.WIDTH - 16 * 4 ) / 2  + Resource.Display.TOP_X
MENU_TOP_Y = Resource.Display.HEIGHT * 5 / 7 + Resource.Display.TOP_Y

LOGO_PADDING_Y = 1
LOGO_1_U = 0
LOGO_1_V = 32
LOGO_1_W = 41
LOGO_1_H  = 16
LOGO_1_X = Resource.Display.TOP_X + (Resource.Display.WIDTH - LOGO_1_W) / 2
LOGO_1_Y = Resource.Display.TOP_Y + 34
LOGO_2_U = 0
LOGO_2_V  = 48
LOGO_2_W = 55
LOGO_2_H  = 16
LOGO_2_X = Resource.Display.TOP_X + (Resource.Display.WIDTH - LOGO_2_W) / 2
LOGO_2_Y = LOGO_1_Y + LOGO_1_H + LOGO_PADDING_Y
LOGO_3_U = 0
LOGO_3_V  = 64
LOGO_3_W = 153
LOGO_3_H  = 16
LOGO_3_X = Resource.Display.TOP_X + (Resource.Display.WIDTH - LOGO_3_W) / 2
LOGO_3_Y = LOGO_2_Y + LOGO_2_H + LOGO_PADDING_Y

CLEARED_ICON_U = 0
CLEARED_ICON_V = 24
CLEARED_ICON_W = 8
CLEARED_ICON_H = 8

SELECTED_TICK = 30
BLINK_TICK_UNIT = 5

class TitleScene:

    class State:
        SELECTING = 0
        SELECTED = auto()

    def __init__(self, game) -> None:
        self.game = game
        self.input = self.game.app.input
        self.state = self.State.SELECTING
        self.tick_count = 0
        
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
        if self.state == self.State.SELECTING:
            self.update_selecting()
        elif  self.state == self.State.SELECTED:
            self.update_selected()

    def update_selecting(self):
        if self.input.has_tapped(Input.UP):
            pyxel.play(3,Resource.Sound.SELECT)
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = 2
        elif self.input.has_tapped(Input.DOWN):
            pyxel.play(3,Resource.Sound.SELECT)
            self.selected_index += 1
            if self.selected_index > 2:
                self.selected_index = 0

        if self.input.has_tapped(Input.BUTTON_1) or \
            self.input.has_tapped(Input.BUTTON_2):
            pyxel.play(3, Resource.Sound.START)
            self.state = self.State.SELECTED
    
    def update_selected(self):
        self.tick_count += 1
        if self.tick_count == SELECTED_TICK:
            (self.selections[self.selected_index]["action"])(self.selections[self.selected_index]["difficulty"])
    
    def draw(self):
        for k, v in self.selections.items():
            loc = v["loc"]
            if k == self.selected_index and self.tick_count // BLINK_TICK_UNIT % 2 == 0:
                selector_x = loc[0] - 8
                selector_y = loc[1]
                pyxel.tri(selector_x, selector_y, selector_x + 4, selector_y + 2, selector_x, selector_y + 4,pyxel.COLOR_WHITE)

            pyxel.text(loc[0],loc[1],v["label"],pyxel.COLOR_WHITE)

            # クリア済難易度( = game.game_vars.cleared_difficultiesに存在するもの)には印をつける
            if v["difficulty"] in self.game.game_vars.cleared_difficulties :
                a = []
                pyxel.blt(loc[0] + 75, loc[1], 0, CLEARED_ICON_U, CLEARED_ICON_V, CLEARED_ICON_W, CLEARED_ICON_H, pyxel.COLOR_BLACK)

            # pyxel.text(TITLE_X, TITLE_Y, General.GAME_TITLE, pyxel.COLOR_WHITE)
            pyxel.blt(LOGO_1_X, LOGO_1_Y, 0, LOGO_1_U, LOGO_1_V, LOGO_1_W, LOGO_1_H, pyxel.COLOR_BLACK)
            pyxel.blt(LOGO_2_X, LOGO_2_Y, 0, LOGO_2_U, LOGO_2_V, LOGO_2_W, LOGO_2_H, pyxel.COLOR_BLACK)
            pyxel.blt(LOGO_3_X, LOGO_3_Y,  0, LOGO_3_U, LOGO_3_V, LOGO_3_W, LOGO_3_H, pyxel.COLOR_BLACK)