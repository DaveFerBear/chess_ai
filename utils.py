import chess
import random

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

'''
Count total material value of each player and return the difference
'''
def board_strength_using_piece_weights(board):
    strength = 0.0
    for piece in PIECE_WEIGHTS:
        strength += PIECE_WEIGHTS[piece]*len(board.pieces(piece, chess.WHITE))
        strength -= PIECE_WEIGHTS[piece]*len(board.pieces(piece, chess.BLACK))
    return strength

'''
Return the difference in number of available moves between each player
Try a random move to check the number of legal moves of the opponent
'''
def board_strength_using_legal_moves(board):
    num_player_legal_moves = len(board.legal_moves)
    random_move = random.choice(board.legal_moves)
    board.push(random_move)
    num_opponent_legal_moves = len(board.legal_moves)
    board.pop()

    if board.turn:
        # white has current move so player=white, opponent=black
        return num_player_legal_moves - num_opponent_legal_moves
    else:
        # black has current move so player=black, opponent=white
        return num_opponent_legal_moves - num_player_legal_moves

def weighted_board_strength(board):
    # todo: add weights to each individual evaluation
    return board_strength_using_piece_weights(board) + board_strength_using_legal_moves(board)

'''
Implementation of minimax with alpha-beta pruning.
Written as a util so any chess engines can use.
'''
def minimax(chess_tree, depth, is_maximizing_player=True, alpha=-float('inf'), beta=float('inf')):
    # If node has no children return its board value
    if len(chess_tree.leaf_nodes) == 0:
        return board_strength_using_piece_weights(chess_tree.board), chess_tree
    
    if is_maximizing_player:
        best_value = -float('inf') 
        best_board_state = None
        for child in chess_tree.leaf_nodes:
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
        for child in chess_tree.leaf_nodes:
            value, state = minimax(child, depth + 1, True, alpha, beta)
            if value < best_value:
                best_value = value
                best_board_state = state
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_board_state

'''
Returns the move needed to transform current state to next state
or None if no legal move exists
'''
def get_move_to_next_state(current_board_state, next_board_state):
    for move in current_board_state.legal_moves:
            new_board_state = current_board_state.copy(stack=True)
            new_board_state.push(move)
            if new_board_state == next_board_state:
                return move
    return None


'''
Apply fuzzy logic to determine the phase of the game based on 
remaining pieces and number of moves played
'''
def get_game_phase(current_board_state):
    num_turns = current_board_state.fullmove_number
    num_pieces = 0 #todo: count num pieces left on the board
    # todo: use num_turns and num_pieces to determine stage of game
    if num_turns < 3:
        return "early"
    elif num_pieces > 16:
        return "mid"
    else:
        return "late"
