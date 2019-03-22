import utils
import random

class ChessEngine(object):
    def __init__(self):
        pass
    
    def play(self, chess_tree):
        raise Exception("play() function not implemented.")

'''
Example engine giving random moves.
'''
class RandomEngine(ChessEngine):
    def __init__(self):
        super()
    
    def play(self, chess_tree):
        return random.choice(chess_tree.leaf_boards)

'''
Engine using exclusively minimax with alpha-beta pruning.
'''
class MiniMaxEngine(ChessEngine):
    def __init__(self):
        super()
    
    def play(self, chess_tree):
        value, state = utils.minimax(chess_tree, 2)
        return state


# More engines below, ex. RLEngine, GeneticEngine, etc.
# ...