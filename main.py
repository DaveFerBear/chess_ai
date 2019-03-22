import chess
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

    def minimax(self, depth, is_maximizing_player=True, alpha=-float('inf'), beta=float('inf')):
        # If node has no children return its board value
        if len(self.leaf_boards) == 0:
            return utils.board_strength_using_piece_weights(self.board), self
        
        if is_maximizing_player:
            best_value = -float('inf') 
            best_board_state = None
            for child in self.leaf_boards:
                value, state = child.minimax(depth + 1, False, alpha, beta)
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
            for child in self.leaf_boards:
                value, state = child.minimax(depth + 1, True, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_board_state = state
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value, best_board_state
            

class ChessEngine(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes(depth=3)

    for m in ct.leaf_boards[0].leaf_boards:
        print("---------current board state-------------")
        print(m.board)
        print("---------suggested next move-------------")
        value, state = m.minimax(2)
        print(state.board)
