import chess
from tree import GameTree

class Engine(object):

	def __init__(self, board=None):
		if board:
			self.board = board
		else:
			self.board = chess.Board()

		self.game_tree = GameTree(self.board, chess.Move()) # Null move is root node state.

	'''
	params: chess.Board, chess.Color
	returns: chess.Move
	'''
	def update_move(self, board, move):
		print('move')

	def generate_legal_moves_and_update_game_tree(self, depth=2):
		if depth < 1:
			return

		if len(self.game_tree.successors) != 0:
			raise ValueError('Expected empty game tree successors but nodes exist.')

		self.game_tree.successors = [m for m in self.board.generate_legal_moves()]

		for move in self.game_tree.successors:
			self.board.push(move)
			self.generate_legal_moves_and_update_game_tree(depth=depth-1)
			self.board.pop() # Don't alter the current game board.

	def get_game_tree(self):
		return self.game_tree

class RandomEngine(Engine):
	def __init__(self):
		super()

	def move(self, board, side):
		return super().move(board, side)
