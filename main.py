import chess
import engine
import utils
from chess_tree import ChessTree

def play_engines(e1, e2, print_out=False):
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes(depth=2)

    white_to_play = True

    while not b.is_game_over():
        cur_player = e1 if white_to_play else e2
        move = cur_player.play(ct)

        print("Selected Move: {}".format(move))

        ct = ct.find_new_head(move) # Travel down chess tree
        ct.generate_leaf_nodes()
        white_to_play = not white_to_play # Change player

        print("Strength: {} after {} moves.".format("%.2f" % utils.board_strength_using_piece_weights(ct.board), len(ct.board.move_stack)))
        print(ct.board)
        
    print("Winner: {}".format(type(cur_player)))


if __name__ == '__main__':

    e1 = engine.GeneticEngine()
    e2 = engine.GeneticEngine()

    play_engines(e1, e2, print_out=True)
    
