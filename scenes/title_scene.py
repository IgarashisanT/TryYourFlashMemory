import pyxel as pyxel

from constants import Difficulty
from lib.input import Input

class TitleScene:
    def __init__(self, game) -> None:
        self.game = game
        self.input = self.game.app.input
        
        self.selections = {
            0 : {
                "loc" : [96,112],
                "label" : "EASY   (5 digits)",
                "action" : self.game.go_to_game,
                "difficulty":Difficulty.EASY,
            },
            1 : {
                "loc" : [96,128],
                "label" : "NORMAL (7 digits)",
                "action" : self.game.go_to_game,
                "difficulty":Difficulty.NORMAL,
            },
            2 : {
                "loc" : [96,144],
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

            pyxel.text(96,40,"TRY FLASH MEMORY",pyxel.COLOR_WHITE)