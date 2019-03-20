import chess

class ChessTree(object):
    def __init__(self, board_state):
        self.legal_moves = []
        self.board = board_state
    
    def generate_leaf_nodes(self):
        if len(self.legal_moves) is not 0:
            print("Re-generating leaf nodes.")
        for m in self.board.legal_moves:
            leaf = self.board.copy(stack=True)
            leaf.push(m)
            self.legal_moves.append(leaf)

class ChessEngine(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes()
	