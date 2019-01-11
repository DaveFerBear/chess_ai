import chess
class Engine(object):

	def __init__(self):
		pass

	'''
	params: chess.Board, chess.Color
	returns: chess.Move
	'''
	def move(self, board, side):
		print('move')

class RandomEngine(Engine):
	def __init__(self):
		super()

	def move(self, board, side):
		return super().move(board, side)
