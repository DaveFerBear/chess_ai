from engine import RandomEngine
import chess

if __name__ == '__main__':
	board = chess.Board()
	engine = RandomEngine()
	
	game_over = False
	while not board.is_game_over():
		print(board)
		text_in = input('Enter SAN Move: ')
		
		if text_in == 'exit':
			exit()
		
		# Execue Move
		try:
			board.push_san(text_in)
		except ValueError:
			pass

	print(board)