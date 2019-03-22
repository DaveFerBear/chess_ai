import chess

PIECE_WEIGHTS = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.15,
    chess.ROOK: 5,
    chess.QUEEN: 9
}
'''
Stronger for white -> (+)
Stronger for black -> (-)
'''
def board_strength_using_piece_weights(board):
    strength = 0.0
    for piece in PIECE_WEIGHTS:
        strength += PIECE_WEIGHTS[piece]*len(board.pieces(piece, chess.WHITE))
        strength -= PIECE_WEIGHTS[piece]*len(board.pieces(piece, chess.BLACK))
    return strength

'''
Implementation of minimax with alpha-beta pruning.
Written as a util so any chess engines can use.
'''
def minimax(chess_tree, depth, is_maximizing_player=True, alpha=-float('inf'), beta=float('inf')):
    # If node has no children return its board value
    if len(chess_tree.leaf_boards) == 0:
        return board_strength_using_piece_weights(chess_tree.board), chess_tree
    
    if is_maximizing_player:
        best_value = -float('inf') 
        best_board_state = None
        for child in chess_tree.leaf_boards:
            value, state = minimax(child, depth + 1, False, alpha, beta)
            if value > best_value:
                best_value = value
                best_board_state = state
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_board_state

    else:
        best_value = float('inf') 
        best_board_state = None
        for child in chess_tree.leaf_boards:
            value, state = minimax(child, depth + 1, True, alpha, beta)
            if value < best_value:
                best_value = value
                best_board_state = state
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_board_state