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
        self._readonly = False
        
        for i in range(0,self.amount):
            self.selectors.append(Selector(self.x + i * (self.PADDING + Selector.NumberGraphic.WIDTH), self.y, pyxel.COLOR_WHITE, self.input))
        self.selectors[0].activate()

    def update(self):
        for s in self.selectors:
            s.update()
        
        if self._readonly:
            return
        
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

    def set_y(self,y):
        self.y = y
        for selector in self.selectors:
            selector.y = y

    def draw(self):
        for s in self.selectors:
            s.draw()

    def get_value(self):
        value = ''
        for s in self.selectors:
            value += s.get_value()
        return value
    
    def change_to_readonly(self):
        '''
        読み取り専用(操作不能)に切り替える
        '''
        self._readonly = True
        self.selectors[self.active_index].deactivate()

    def change_to_active(self):
        '''
        読み取り専用を解除し、操作可能に切り替える
        '''
        self._readonly = False
        self.selectors[self.active_index].activate()

    def all_results_shown(self):
        '''
        全ての結果アイコンが表示されているか判定する
        '''
        for i in range(0,self.amount):
            if self.selectors[i].state == Selector.State.INPUT:
                return False
        return True

    def show_next_result(self,answer):
        '''
        結果アイコンをひとつ表示する
        (※左から順に表示していく)
        ※引数のanswerは正解の数字文字列
        ※正解ならTrue, 不正解ならFalseを返却
        '''
        for i in range(0,self.amount):
            if self.selectors[i].state == Selector.State.INPUT:
                if self.selectors[i].get_value() == answer[i]:
                    self.selectors[i].update_state(Selector.State.CORRECT)
                    return True
                else:
                    self.selectors[i].update_state(Selector.State.INCORRECT)
                    return False

    def hide_all_results(self):
        '''
        全ての結果アイコンを非表示にする
        '''
        for i in range(0,self.amount):
            self.selectors[i].update_state(Selector.State.INPUT)