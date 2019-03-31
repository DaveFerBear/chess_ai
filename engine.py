import utils
import random
import sys
import Genetic.Genetic as Genetic
from network import core

# from fuzzy_phase import FuzzyGamePhaseSelector

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
        next_board_state = random.choice(chess_tree.leaf_nodes)
        move = utils.get_move_to_next_state(chess_tree.board, next_board_state.board)
        return move

'''
Engine using exclusively minimax with alpha-beta pruning.
'''
class MiniMaxEngine(ChessEngine):
    def __init__(self):
        self.model = core.Model()
        super()
    
    def play(self, chess_tree):
        print(chess_tree)
        value, next_board_state = utils.minimax(self.model, chess_tree, 2)
        move = next_board_state.board.peek()
        print("MINIMAX ENGINE MOVE: {}".format(move))
        return move

'''
Mitch to add play method and description here
'''
class OpeningEngine(ChessEngine):
    def __init__(self):
        self.model = core.Model()
        print("Created Model")
        super()

    def play(self, chess_tree):
        best_score = 0
        best_move = None

        chess_tree.generate_leaf_nodes(depth=1)
        leaves = []
        for leaf in chess_tree.leaf_nodes:
            # print(leaf.board)
            # print(leaf.board.turn)
            # print(leaf.board.peek())
            score = self.model.inference(leaf.board, leaf.board.turn)
            # print(score)

            if best_move == None or score > best_score:
                best_move = leaf.board.peek()
                best_score = score
        sys.exit()
        return best_move

'''
Ross to add play method and description here
'''
class GeneticEngine(ChessEngine):
    def __init__(self):
        super()
        self.engine = Genetic.Engine("Best")
    
    def play(self, chess_tree):
        self.engine.load_board(chess_tree.board)
        move = self.engine.play_move(chess_tree.board.turn)
        return utils.chess.Move.from_uci(move)

'''
A combination of the Opening, Genetic, and MiniMax engines
'''
class HybridEngine(ChessEngine):
    def __init__(self):
        super()
        self.phase_selector = FuzzyGamePhaseSelector()
    
    def play(self, chess_tree):
        game_phase = phase_selector.get_game_phase(chess_tree.board_state)
        if game_phase < 0.3:
            return OpeningEngine.play(chess_tree.board_state)
        elif game_phase < 0.6:
            return GeneticEngine.play(chess_tree.board_state)
        else:
            return MiniMaxEngine.play(chess_tree.board_state)
