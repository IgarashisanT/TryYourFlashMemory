from enum import Enum, auto
import pyxel

from scenes.title_scene import TitleScene
from scenes.game_scene import GameScene
from scenes.clear_scene import ClearScene
from game_vars import GameVars

class Scene(Enum):
    NONE = 0
    TITLE = auto()
    GAME = auto()
    CLEAR = auto()

class Game:
    """
    遷移を含むScene管理を制御するクラス
    """

    def __init__(self, app) -> None:
        self.app = app
        self.next_scene = None
        self.game_vars = GameVars(self)
        
        self.scene = TitleScene(self)

    def go_to_title(self):
        self.next_scene = Scene.TITLE

    def go_to_game(self,difficulty):
        self.game_vars.new_game(difficulty)
        self.next_scene = Scene.GAME

    def go_to_clear(self):
        self.next_scene = Scene.CLEAR

    def switch_scene(self):
        new_scene = None
        if self.next_scene == Scene.TITLE:
            new_scene = TitleScene
        elif self.next_scene == Scene.GAME:
            new_scene = GameScene
        elif self.next_scene == Scene.CLEAR:
            new_scene = ClearScene
        else:
            return
        self.scene.on_exit()
        self.scene = new_scene(self)
        self.next_scene = None
    
    def update(self):
        if self.next_scene is not None:
            self.switch_scene()
        self.scene.update()
    
    def draw(self):
        # 背景は必ず描画する
        pyxel.bltm(0,0,0,0,0,240,240)

        self.scene.draw()
    