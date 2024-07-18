import pyxel

from lib.input import Input

class Selector:
    class NumberGraphic:
        TOP_U = 0
        TOP_V = 0
        WIDTH = 8
        HEIGHT = 16

    ARROW_WIDTH = 6
    ARROW_HEIGHT = 6
    ARROW_NUMBER_PADDING = 1

    CHAR_WIDTH = 4
    CHAR_HEIGHT = 8
    VALUES = [0,1,2,3,4,5,6,7,8,9]

    def __init__(self,x,y,colkey,input:Input):
        self.x = x
        self.y = y
        self.colkey = colkey
        self.index = 0
        self.is_active = False
        self.input = input

    def update(self):
        if not self.is_active:
            return
        
        if self.input.has_tapped(Input.UP):
            self.index += 1
            if self.index > self.VALUES[len(self.VALUES) - 1]:
                self.index = 0
        elif self.input.has_tapped(Input.DOWN):
            self.index -= 1
            if self.index < 0 :
                self.index = self.VALUES[len(self.VALUES) - 1]

    def draw(self):
        if self.is_active :
            up_arrow_x = self.x + (self.NumberGraphic.WIDTH - self.ARROW_WIDTH) / 2
            up_arrow_y = self.y
            down_arrow_x = self.x + (self.NumberGraphic.WIDTH - self.ARROW_WIDTH) / 2
            down_arrow_y = self.y + self.ARROW_HEIGHT + self.ARROW_NUMBER_PADDING + self.NumberGraphic.HEIGHT + self.ARROW_NUMBER_PADDING
            pyxel.tri(up_arrow_x, up_arrow_y + (self.ARROW_HEIGHT - 1), up_arrow_x + self.ARROW_WIDTH - 1, up_arrow_y + (self.ARROW_HEIGHT - 1), up_arrow_x + self.ARROW_WIDTH / 2, up_arrow_y, pyxel.COLOR_WHITE)
            pyxel.tri(down_arrow_x, down_arrow_y, down_arrow_x + self.ARROW_WIDTH - 1, down_arrow_y, down_arrow_x + self.ARROW_WIDTH / 2, down_arrow_y + (self.ARROW_HEIGHT - 1), pyxel.COLOR_WHITE)

        pyxel.blt(self.x, self.y + self.ARROW_HEIGHT + self.ARROW_NUMBER_PADDING, 0, self.NumberGraphic.TOP_U + self.index * self.NumberGraphic.WIDTH, self.NumberGraphic.TOP_V,self.NumberGraphic.WIDTH, self.NumberGraphic.HEIGHT, pyxel.COLOR_BLACK)

    # 値を取得する
    def get_value(self):
        return str(self.VALUES[self.index])

    # アクティブ状態にする 
    def activate(self):
        self.is_active = True

    # アクティブ状態を解除する 
    def deactivate(self):
        self.is_active = False