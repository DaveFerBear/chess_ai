from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
import chess

class FuzzyGamePhaseSelector(object):
    def get_game_phase(self, board):
        num_pieces = len(board.piece_map())
        num_moves = board.fullmove_number
        white_king_advanced_squares = int(board.king(chess.WHITE)/8) + 1
        black_king_advanced_squares = 8 - int(board.king(chess.BLACK)/8)

        self.sim.input['num_pieces'] = num_pieces
        self.sim.input['num_moves'] = num_moves
        self.sim.input['white_king_advanced_squares'] = white_king_advanced_squares
        self.sim.input['black_king_advanced_squares'] = black_king_advanced_squares
        self.sim.compute()

        return self.sim.output['game_phase']

    def __init__(self):
        # Create fuzzy variables
        num_pieces = ctrl.Antecedent(np.arange(2, 33, 1), 'num_pieces')
        num_moves = ctrl.Antecedent(np.arange(0, 150, 1), 'num_moves')
        white_king_advanced_squares = ctrl.Antecedent(np.arange(1,9,1), 'white_king_advanced_squares')
        black_king_advanced_squares = ctrl.Antecedent(np.arange(1,9,1), 'black_king_advanced_squares')
        game_phase = ctrl.Consequent(np.linspace(0, 1, 50), 'game_phase')

        # Populate the fuzzy variables with membership functions
        num_pieces['LOW'] = fuzz.gaussmf(num_pieces.universe, 0, 8)
        num_pieces['MEDIUM'] = fuzz.pimf(num_pieces.universe, 4, 15, 17, 28)
        num_pieces['HIGH'] = fuzz.gaussmf(num_pieces.universe, 32, 8)

        num_moves['LOW'] = fuzz.sigmf(num_moves.universe, 10, -.4)
        num_moves['MEDIUM'] = fuzz.pimf(num_moves.universe, 10, 20, 30, 60)
        num_moves['HIGH'] = fuzz.sigmf(num_moves.universe, 45, .1)

        a = fuzz.trimf(black_king_advanced_squares.universe, [1,1,8])
        b = fuzz.trimf(black_king_advanced_squares.universe, [1,8,8])
        white_king_advanced_squares['RETREATED'] = a
        white_king_advanced_squares['ADVANCED'] = b
        black_king_advanced_squares['RETREATED'] = a
        black_king_advanced_squares['ADVANCED'] = b

        game_phase.automf(names=['OPENING', 'MIDDLE', 'END'])

        # Add extra game phases for king file rules.
        game_phase['PROBABLY_OPENING'] = fuzz.trapmf(game_phase.universe, [0,.1,.5,.6])/3
        game_phase['PROBABLY_END'] = fuzz.trapmf(game_phase.universe, [.4,.5,.9,1])/3

        rules = [
            ctrl.Rule(antecedent=num_pieces['HIGH'], consequent=game_phase['OPENING']),
            ctrl.Rule(antecedent=num_pieces['MEDIUM'], consequent=game_phase['MIDDLE']),
            ctrl.Rule(antecedent=num_pieces['LOW'], consequent=game_phase['END']),

            ctrl.Rule(antecedent=num_moves['LOW'], consequent=game_phase['OPENING']),
            ctrl.Rule(antecedent=num_moves['MEDIUM'], consequent=game_phase['MIDDLE']),
            ctrl.Rule(antecedent=num_moves['HIGH'], consequent=game_phase['END']),
            
            ctrl.Rule(antecedent=(
                white_king_advanced_squares['RETREATED'] & black_king_advanced_squares['RETREATED']),
                consequent=game_phase['PROBABLY_OPENING']),
            ctrl.Rule(antecedent=(
                white_king_advanced_squares['ADVANCED'] & black_king_advanced_squares['ADVANCED']),
                consequent=game_phase['PROBABLY_END'])
        ]

        system = ctrl.ControlSystem(rules=rules)
        self.sim = ctrl.ControlSystemSimulation(system, flush_after_run=1) # TODO: when to flush.
