import pickle
import re, os, time
from random import triangular
from math import floor
import sunfish
from PST import PST

MAX_NUM_MOVES = 200
SEARCH_TIME = 1


class Engine:
    def __init__(self, prefix):
        self.load_from_pckl(prefix)
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, self.pst_padded)
        self.searcher = sunfish.Searcher()
    
    def reset_position(self):
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, self.pst_padded)
        self.searcher = sunfish.Searcher()

    def set_position(self, board, white, wc, bc, ep, kp):
        self.pos = sunfish.Position(board, 0, wc, bc, ep, kp, self.pst_padded)
        if not white:
            self.pos = self.pos.rotate()


    def load_from_pckl(self, prefix):
        self.pst, self.piece = PST.load_data(prefix)
        self.pst_padded = PST.generate_pst_padded(self.pst, self.piece)
    
    def save_to_pckl(self, prefix):
        PST.save_data(self.pst, self.piece, prefix)

    def evolve(self, random_pst, random_piece):
        self.pst = PST.randomize_pst(self.pst, random_pst)
        self.piece = PST.randomize_piece(self.piece, random_piece)
        self.pst_padded = PST.generate_pst_padded(self.pst, self.piece)

    # Convert from 'd2d4' to '(84, 64)'
    def parse(self, c, white=True):
        if not white:
            c = self.convert_black_move(c)
        fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
        A = 91 + fil - 10*rank
        fil, rank = ord(c[2]) - ord('a'), int(c[3]) - 1
        B = 91 + fil - 10*rank
        return (A,B)

    # Convert from '(84, 64)' to 'd2d4'
    def inv_parse(self, c, white=True):
        a,b = c # Separate squares
        move = str(chr(97-1+a%10))+str(10-floor(a/10))
        move += str(chr(97-1+b%10))+str(10-floor(b/10))
        if not white:
            move = self.convert_black_move(move)
        return move

    # Rotates board to move for black, need to rotate move
    # 'move' is in conventional notation: 'd2d4'
    def convert_black_move(self, move):
        new_move = str(chr(ord('h') - ord(move[0]) + ord('a')))
        new_move += str(8-int(move[1])+1)
        new_move += str(chr(ord('h') - ord(move[2]) + ord('a')))
        new_move += str(8-int(move[3])+1)
        return new_move

    # 2 functions below act as the API
    # play_move returns the move
    # load_board coverts python chess board
    def play_move(self, white=True):
        move, score = self.searcher.search(self.pos, secs=SEARCH_TIME)
        self.pos = self.pos.move(move)
        return self.inv_parse(move, white)

    # Loads python chess board object
    def load_board(self, board):
        wc = (board.has_kingside_castling_rights(True), board.has_queenside_castling_rights(True))
        bc = (board.has_kingside_castling_rights(False), board.has_queenside_castling_rights(False))
        ep = None
        if board.ep_square:
            if board.turn: # Black side
                ep = board.ep_square+1 # +1 due to padding
            else: # White side
                ep = board.ep_square+55 # Since board is flipped and padded
        self.set_position(b, board.turn, wc, bc, ep, 0)
        


class Game:
    def __init__(self, white_engine, black_engine, print_pos):
        self.white = white_engine
        self.black = black_engine
        self.print = print_pos
        self.winner = ""
        self.moves = []

    def play(self):
        self.white.reset_position()
        self.black.reset_position()
        while True:
            # White to move.
            move, score = self.white.searcher.search(self.white.pos, secs=SEARCH_TIME)
            self.white.pos = self.white.pos.move(move)
            self.black.pos = self.black.pos.move(move)
            self.moves.append(self.white.inv_parse(move, True))
            if self.print:
                print(self.white.inv_parse(move, True))
                sunfish.print_pos(self.white.pos.rotate())
                print(-self.white.pos.score)

            if self.white.pos.score <= -sunfish.MATE_LOWER:
                self.winner = "White"
                break

            # Black to move.
            move, score = self.black.searcher.search(self.black.pos, secs=SEARCH_TIME)
            self.white.pos = self.white.pos.move(move)
            self.black.pos = self.black.pos.move(move)
            self.moves.append(self.black.inv_parse(move, False))
            if self.print:
                print(self.black.inv_parse(move, False))
                sunfish.print_pos(self.black.pos)
                print(self.black.pos.score)

            if self.black.pos.score <= -sunfish.MATE_LOWER:
                self.winner = "Black"
                break

            # Check for draw
            if len(self.moves) > 8:
                if (self.moves[-8] == self.moves[-4] and self.moves[-2] == self.moves[-6] and
                    self.moves[-1] == self.moves[-5] and self.moves[-3] == self.moves[-7]):
                    self.winner = "Draw - Repetition"
                    break
            elif len(self.moves) >= MAX_NUM_MOVES:
                    self.winner = "Draw - Max Moves"
                    break
        print(self.winner)
        self.save_moves()

    def save_moves(self):
        game_num = 1
        path = 'Genetic/Games/' + str(game_num) + '.pckl'
        while os.path.isfile(path):
            game_num += 1
            path = 'Genetic/Games/' + str(game_num) + '.pckl'
        f = open('Genetic/Games/' + str(game_num) + '.pckl', 'wb')
        pickle.dump(self.moves, f)
        f.close()

    def load_moves(self, game_num):
        f = open('Genetic/Games/' + str(game_num) + '.pckl', 'rb')
        self.moves = pickle.load(f)
        f.close()
        self.white.reset_position()
        i = 0
        for move in self.moves:
            if i%2 == 0:
                self.white.pos = self.white.pos.move(self.white.parse(move, True))
                print(move)
                sunfish.print_pos(self.white.pos.rotate())
            else:
                self.white.pos = self.white.pos.move(self.white.parse(move, False))
                print(move)
                sunfish.print_pos(self.white.pos)
            i += 1
            time.sleep(1)


class Match:
    def __init__(self, engine1, engine2, num_games, print_pos=False):
        self.engine1 = engine1
        self.engine2 = engine2
        self.num_games = num_games
        self.print_pos = print_pos
        self.results = []
        self.score = 0

    def play(self):
        for i in range(self.num_games):
            game = Game(self.engine1, self.engine2, self.print_pos)
            game.play()
            if game.winner == "White":
                self.results.append(1)
                self.score += 1
            elif game.winner == "Black":
                self.results.append(-1)
                self.score -= 1
            else:
                self.results.append(0)
        # Now switch sides
        for i in range(self.num_games):
            game = Game(self.engine2, self.engine1, self.print_pos)
            game.play()
            if game.winner == "Black":
                self.results.append(1)
                self.score += 1
            elif game.winner == "White":
                self.results.append(-1)
                self.score -= 1
            else:
                self.results.append(0)
        print("Results:", self.results)
        print("Final score:", self.score)


def train():
    #Configurations
    piece_randomness = 3
    pst_randomness = 4
    games_per_match = 2
    generations = 100
    # Load current best engine
    engine1 = Engine("Best")
    engine2 = Engine("Init")
    engine2.evolve(pst_randomness, piece_randomness)
    for gen in range(generations):
        print("\nGeneration", gen+1)
        engine2.save_to_pckl("GEN"+str(gen+1))
        match = Match(engine1, engine2, games_per_match, False)
        match.play()
        if match.score > 0:
            print("Winner is Engine1!")
            engine2.load_from_pckl("Best") # Copy engine 1
            engine2.evolve(pst_randomness, piece_randomness)
        elif match.score < 0:
            print("Winner is Engine2!")
            engine2.save_to_pckl("Best")
            engine1.load_from_pckl("Best")
            engine2.evolve(pst_randomness, piece_randomness)
        else:
            print("Match ends in a draw")
            engine2.evolve(pst_randomness, piece_randomness)

def playback(game_num):
    engine = Engine("Best")
    game = Game(engine, None, True)
    game.load_moves(game_num)

def show_params(prefix):
    engine = Engine(prefix)
    print(engine.pst)
    print(engine.piece)

def play_stock():
    engine_trained = Engine("Best")
    engine_stock = Engine("Init")
    match = Match(engine_trained, engine_stock,1, True)
    match.play()
    


if __name__ == '__main__':
    #train()
    #playback(541)
    show_params("Best")
    print()
    show_params("Init")
    #play_stock()
