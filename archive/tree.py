'''
Data container.  Game logic is contained in engine classes.
'''
class GameTree(object):
	def __init__(self, board, root_data):
		self.root_state = board # Only move updates are stored for space efficiency
		self.root_game_tree_node = GameTreeNode(root_data)

	class GameTreeNode(object):
		def __init__(self, data):
			self.data = data
			self.successors