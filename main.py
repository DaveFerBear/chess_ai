import chess

class ChessTree(object):
    def __init__(self, board_state):
        self.leaf_boards = []
        self.board = board_state
    
    def generate_leaf_nodes(self):
        if len(self.leaf_boards) is not 0:
            print("Re-generating leaf nodes.")
        
        for m in self.board.legal_moves:
            new_board = self.board.copy(stack=True)
            new_board.push(m)
            leaf = ChessTree(new_board)
            self.leaf_boards.append(leaf)

class ChessEngine(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    b = chess.Board()
    ct = ChessTree(b)
    ct.generate_leaf_nodes()

    for m in ct.leaf_boards:
        print(m.board)
	