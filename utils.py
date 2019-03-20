import chess

PIECE_WEIGHTS = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.15,
    chess.ROOK: 5,
    chess.QUEEN: 9
}

# Stronger for white -> (+)
# Stronger for black -> (-)
def board_strength_using_piece_weigths(board):
    strength = 0.0
    for piece in PIECE_WEIGHTS:
        strength += PIECE_WEIGHTS[piece]*len(board.pieces(piece, chess.WHITE))
        strength -= PIECE_WEIGHTS[piece]*len(board.pieces(piece, chess.BLACK))
    return strength