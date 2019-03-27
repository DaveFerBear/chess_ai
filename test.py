import chess.pgn
from fuzzy_phase import FuzzyGamePhaseSelector
import matplotlib.pyplot as plt

NEW_BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
SAMPLE_FEN_0 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
SAMPLE_FEN_1 = '5k2/ppp5/4P3/3R3p/6P1/1K2Nr2/PP3P2/8 b - - 1 32'
SAMPLE_FEN_2 = '4k3/8/8/8/8/8/4P3/4K3 w - - 5 39'

SAMPLE_GAME_PGN_PATH = 'notebooks/datasets/Adams.pgn'

def test_fuzzy_logic_discrete_states():
    print("Testing Game Phase Fuzzy Logic - phase between (0,1)")
    phase_selector = FuzzyGamePhaseSelector()
    test_fens = [NEW_BOARD_FEN, SAMPLE_FEN_0, SAMPLE_FEN_1, SAMPLE_FEN_2]

    for f in test_fens:
        board = chess.Board(fen=f)
        print(board)
        phase = phase_selector.get_game_phase(board) 
        print("Calculated phase: {}".format(phase))

def test_fuzzy_logic_continuous_game():
    # Read PGN
    pgn = open(SAMPLE_GAME_PGN_PATH)
    game = chess.pgn.read_game(pgn)
    board = game.board()
    phase_selector = FuzzyGamePhaseSelector()

    phase = []

    for move in game.mainline_moves():
        board.push(move)
        phase.append(phase_selector.get_game_phase(board))  
    plt.plot(phase)
    plt.show()


if __name__ == '__main__':
    test_fuzzy_logic_discrete_states()
    test_fuzzy_logic_continuous_game()
