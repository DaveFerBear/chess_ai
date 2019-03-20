import test

def user_gameplay():
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

if __name__ == '__main__':
	test.test_game_tree()
	