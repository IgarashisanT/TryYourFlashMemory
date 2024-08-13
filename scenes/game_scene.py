from enum import auto
import random 
import pyxel as pyxel
from constants import Window, Difficulty, Resource
from lib.input import Input
from lib.selector_group import SelectorGroup,Selector

# 開始カウントダウン
COUNTDOWN_NUM = 3
COUNTDOWN_UNIT_TICK = 30

# フラッシュ表示
SHOW_TICK = 30

# 結果確認
SELECTOR_GROUP_UP_TO_Y = Resource.Display.TOP_Y + 30
RESULT_SHOW_UNIT_TICK = 10

class GameScene:

    class State:
        COUNT = 1
        SHOW = auto()
        INPUT = auto()
        CHECK_1 = auto()    # 解答を上にスクロール
        CHECK_2 = auto()    # 答え合わせ
        CHECK_3 = auto()    # 結果表示

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
        
        selector_group_top_x = Resource.Display.TOP_X + (Resource.Display.WIDTH - self.digit * Selector.NumberGraphic.WIDTH - (self.digit - 1) * SelectorGroup.PADDING) / 2
        selector_group_top_y = (Resource.Display.TOP_Y + Resource.Display.HEIGHT - (Selector.NumberGraphic.HEIGHT + (Selector.ARROW_HEIGHT + SelectorGroup.PADDING) * 2 )) / 2 + Resource.Display.TOP_Y

        self.selector_group = SelectorGroup(self.digit,selector_group_top_x, selector_group_top_y,self.input)
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
        elif  self.state == self.State.CHECK_1:
            self.update_check_1()
        elif  self.state == self.State.CHECK_2:
            self.update_check_2()
        elif  self.state == self.State.CHECK_3:
            self.update_check_3()


    def draw(self):
        if self.state == self.State.COUNT:
            self.draw_count()
        elif  self.state == self.State.SHOW:
            self.draw_show()
        elif  self.state == self.State.INPUT:
            self.draw_input()
        elif  self.state == self.State.CHECK_1:
            self.draw_check_1()
        elif  self.state == self.State.CHECK_2:
            self.draw_check_2()
        elif  self.state == self.State.CHECK_3:
            self.draw_check_3()

    # region カウントダウン

    def update_count(self):
        self.tick_count += 1
        if self.tick_count == COUNTDOWN_UNIT_TICK:
            self.tick_count = 0
            self.count -= 1
            if self.count == 0:
                self.state = self.State.SHOW

    def draw_count(self):
        count_x = Resource.Display.TOP_X + (Resource.Display.WIDTH - 4) / 2
        count_y = (Resource.Display.TOP_Y + Resource.Display.HEIGHT - 8 ) / 2 + Resource.Display.TOP_Y
        pyxel.text(count_x, count_y,str(self.count),pyxel.COLOR_WHITE)

    # endregion

    # region 表示

    def update_show(self):
        self.tick_count += 1
        if self.tick_count == SHOW_TICK:
            self.tick_count = 0
            self.state = self.State.INPUT

    def draw_show(self):
        top_x = Resource.Display.TOP_X + (Resource.Display.WIDTH - len(self.answer) * (Selector.NumberGraphic.WIDTH) - ((len(self.answer) - 1 ) * SelectorGroup.PADDING)) / 2
        top_y = (Resource.Display.TOP_Y + Resource.Display.HEIGHT - Selector.NumberGraphic.HEIGHT) / 2 + Resource.Display.TOP_Y
        for i in range(0,len(self.answer)):
            pyxel.blt(top_x + i * (Selector.NumberGraphic.WIDTH + SelectorGroup.PADDING),top_y,0,Selector.NumberGraphic.TOP_U + Selector.NumberGraphic.WIDTH * int(self.answer[i]),Selector.NumberGraphic.TOP_V,Selector.NumberGraphic.WIDTH,Selector.NumberGraphic.HEIGHT,pyxel.COLOR_BLACK)

    # endregion

    # region 入力

    def update_input(self):
        self.selector_group.update()

        if self.input.has_tapped(Input.BUTTON_1) or \
            self.input.has_tapped(Input.BUTTON_2):
            self.tick_count = 0
            self.state = self.State.CHECK_1
    
    def draw_input(self):
        self.selector_group.draw()

    # endregion

    # region 結果確認1

    def update_check_1(self):
        self.selector_group.change_to_readonly()
        self.selector_group.set_y(self.selector_group.y - 1)
        if self.selector_group.y == SELECTOR_GROUP_UP_TO_Y:
            self.tick_count = 0
            self.state = self.State.CHECK_2
    
    def draw_check_1(self):
        self.selector_group.draw()

    # endregion

    # region 結果確認2

    def update_check_2(self):
        self.tick_count += 1
        if self.tick_count == RESULT_SHOW_UNIT_TICK:
            self.tick_count = 0
            if self.selector_group.all_results_shown():
                if self.__get_correct_amount() == len(self.answer):
                    self.result = 'CORRECT'
                    self.game.game_vars.cleared_difficulties.append(self.difficulty)
                else:
                    self.result = 'INCORRECT'
                self.state = self.State.CHECK_3
            else:
                self.selector_group.show_next_result(self.answer)
    
    def draw_check_2(self):
        self.selector_group.draw()

    # endregion

    # region 結果確認3

    def update_check_3(self):
        if self.input.has_tapped(Input.BUTTON_1) or \
            self.input.has_tapped(Input.BUTTON_2):
            if self.__is_all_clear():
                self.state = self.game.go_to_clear()
            else:
                self.state = self.game.go_to_title()
    
    def draw_check_3(self):
        self.selector_group.draw()
        if self.result == 'CORRECT':
            result = 'CORRECT!'
        else:
            result = 'INCORRECT ( ' + str(self.__get_correct_amount()) + ' / ' + str(self.digit) + ' )'
            remarks = 'Correct answer is ' + self.answer
            pyxel.text((Window.WIDTH - len(remarks) * 4 )/ 2,(Window.HEIGHT - 8) / 2 + 10, remarks,pyxel.COLOR_WHITE)

        pyxel.text((Window.WIDTH - len(result) * 4 )/ 2,(Window.HEIGHT - 8) / 2, result,pyxel.COLOR_WHITE)

        guide = 'Press A/B button to go to Title'
        pyxel.text((Window.WIDTH - len(guide) * 4 )/ 2,Window.HEIGHT / 2 + 30, guide,pyxel.COLOR_WHITE)

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

    # 全難易度をクリアしたか判定する
    def __is_all_clear(self):
        enum_values = [e for e in Difficulty]
        return all(value in self.game.game_vars.cleared_difficulties for value in enum_values)

    # endregion