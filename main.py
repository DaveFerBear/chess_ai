import chess
import engine
import utils

class ChessTree(object):
    def __init__(self, board_state):
        self.leaf_boards = []     # list of ChessTree() objects
        self.board = board_state  # chess.Board() object
        self.strength = utils.board_strength_using_piece_weights(self.board)

    def generate_leaf_nodes(self, depth=1):
        if len(self.leaf_boards) is not 0:
            print("Re-generating leaf nodes.")
        
        for m in self.board.legal_moves:
            new_board = self.board.copy(stack=True)
            new_board.push(m)
            leaf = ChessTree(new_board)
            if depth > 1:
                leaf.generate_leaf_nodes(depth-1)
            self.leaf_boards.append(leaf)

if __name__ == '__main__':
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes(depth=3)

    for m in ct.leaf_boards[0].leaf_boards:
        print("---------current board state-------------")
        print(m.board)
        print("---------suggested next move-------------")
        value, state = utils.minimax(m, 2)
        print(state.board)
