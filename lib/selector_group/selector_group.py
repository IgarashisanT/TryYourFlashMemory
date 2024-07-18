import pyxel

from lib.input import Input
from lib.selector_group import Selector

class SelectorGroup:
    PADDING = 1

    def __init__(self, amount, x, y,input:Input):
        self.amount = amount
        self.x = x
        self.y = y
        self.active_index = 0
        self.input = input
        self.selectors = []
        
        for i in range(0,self.amount):
            self.selectors.append(Selector(self.x + i * (self.PADDING + Selector.NumberGraphic.WIDTH), self.y, pyxel.COLOR_WHITE, self.input))
        self.selectors[0].activate()

    def update(self):
        for s in self.selectors:
            s.update()
        
        if self.input.has_tapped(Input.RIGHT):
            nowIndex = self.active_index
            newIndex = nowIndex + 1
            if newIndex > self.amount - 1:
                newIndex = 0
            self.selectors[nowIndex].deactivate()
            self.selectors[newIndex].activate()
            self.active_index = newIndex
        elif self.input.has_tapped(Input.LEFT):
            nowIndex = self.active_index
            newIndex = nowIndex - 1
            if newIndex < 0 :
                newIndex = self.amount - 1
            self.selectors[nowIndex].deactivate()
            self.selectors[newIndex].activate()
            self.active_index = newIndex

    def draw(self):
        for s in self.selectors:
            s.draw()

    def get_value(self):
        value = ''
        for s in self.selectors:
            value += s.get_value()
        return value