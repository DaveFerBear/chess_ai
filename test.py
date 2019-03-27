import chess
from fuzzy_phase import FuzzyGamePhaseSelector


NEW_BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
SAMPLE_FEN = '5k2/ppp5/4P3/3R3p/6P1/1K2Nr2/PP3P2/8 b - - 1 32'

def test_fuzzy_logic():
    print("Testing Game Phase Fuzzy Logic - phase between (0,1)")
    phase_selector = FuzzyGamePhaseSelector()
    test_fens = [NEW_BOARD_FEN, SAMPLE_FEN]

    for f in test_fens:
        board = chess.Board(fen=f)
        print(board)
        phase = phase_selector.get_game_phase(board) 
        print("Calculated phase: {}".format(phase))

if __name__ == '__main__':
    test_fuzzy_logic()
