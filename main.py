import chess
import engine
import utils

class ChessTree(object):
    def __init__(self, board_state):
        self.leaf_nodes = []     # list of ChessTree() objects
        self.board = board_state  # chess.Board() object
        self.strength = utils.board_strength_using_piece_weights(self.board)

    def generate_leaf_nodes(self, depth=1):
        if len(self.leaf_nodes) is not 0:
            print("Re-generating leaf nodes.")
        
        for m in self.board.legal_moves:
            new_board = self.board.copy(stack=True)
            new_board.push(m)
            leaf = ChessTree(new_board)
            if depth > 1:
                leaf.generate_leaf_nodes(depth-1)
            self.leaf_nodes.append(leaf)

if __name__ == '__main__':
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes(depth=3)

    for m in ct.leaf_nodes[0].leaf_nodes:
        print("---------current board state-------------")
        print(m.board)
        print("---------suggested next state------------")
        value, state = utils.minimax(m, 2)
        print(state.board)
        print("---------recommended move----------------")
        move = utils.get_move_to_next_state(m.board, state.board)
        print(move)
        print("---------game phase membership-----------")
        print(utils.get_game_phase_membership(state.board))
