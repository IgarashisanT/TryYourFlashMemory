from enum import Enum,auto
import random 
import pyxel as pyxel
from constants import Window, Difficulty, Resource
from lib.input import Input
from lib.selector_group import SelectorGroup

# 開始カウントダウン
COUNTDOWN_NUM = 3
COUNTDOWN_UNIT_TICK = 30

# フラッシュ表示
SHOW_TICK = 30

class GameScene:

    class State:
        COUNT = 1
        SHOW = auto()
        INPUT = auto()
        CHECK = auto()

    def __init__(self, game) -> None:
        self.game = game
        self.input = self.game.app.input
        self.state = self.State.COUNT
        self.count = COUNTDOWN_NUM
        self.tick_count = 0
        self.difficulty = self.game.game_vars.difficulty
        self.result = ''

        if self.difficulty == Difficulty.EASY:
            self.digit = 5
        if self.difficulty == Difficulty.NORMAL:
            self.digit = 7
        if self.difficulty == Difficulty.HARD:
            self.digit = 10
        
        self.selector_group = SelectorGroup(self.digit,( Window.WIDTH - self.digit * 5 ) / 2, 40,self.input)
        self.answer = self.__generate_random_number_string(self.digit)
    
    def on_exit(self):
        pyxel.stop()

    def update(self):
        if self.state == self.State.COUNT:
            self.update_count()
        elif  self.state == self.State.SHOW:
            self.update_show()
        elif  self.state == self.State.INPUT:
            self.update_input()
        elif  self.state == self.State.CHECK:
            self.update_check()

    def draw(self):
        if self.state == self.State.COUNT:
            self.draw_count()
        elif  self.state == self.State.SHOW:
            self.draw_show()
        elif  self.state == self.State.INPUT:
            self.draw_input()
        elif  self.state == self.State.CHECK:
            self.draw_check()

    # region カウントダウン

    def update_count(self):
        self.tick_count += 1
        if self.tick_count == COUNTDOWN_UNIT_TICK:
            self.tick_count = 0
            self.count -= 1
            if self.count == 0:
                self.state = self.State.SHOW

    def draw_count(self):
        pyxel.text((Window.WIDTH - 2) / 2,(Window.HEIGHT - 8) / 2,str(self.count),pyxel.COLOR_WHITE)

    # endregion

    # region 表示

    def update_show(self):
        self.tick_count += 1
        if self.tick_count == SHOW_TICK:
            self.tick_count = 0
            self.state = self.State.INPUT

    def draw_show(self):
        top_x = (Resource.Display.WIDTH - len(self.answer) * (Resource.NumberGraphic.WIDTH) - ((len(self.answer) - 1 ) * Resource.NumberGraphic.MARGIN) + Resource.Display.TOP_X) / 2
        top_y = (Resource.Display.HEIGHT - Resource.NumberGraphic.HEIGHT) / 2 + Resource.Display.TOP_Y
        for i in range(0,len(self.answer)):
            pyxel.blt(top_x + i * (Resource.NumberGraphic.WIDTH + Resource.NumberGraphic.MARGIN),top_y,0,Resource.NumberGraphic.TOP_U + Resource.NumberGraphic.WIDTH * int(self.answer[i]),Resource.NumberGraphic.TOP_V,Resource.NumberGraphic.WIDTH,Resource.NumberGraphic.HEIGHT,pyxel.COLOR_BLACK)

    # endregion

    # region 入力

    def update_input(self):
        self.selector_group.update()

        if self.input.has_tapped(Input.BUTTON_1) or \
            self.input.has_tapped(Input.BUTTON_2):
            self.state = self.State.CHECK
    
    def draw_input(self):
        self.selector_group.draw()

    # endregion

    # region 結果確認

    def update_check(self):
        self.tick_count += 1

        # TODO 実装
        if self.tick_count == 1:
            if self.__get_correct_amount() == len(self.answer):
                self.result = 'CORRECT'
            else:
                self.result = 'INCORRECT'

        if self.input.has_tapped(Input.BUTTON_1) or \
            self.input.has_tapped(Input.BUTTON_2):
            self.state = self.game.go_to_title()
    
    def draw_check(self):
        self.selector_group.draw()
        pyxel.text((Window.WIDTH - 24 * 4 )/ 2,(Window.HEIGHT - 8) / 2,self.result,pyxel.COLOR_WHITE)
        if self.result == 'INCORRECT':
            pyxel.text((Window.WIDTH - 24 * 4 )/ 2,(Window.HEIGHT - 8) / 2 + 10,'' + str(self.__get_correct_amount()) + ' / ' + str(self.digit),pyxel.COLOR_WHITE)
            pyxel.text((Window.WIDTH - 24 * 4 )/ 2,(Window.HEIGHT - 8) / 2 + 20,'Correct answer is ' + self.answer,pyxel.COLOR_WHITE)

        pyxel.text((Window.WIDTH - 16 * 4 )/ 2,Window.HEIGHT * 5 / 8,'Press A/B button',pyxel.COLOR_WHITE)
        pyxel.text((Window.WIDTH - 16 * 4 )/ 2,Window.HEIGHT * 5 / 8 + 8,'to go to Title.',pyxel.COLOR_WHITE)

    # endregion

    # region private method

    # 指定した桁数のランダム数字文字列を取得する
    def __generate_random_number_string(self,n):
        if n <= 10:
            # 10桁以下の場合、重複なし
            return ''.join(random.sample('0123456789', n))
        else:
            # 10桁以上の場合、重複を最小限にする
            result = list('0123456789')
            additional_digits = n - 10
            for _ in range(additional_digits):
                result.append(random.choice('0123456789'))
            random.shuffle(result)
            return ''.join(result)
        
    # 合っている文字数を取得する
    def __get_correct_amount(self):
        user_input = self.selector_group.get_value()
        correct_amount = 0
        for i in range(0,len(user_input)):
            if user_input[i:i+1] == self.answer[i:i+1]:
                correct_amount += 1
        return correct_amount

    # endregion