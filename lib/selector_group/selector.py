import pyxel

from lib.input import Input

class Selector:
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
            colkey = pyxel.COLOR_YELLOW
        else:
            colkey =  pyxel.COLOR_WHITE
        pyxel.text(self.x, self.y, str(self.VALUES[self.index]),colkey)

    # 値を取得する
    def get_value(self):
        return str(self.VALUES[self.index])

    # アクティブ状態にする 
    def activate(self):
        self.is_active = True

    # アクティブ状態を解除する 
    def deactivate(self):
        self.is_active = False