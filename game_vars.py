class GameVars:
    """
    Sceneを超えたゲーム・変数の制御を行うクラス
    """

    def __init__(self, game):
        self.game = game
        self.difficulty = None
        self.cleared_difficulties = []

    def new_game(self, difficulty):
        self.difficulty = difficulty