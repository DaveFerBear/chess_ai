import chess
import engine
import utils
from chess_tree import ChessTree

if __name__ == '__main__':
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes(depth=2)

    for m in ct.leaf_nodes[0].leaf_nodes:
        print("---------current board state-------------")
        print(m.board)
        print("---------suggested next state------------")
        value, state = utils.minimax(m, 2)
        print(state.board)
