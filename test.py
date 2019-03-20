from engine import Engine, RandomEngine
import tree
import chess

def test_game_tree():
	e = Engine()
	e.generate_legal_moves_and_update_game_tree(depth=2)
	game_tree = e.get_game_tree()
	print(game_tree.successors)