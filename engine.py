import chess
from tree import GameTree

class Engine(object):

	def __init__(self, board=None):
		if board:
			self.board = board
		else:
			self.board = chess.Board()

		self.game_tree_root = GameTree(self.board)

	'''
	params: chess.Board, chess.Color
	returns: chess.Move
	'''
	def update_move(self, board, move):
		print('move')

	def generate_legal_moves_and_update_game_tree(self, board, depth=1):
		if depth < 1:
			return

		if len(self.board.successors) != 0:
			raise ValueError('Expected empty game tree successors but nodes exist.')

		self.board.successors = [m for m in self.board.generate_legal_moves()]

		for move in self.board.successors:
			self.board.push(move)
			generate_legal_moves_and_update_game_tree(self.board, depth=depth-1)
			self.board.pop() # Don't alter the current game board.

	def get_game_tree(self):
		return self.game_tree_root

class RandomEngine(Engine):
	def __init__(self):
		super()

	def move(self, board, side):
		return super().move(board, side)
