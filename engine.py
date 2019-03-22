import utils

class ChessEngine(object):
    def __init__(self):
        pass
    
    def play(self, chess_tree):
        raise Exception("play() function not implemented.")

class MiniMaxEngine(ChessEngine):
    def __init__(self):
        super()
    
    def play(self, chess_tree):
        value, state = utils.minimax(chess_tree, 2)
        return state


# More engines below, ex. RLEngine, GeneticEngine, etc.
# ...