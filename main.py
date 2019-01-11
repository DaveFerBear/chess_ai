from engine import RandomEngine
import chess

if __name__ == '__main__':
	board = chess.Board()
	engine = RandomEngine()
	
	game_over = False
	while not board.is_checkmate():
		print(board)
		move = input('Enter UCI Move: ')
		board.push_san(move)

	print(board)